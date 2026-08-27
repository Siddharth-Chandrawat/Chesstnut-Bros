from utils import logic
from utils import eval, misc
from copy import deepcopy

from collections import defaultdict

TRANSPOSITION_TABLE = defaultdict(lambda: 0.1)

def computerMakeMove(board, depth, currentTurn, og_depth, alpha, beta):
    moves = eval.MoveOrder(board, logic.generateAllMoves(board, currentTurn), currentTurn, logic.blackAttackSquares, logic.whiteAttackSquares)
    
    if (not moves):
        if currentTurn:
            if logic.isKingInCheck(logic.whiteKingLocation, currentTurn):
                return -1000000
            else:
                return 0
        else:
            if logic.isKingInCheck(logic.blackKingLocation, currentTurn):
                return 1000000
            else:
                return 0
    if (depth == 0):
        return searchCaptures(board, alpha, beta, currentTurn)
        # TRANSPOSITION_TABLE[misc.genZobrist(board)] = val
    bestMove = moves[0]
    if currentTurn:
        bestEval = -100000
        # print("the moves calculated for depth:,", depth, "and currentTurn", currentTurn, "are:-")
        # print(logic.generateAllMoves(board, currentTurn))
        for move in moves:
            constants = deepcopy(logic.fetchConstants())
            # logic.printConstants()    
            piece = board[move[0]]
            # print("Board Stats before making move:", move, piece, "depth: ", depth)
            # printStats(board)
            capture, flag = logic.makeMove(board, move)



            # print("\nBoard Stats after making move:", move, piece, "depth: ", depth)
            # printStats(board)
            val = TRANSPOSITION_TABLE[misc.genZobrist(board)]
            if val == 0.1:
                val = computerMakeMove(board, depth-1, (not currentTurn), og_depth, alpha, beta)
                TRANSPOSITION_TABLE[misc.genZobrist(board)] = val
            if val > bestEval:
                bestMove = move
                bestEval = val
            logic.unmakeMove(board, move, capture, flag)
            logic.restoreConstants(constants)
            alpha = max(alpha, val)
            if beta<=alpha:
                break
            # print("\nBoard Stats after unmaking move:", move, piece, "depth: ", depth)
            # printStats(board)
    else:
        bestEval = 100000
        # print("the moves calculated for depth:,", depth, "and currentTurn", currentTurn, "are:-")
        # print(logic.generateAllMoves(board, currentTurn))
        for move in moves:
            constants = deepcopy(logic.fetchConstants())
            piece = board[move[0]]
            # print("Board Stats before making move:", move, piece, "depth: ", depth)
            # printStats(board)
            capture, flag = logic.makeMove(board, move)
            # print("\nBoard Stats after making move:", move, piece, "depth: ", depth)
            # printStats(board)
            val = TRANSPOSITION_TABLE[misc.genZobrist(board)]
            if val == 0.1:
                val = computerMakeMove(board, depth-1, (not currentTurn), og_depth, alpha, beta)
                TRANSPOSITION_TABLE[misc.genZobrist(board)] = val
            #     print(move, val)
            if depth == og_depth:
                val+=eval.kingCheckmateValue(board, currentTurn, logic.whiteKingLocation, logic.blackKingLocation, logic.whitePiecesLocation, logic.blackPiecesLocation)
            if val < bestEval:
                bestMove = move
                bestEval = val
            logic.unmakeMove(board, move, capture, flag)
            logic.restoreConstants(constants)
            beta = min(beta, val)
            if beta<=alpha:
                break
            # print("\nBoard Stats after unmaking move:", move, piece, "depth: ", depth)
            # printStats(board)
    if (depth == og_depth):
        return bestMove, bestEval
    else:
        return bestEval


def searchCaptures(board, alpha, beta, currentTurn): # might include checks in here
    captureMoves = list()
    moves = eval.MoveOrder(board, logic.generateCaptureMoves(board, currentTurn), currentTurn, logic.blackAttackSquares, logic.whiteAttackSquares)
    if not moves:
        return eval.evaluateBoard(board)
    if currentTurn:
        for move in moves:
            bestEval = -100000
            constants = deepcopy(logic.fetchConstants())
            capture, flag = logic.makeMove(board, move)
            val = searchCaptures(board, alpha, beta, (not currentTurn))
            if val>bestEval:
                bestEval = val
            logic.unmakeMove(board, move, capture, flag)
            logic.restoreConstants(constants)
            alpha = max(alpha, val)
            if beta<=alpha:
                break
    else:
        for move in moves:
            bestEval = 100000
            constants = deepcopy(logic.fetchConstants())
            capture, flag = logic.makeMove(board, move)
            val = searchCaptures(board, alpha, beta, (not currentTurn))
            if val<bestEval:
                bestEval = val
            logic.unmakeMove(board, move, capture, flag)
            logic.restoreConstants(constants)
            beta = min(beta, val)
            if beta<=alpha:
                break
    return bestEval
