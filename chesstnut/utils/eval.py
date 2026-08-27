
PawnValue = 100
KnightValue = 320
BishopValue = 330
RookValue = 500
QueenValue = 900
KingValue = 20000

def isBlankSquare(piece_code):
    if piece_code%7 == -1:
        return True
    else:
        return False
def isBlack(piece_code):
    if piece_code//7 == 0:
        return True
    else:
        return False
def isWhite(piece_code):
    if piece_code//7 == 1:
        return True
    else:
        return False

def isKing(piece_code):
    if piece_code%7 == 1:
        return True
    else:
        return False
def isQueen(piece_code):
    if piece_code%7 == 2:
        return True
    else:
        return False
def isRook(piece_code):
    if piece_code%7 == 3:
        return True
    else:
        return False
def isKnight(piece_code):
    if piece_code%7 == 4:
        return True
    else:
        return False
def isBishop(piece_code):
    if piece_code%7 == 5:
        return True
    else:
        return False
def isPawn(piece_code):
    if piece_code%7 == 6:
        return True
    else:
        return False

def getPieceValue(piece):
    if isKing(piece):
        return 20000
    elif isQueen(piece):
        return 900
    elif isRook(piece):
        return 500
    elif isKnight(piece):
        return 320
    elif isBishop(piece):
        return 330
    elif isPawn(piece):
        return 100
    

pawn_heatmap = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 40, 40,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]
pawn_heatmap_opponent = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 40, 40,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0, 0, 0, 0, 0, 0

]

knight_heatmap = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,   0,   0,   0,  -20, -40,
    -30,  0,   10,  15,  15,  10,  0,  -30,
    -30,  5,   15,  20,  20,  15,  5,  -30,
    -30,  0,   15,  20,  20,  15,  0,  -30,
    -30,  5,   10,  15,  15,  10,  5,  -30,
    -40, -20,  0,   5,   5,   0,  -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]
knight_heatmap_opponent = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-40,-50,-50,-40,-40,-50
]

bishop_heatmap = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishop_heatmap_opponent = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

rook_heatmap = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]
rook_heatmap_opponent = [
    0,  0,  0,  5,  5,  0,  0,  0,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

queen_heatmap = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,   0,  5,  5,  5,  5,  0, -5,
    0,    0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
queen_heatmap_opponent = [-20, -10, -10, -5, -5, -10, -10, -20, 
                          -10, 0, 5, 0, 0, 0, 0, -10, 
                          -10, 5, 5, 5, 5, 5, 0, -10, 
                          0, 0, 5, 5, 5, 5, 0, -5, 
                          -5, 0, 5, 5, 5, 5, 0, -5, 
                          -10, 0, 5, 5, 5, 5, 0, -10, 
                          -10, 0, 0, 0, 0, 0, 0, -10, 
                          -20, -10, -10, -5, -5, -10, -10, -20]

king_middlegame_heatmap = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20,  20,   0,   0,   0,   0,  20,  20,
    20,  30,  10,   0,   0,  10,  30,  20
]
king_middlegame_heatmap_opponent = [
    20,  30,  10,   0,   0,  10,  30,  20,
    20,  20,   0,   0,   0,   0,  20,  20,
   -10, -20, -20, -20, -20, -20, -20, -10,
   -20, -30, -30, -40, -40, -30, -30, -20,
   -30, -40, -40, -50, -50, -40, -40, -30,
   -30, -40, -40, -50, -50, -40, -40, -30,
   -30, -40, -40, -50, -50, -40, -40, -30,
   -30, -40, -40, -50, -50, -40, -40, -30
]

king_endgame_heatmap=[
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]
king_endgame_heatmap_opponent = [
    -50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]

def evaluateBoard(board):
    eval = 0
    for location in range(64):
        if isBlack(board[location]):
            black_piece = board[location]
            if isKing(black_piece):
                eval-=(KingValue+king_middlegame_heatmap_opponent[location])
            elif isQueen(black_piece):
                eval-=(QueenValue+queen_heatmap_opponent[location])
            elif isPawn(black_piece):
                eval-=(PawnValue+pawn_heatmap_opponent[location])
            elif isBishop(black_piece):
                eval-=(BishopValue+bishop_heatmap_opponent[location])
            elif isKnight(black_piece):
                eval-=(KnightValue+knight_heatmap_opponent[location])
            elif isRook(black_piece):
                eval-=(RookValue+rook_heatmap_opponent[location])
        elif isWhite(board[location]):
                white_piece = board[location]
                if isKing(white_piece):
                    eval+=(KingValue+king_middlegame_heatmap[location])
                elif isQueen(white_piece):
                    eval+=(QueenValue+queen_heatmap[location])
                elif isPawn(white_piece):
                    eval+=(PawnValue+pawn_heatmap[location])
                elif isBishop(white_piece):
                    eval+=(BishopValue+bishop_heatmap[location])
                elif isKnight(white_piece):
                    eval+=(KnightValue+knight_heatmap[location])
                elif isRook(white_piece):
                    eval+=(RookValue+rook_heatmap[location])
    return eval

def MoveOrder(board, moves, currentTurn, blackAttackSquares, whiteAttackSquares):
    if not moves:
        return moves
    moveScores = list()
    for move in moves:
        score = 0
        capture_piece = board[move[1]]
        clicked_piece = board[move[0]]
        if not isBlankSquare(capture_piece):
            score = 10*getPieceValue(capture_piece) - getPieceValue(clicked_piece)
        # promotion insertion
            
        if currentTurn:
            if move[1] in blackAttackSquares:
                score-=getPieceValue(clicked_piece)
        else:
            if move[1] in whiteAttackSquares:
                score-=getPieceValue(clicked_piece)
        moveScores.append(score)
    sorted_moves = [pair[0] for pair in sorted(list(zip(moves, moveScores)), key=lambda x: x[1], reverse=True)]
    return sorted_moves

def KingDistanceValue(currentTurn, whiteKing, blackKing):
    val = 0
    if currentTurn:
        myKing = whiteKing
        oppKing = blackKing
    else:
        myKing = blackKing
        oppKing = whiteKing
    
    kingsDistance = abs(myKing//8 - oppKing//8) + abs(myKing%8 - oppKing%8)
    val = 16 - kingsDistance
    return val

def endgameWeight(board, currentTurn, blackPiecesLocation, whitePiecesLocation):
    if currentTurn:
        val = 24000
        for piece in whitePiecesLocation:
            val-=getPieceValue(board[piece])
        val/=240
    else:
        val = 24000
        for piece in blackPiecesLocation:
            val-=getPieceValue(board[piece])
        val/=240
    return val
        

def kingCheckmateValue(board, currentTurn, whiteKing, blackKing, whitePiecesLocation, blackPiecesLocation):
    return KingDistanceValue(currentTurn, whiteKing, blackKing)*endgameWeight(board, currentTurn, blackPiecesLocation, whitePiecesLocation)