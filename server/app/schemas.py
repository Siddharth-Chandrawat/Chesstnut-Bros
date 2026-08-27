from typing import List, Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    # Restricted charset: the username becomes part of a DynamicKV
    # model name ("games_<username>") and a URL path segment, so it
    # can't contain anything that would break either.
    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_-]+$")
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MoveRequest(BaseModel):
    from_sq: int = Field(ge=0, le=63)
    to_sq: int = Field(ge=0, le=63)


class MoveResult(BaseModel):
    game_id: str
    fen: str
    status: str
    human_move: List[int]
    engine_move: Optional[List[int]] = None
    engine_eval: Optional[float] = None


class NewGameOut(BaseModel):
    game_id: str
    fen: str


class GameOut(BaseModel):
    game_id: str
    fen: str
    status: str
    moves: List[List[int]]
    created_at: str
    updated_at: str