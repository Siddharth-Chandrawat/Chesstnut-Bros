import json
import sys

from utils import logic
from utils.search import computerMakeMove  # <-- extract this from main.py, see docstring above


def main() -> None:
    fen = sys.argv[1]
    depth = int(sys.argv[2])

    board = logic.readFen(fen)
    white_to_move = fen.split(" ")[1] == "w"

    result = computerMakeMove(board, depth, white_to_move, depth, -10_000_000, 10_000_000)

    best_move, best_eval = result

    print(json.dumps({"move": best_move, "eval": best_eval}))


if __name__ == "__main__":
    main()
