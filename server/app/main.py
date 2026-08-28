from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from . import chess_bridge, engine_client, game_store, kv_client
from .config import settings
from .schemas import GameOut, MoveRequest, MoveResult, NewGameOut, RegisterRequest, TokenResponse
from .security import create_access_token, get_current_username, hash_password, verify_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    kv_client.get_client() 
    yield
    await kv_client.close_client()


app = FastAPI(title="Chesstnut Bros API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=TokenResponse)
async def register(body: RegisterRequest):
    if await game_store.get_user(body.username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    await game_store.create_user(body.username, hash_password(body.password))
    return TokenResponse(access_token=create_access_token(body.username))


@app.post("/login", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await game_store.get_user(form.username)
    if user is None or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return TokenResponse(access_token=create_access_token(form.username))


@app.post("/games", response_model=NewGameOut)
async def new_game(username: str = Depends(get_current_username)):
    game = await game_store.create_game(username)
    return NewGameOut(game_id=game["game_id"], fen=game["fen"])


@app.get("/games", response_model=List[GameOut])
async def list_games(username: str = Depends(get_current_username)):
    games = await game_store.list_user_games(username)
    return [GameOut(**g) for g in games]


@app.get("/games/{game_id}", response_model=GameOut)
async def get_game(game_id: str, username: str = Depends(get_current_username)):
    game = await game_store.load_game(username, game_id)
    return GameOut(**game)


@app.post("/games/{game_id}/move", response_model=MoveResult)
async def submit_move(game_id: str, body: MoveRequest, username: str = Depends(get_current_username)):
    lock = await game_store.get_game_lock(game_id)
    async with lock:  
        game = await game_store.load_game(username, game_id)
        if game["status"] != "in_progress":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game already finished")

        try:
            new_fen, _captured = chess_bridge.apply_move(game["fen"], body.from_sq, body.to_sq)
        except chess_bridge.IllegalMoveError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

        game["fen"] = new_fen
        game["moves"].append([body.from_sq, body.to_sq])
        expected_version = game["version"]

        if not chess_bridge.has_legal_moves(new_fen, white_to_move=False):
            game["status"] = "white_won"  # simplification: not yet distinguishing checkmate vs. stalemate
            await game_store.save_game(game, expected_version)
            return MoveResult(
                game_id=game_id, fen=game["fen"], status=game["status"],
                human_move=[body.from_sq, body.to_sq],
            )

        try:
            result = await engine_client.compute_engine_move(new_fen)
        except engine_client.EngineTimeoutError as exc:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(exc))
        except engine_client.EngineError as exc:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))

        engine_from, engine_to = result["move"]
        engine_fen, _captured = chess_bridge.apply_move(game["fen"], engine_from, engine_to)
        game["fen"] = engine_fen
        game["moves"].append([engine_from, engine_to])

        if not chess_bridge.has_legal_moves(engine_fen, white_to_move=True):
            game["status"] = "black_won"

        await game_store.save_game(game, expected_version)

        return MoveResult(
            game_id=game_id,
            fen=game["fen"],
            status=game["status"],
            human_move=[body.from_sq, body.to_sq],
            engine_move=[engine_from, engine_to],
            engine_eval=result.get("eval"),
        )


@app.post("/games/{game_id}/resign", response_model=GameOut)
async def resign_game(game_id: str, username: str = Depends(get_current_username)):
    lock = await game_store.get_game_lock(game_id)
    async with lock:
        game = await game_store.load_game(username, game_id)
        if game["status"] != "in_progress":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game already finished")

        expected_version = game["version"]
        game["status"] = "black_won"  # human resigned — engine is credited with the win
        await game_store.save_game(game, expected_version)
        return GameOut(**game)


@app.post("/games/{game_id}/undo", response_model=GameOut)
async def undo_move(game_id: str, username: str = Depends(get_current_username)):
    lock = await game_store.get_game_lock(game_id)
    async with lock:
        game = await game_store.load_game(username, game_id)
        if game["status"] != "in_progress":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't undo a finished game")
        if len(game["moves"]) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No move to undo yet")

        game["moves"] = game["moves"][:-2]
        game["fen"] = chess_bridge.replay_moves(game["moves"])
        expected_version = game["version"]
        await game_store.save_game(game, expected_version)
        return GameOut(**game)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
