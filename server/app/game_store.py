import asyncio
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status

from . import kv_client as kv

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
USERS_MODEL = "users"

# One asyncio.Lock per game_id, created on first use. Guards against
# two overlapping requests (a duplicate click, a client retry) racing
# a read-modify-write against the same game record.
_game_locks: dict[str, asyncio.Lock] = {}
_locks_guard = asyncio.Lock()


async def get_game_lock(game_id: str) -> asyncio.Lock:
    async with _locks_guard:
        lock = _game_locks.get(game_id)
        if lock is None:
            lock = asyncio.Lock()
            _game_locks[game_id] = lock
        return lock


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def get_user(username: str) -> Optional[dict]:
    return await kv.kv_get(USERS_MODEL, username)


async def create_user(username: str, password_hash: str) -> None:
    await kv.kv_set(
        USERS_MODEL, username,
        {"username": username, "password_hash": password_hash, "created_at": _now()},
    )


async def create_game(username: str) -> dict:
    game_id = uuid.uuid4().hex[:12]
    game = {
        "game_id": game_id,
        "username": username,
        "fen": STARTING_FEN,
        "status": "in_progress",
        "moves": [],
        "version": 0,
        "created_at": _now(),
        "updated_at": _now(),
    }
    await kv.kv_set(kv.games_model(username), game_id, game)
    return game


async def load_game(username: str, game_id: str) -> dict:
    """
    Games live in a model scoped to their owner (games_<username>),
    so this can never return a different user's game by construction
    — DynamicKV has no cross-model key lookup, so the caller must
    already know whose games to look in. Callers get `username` from
    the authenticated request, never from the client's input.
    """
    game = await kv.kv_get(kv.games_model(username), game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game


async def save_game(game: dict, expected_version: int) -> None:
    """
    Optimistic concurrency as a second line of defense underneath the
    per-game asyncio.Lock: re-check the version immediately before
    writing, and reject if something else updated this game in the
    meantime. DynamicKV's API has no compare-and-swap primitive, so
    this check-then-write is still a narrow race in the abstract —
    it's the per-game asyncio.Lock (held by the caller for the whole
    request) that actually closes it for anything going through this
    server.
    """
    model = kv.games_model(game["username"])
    current = await kv.kv_get(model, game["game_id"])
    if current is not None and current.get("version", 0) != expected_version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Game was modified concurrently, reload and retry",
        )
    game["version"] = expected_version + 1
    game["updated_at"] = _now()
    await kv.kv_set(model, game["game_id"], game)


async def list_user_games(username: str) -> list[dict]:
    """
    A single GET /{model} against this user's games model. No
    application-maintained index list needed — DynamicKV already
    groups records by model, which is what the old _add_game_to_user_index
    / list_user_games index-list approach was working around.
    """
    games = await kv.kv_get_all(kv.games_model(username))
    return list(games.values())