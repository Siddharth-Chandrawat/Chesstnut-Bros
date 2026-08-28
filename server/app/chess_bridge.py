import sys
from pathlib import Path

from .config import settings

sys.path.insert(0, str(Path(settings.chesstnut_dir).resolve()))

from utils import logic  # noqa: E402  (headless — no pygame/tkinter import in this module)

from .game_store import STARTING_FEN

PIECE_TO_FEN = {
    1: "k", 2: "q", 3: "r", 4: "n", 5: "b", 6: "p",
    8: "K", 9: "Q", 10: "R", 11: "N", 12: "B", 13: "P",
}


class IllegalMoveError(Exception):
    pass


def _side_to_move(fen: str) -> bool:
    # True = white to move, matching main.py's `currentTurn = True` convention.
    return fen.split(" ")[1] == "w"


def _castling_rights_string() -> str:
    rights = ""
    if not logic.hasWhiteKingMoved and not logic.hasWhiteRightRookMoved:
        rights += "K"
    if not logic.hasWhiteKingMoved and not logic.hasWhiteLeftRookMoved:
        rights += "Q"
    if not logic.hasBlackKingMoved and not logic.hasBlackRightRookMoved:
        rights += "k"
    if not logic.hasBlackKingMoved and not logic.hasBlackLeftRookMoved:
        rights += "q"
    return rights or "-"


def board_to_fen(board: list, white_to_move: bool, fullmove_number: int) -> str:
    """
    logic.py has no FEN serializer (only readFen, the inverse) — this
    is new code, not a wrapper around something that already existed.
    En passant is always "-" since the engine doesn't implement it.
    """
    rows = []
    for row in range(8):
        empty = 0
        row_str = ""
        for col in range(8):
            piece = board[row * 8 + col]
            if piece == -1:
                empty += 1
            else:
                if empty:
                    row_str += str(empty)
                    empty = 0
                row_str += PIECE_TO_FEN.get(piece, "?")
        if empty:
            row_str += str(empty)
        rows.append(row_str)
    placement = "/".join(rows)
    side = "w" if white_to_move else "b"
    castling = _castling_rights_string()
    return f"{placement} {side} {castling} - 0 {fullmove_number}"


def apply_move(fen: str, from_sq: int, to_sq: int) -> tuple[str, bool]:
    """
    Validates [from_sq, to_sq] as legal for the side to move in `fen`,
    applies it, and returns (new_fen, was_capture).
    Raises IllegalMoveError if the move isn't legal.
    """
    board = logic.readFen(fen)  # resets logic.py's globals for THIS position (requires the patch above)
    white_to_move = _side_to_move(fen)

    # NOTE: verify this matches your actual legalMoves signature.
    legal = logic.legalMoves(board, from_sq, white_to_move)
    if [from_sq, to_sq] not in legal:
        raise IllegalMoveError(f"{[from_sq, to_sq]} is not legal in position {fen}")

    captured_piece, _flag = logic.makeMove(board, [from_sq, to_sq])

    fullmove_number = int(fen.split(" ")[-1])
    new_fullmove = fullmove_number + (1 if not white_to_move else 0)  # FEN increments after Black's move

    new_fen = board_to_fen(board, not white_to_move, new_fullmove)
    return new_fen, captured_piece != -1


def has_legal_moves(fen: str, white_to_move: bool) -> bool:
    """Used after each half-move to detect checkmate/stalemate at the API layer."""
    board = logic.readFen(fen)
    pieces = logic.whitePiecesLocation if white_to_move else logic.blackPiecesLocation
    for square in pieces:
        if logic.legalMoves(board, square, white_to_move):
            return True
    return False


def replay_moves(moves: list) -> str:
    fen = STARTING_FEN
    for from_sq, to_sq in moves:
        fen, _captured = apply_move(fen, from_sq, to_sq)
    return fen
