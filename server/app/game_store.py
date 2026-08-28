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
    game = await kv.kv_get(kv.games_model(username), game_id)
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game


async def save_game(game: dict, expected_version: int) -> None:
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
    games = await kv.kv_get_all(kv.games_model(username))
    return list(games.values())
