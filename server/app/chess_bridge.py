"""
The server's direct connection to chesstnut/utils/logic.py, used for
fast, synchronous move validation and application. This is NOT the
slow minimax search — that's dispatched to an isolated subprocess by
engine_client.py. Everything in this file is cheap (microseconds to
low milliseconds) and safe to run inline on the server's event loop,
AS LONG AS THE PATCH BELOW HAS BEEN APPLIED.

--------------------------------------------------------------------
REQUIRED PATCH — apply this to chesstnut/utils/logic.py before using
this file for anything beyond a single game:

logic.py keeps board state — king locations, piece-location lists,
attack-square arrays, castling flags — as MODULE-LEVEL GLOBALS, and
`readFen` does not fully reset them: it appends onto the existing
piece-location lists instead of clearing them, and never touches the
castling flags at all. This server process is long-lived and handles
MANY DIFFERENT users' games in sequence, so calling `logic.readFen`
here for game A and then again for game B WILL corrupt state unless
`readFen` resets everything it owns at the top of the function:

    blackPiecesLocation = []
    whitePiecesLocation = []
    whiteAttackSquares = [0] * 64
    blackAttackSquares = [0] * 64
    blackKingLocation = -1
    whiteKingLocation = -1
    hasWhiteKingMoved = hasBlackKingMoved = False
    hasWhiteLeftRookMoved = hasBlackLeftRookMoved = False
    hasWhiteRightRookMoved = hasBlackRightRookMoved = False

This is required here even though this file never runs a search —
it's a consequence of calling readFen more than once in one process,
independent of concurrency.
--------------------------------------------------------------------

Also verify the exact parameter names/order in legalMoves/makeMove
below against your current logic.py — written to match what was
read out of the repository, but confirm before trusting this beyond
local testing.
"""
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
    """
    Reconstructs the FEN reached after applying `moves` in order from
    the starting position. The server only ever stores the CURRENT fen
    plus the move list, not a snapshot per ply — this is what makes
    "undo" possible without keeping that extra history around: trim
    the move list and recompute from scratch.
    """
    fen = STARTING_FEN
    for from_sq, to_sq in moves:
        fen, _captured = apply_move(fen, from_sq, to_sq)
    return fen