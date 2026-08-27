
ME = 1
if ME:
    OPP = 0
else:
    OPP = 1

currentTurn = True

lastMove = list()
blackKingLocation = -1
whiteKingLocation = -1
blackPiecesLocation = list()
whitePiecesLocation = list()
whiteAttackSquares = [0]*64
blackAttackSquares = [0]*64
BlackKing = 1
WhiteKing = 7
BlackQueen = 2
WhiteQueen = 9
BlackRook = 3
WhiteRook = 10
BlackKnight = 4
WhiteKnight = 11
BlackBishop = 5
WhiteBishop = 12
BlackPawn = 6
WhitePawn = 13

hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved = False, False, False, False, False, False

def fetchConstants():
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved, blackPiecesLocation, whitePiecesLocation, blackAttackSquares, whiteAttackSquares, blackKingLocation, whiteKingLocation
    return [hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved, blackPiecesLocation, whitePiecesLocation, blackAttackSquares, whiteAttackSquares, blackKingLocation, whiteKingLocation]
def restoreConstants(constants):
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved, blackPiecesLocation, whitePiecesLocation, blackAttackSquares, whiteAttackSquares, blackKingLocation, whiteKingLocation
    hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved, blackPiecesLocation, whitePiecesLocation, blackAttackSquares, whiteAttackSquares, blackKingLocation, whiteKingLocation = constants[0], constants[1], constants[2], constants[3], constants[4], constants[5], constants[6], constants[7], constants[8], constants[9], constants[10], constants[11]
def printConstants():
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved, blackPiecesLocation, whitePiecesLocation, blackAttackSquares, whiteAttackSquares, blackKingLocation, whiteKingLocation
    print(hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved)
    print("black pieces:-", blackPiecesLocation)
    print("white pieces:-", whitePiecesLocation)
    print("black attack squares:- ", displayGird(blackAttackSquares))
    print("white attack squares:- ", displayGird(whiteAttackSquares))
    print("black king location:- ", blackKingLocation)
    print("white king location:- ", whiteKingLocation)
def updateLastMove(move):
    global lastMove
    lastMove = move

def changeKingStatus(piece_code):
    global hasWhiteKingMoved, hasBlackKingMoved
    if isWhite(piece_code):
        hasWhiteKingMoved = True
    else:
        hasBlackKingMoved = True
def changeRightRookStatus(piece_code):
    global hasWhiteRightRookMoved, hasBlackRightRookMoved
    if isWhite(piece_code):
        hasWhiteRightRookMoved = True
    else:
        hasBlackRightRookMoved = True
def changeLeftRookStatus(piece_code):
    global hasWhiteLeftRookMoved, hasBlackLeftRookMoved
    if isWhite(piece_code):
        hasWhiteLeftRookMoved = True
    else:
        hasBlackLeftRookMoved = True
def changeRookStatus(piece_code, prev_index):
    global hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
    if isWhite(piece_code):
        if prev_index%8 == 0 and not hasWhiteLeftRookMoved:
            hasWhiteLeftRookMoved = True
        elif not hasWhiteRightRookMoved:
            hasWhiteRightRookMoved = True
    else:
        if prev_index%8 == 0 and not hasBlackLeftRookMoved:
            hasBlackLeftRookMoved = True
        elif not hasBlackRightRookMoved:
            hasBlackRightRookMoved = True 

# def restoreConstants(whiteKing, blackKing, whiteLR, blackLR, whiteRR, blackRR):
#     global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
#     hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved = whiteKing, blackKing, whiteLR, blackLR, whiteRR, blackRR

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



def isSlidingPiece(piece_code):
    if isBishop(piece_code) or isQueen(piece_code) or isRook(piece_code):
        return True
    else:
        return False

def isKingInCheck(index, currentTurn):
    if currentTurn:
        if blackAttackSquares[index] != 0:
            return True
        else:
            return False
    else:
        if whiteAttackSquares[index] != 0:
            return True
        else:
            return False

def squareWithinBounds(index, direction):
    row_add, col_add = actualOffsets[direction]
    row, col = index//8+row_add, index%8+col_add
    if (row > 7) or (row < 0):
        return False
    else:
        if (col > 7) or (col < 0):
            return False
        else:
            return True

#def readFen(fen):
    global blackAttackSquares, whiteAttackSquares, blackKingLocation, whiteKingLocation
    piece_codes = {
        '1': -1,
        'k': 1,  # black king
        'q': 2,  # black queen
        'r': 3,  # black rook
        'n': 4,  # black knight
        'b': 5,  # black bishop
        'p': 6,  # black pawn
        'K': 8,  # white king
        'Q': 9,  # white queen
        'R': 10, # white rook
        'N': 11, # white knight
        'B': 12, # white bishop
        'P': 13  # white pawn
    }
    board = [-1]*64  # Initialize the chessboard with zeros
    fen = fen.split(' ')[0]  # Remove additional FEN information after the board position

    col_index = 0  # Start from index 0 to properly populate the board
    row_index = 0
    for char in fen:
        if char.isdigit():
            row_index += int(char)
        elif char == '/':
            col_index += 1
            row_index = 0
        elif char in piece_codes:
            piece_code = piece_codes[char]
            board[col_index*8+row_index] = piece_code
            if isBlack(piece_code):
                if isKing(piece_code):
                    blackKingLocation = col_index*8+row_index
                blackPiecesLocation.append(col_index*8+row_index)
            else:
                whitePiecesLocation.append(col_index*8+row_index)
                if isKing(piece_code):
                    whiteKingLocation = col_index*8+row_index
            row_index += 1
        else:
            continue  # Ignore unexpected characters
    
    # for move in generateAttackSquares(board, 0):
    #     blackAttackSquares[move[1]]+=1
    # for move in generateAttackSquares(board, 1):
    #     whiteAttackSquares[move[1]]+=1
    for black in blackPiecesLocation:
        updateAttackSquares(board, black)
    for white in whitePiecesLocation:
        updateAttackSquares(board, white)
    if (not ME):
        board = board[::-1]
    return board

def readFen(fen):
    global blackAttackSquares, whiteAttackSquares
    global blackKingLocation, whiteKingLocation
    global blackPiecesLocation, whitePiecesLocation
    global hasWhiteKingMoved, hasBlackKingMoved
    global hasWhiteLeftRookMoved, hasBlackLeftRookMoved
    global hasWhiteRightRookMoved, hasBlackRightRookMoved

    # ============================================================
    # RESET ALL POSITION STATE
    # ============================================================

    blackPiecesLocation = []
    whitePiecesLocation = []

    blackAttackSquares = [0] * 64
    whiteAttackSquares = [0] * 64

    blackKingLocation = -1
    whiteKingLocation = -1

    hasWhiteKingMoved = False
    hasBlackKingMoved = False

    hasWhiteLeftRookMoved = False
    hasBlackLeftRookMoved = False

    hasWhiteRightRookMoved = False
    hasBlackRightRookMoved = False

    # ============================================================
    # PIECE ENCODING
    # ============================================================

    piece_codes = {
        'k': 1,   # black king
        'q': 2,   # black queen
        'r': 3,   # black rook
        'n': 4,   # black knight
        'b': 5,   # black bishop
        'p': 6,   # black pawn

        'K': 8,   # white king
        'Q': 9,   # white queen
        'R': 10,  # white rook
        'N': 11,  # white knight
        'B': 12,  # white bishop
        'P': 13   # white pawn
    }

    # ============================================================
    # SPLIT FEN
    # ============================================================

    fen_parts = fen.split()

    board_fen = fen_parts[0]

    # FEN fields:
    # 0 = board
    # 1 = side to move
    # 2 = castling rights
    # 3 = en passant
    # 4 = halfmove clock
    # 5 = fullmove number

    castling_rights = fen_parts[2] if len(fen_parts) > 2 else "-"

    # ============================================================
    # CREATE BOARD
    # ============================================================

    board = [-1] * 64

    row_index = 0
    col_index = 0

    for char in board_fen:

        # Number means that many empty squares.
        if char.isdigit():
            row_index += int(char)

        # Move to next rank.
        elif char == '/':
            col_index += 1
            row_index = 0

        # Piece.
        elif char in piece_codes:
            piece_code = piece_codes[char]

            location = col_index * 8 + row_index

            board[location] = piece_code

            if isBlack(piece_code):

                blackPiecesLocation.append(location)

                if isKing(piece_code):
                    blackKingLocation = location

            elif isWhite(piece_code):

                whitePiecesLocation.append(location)

                if isKing(piece_code):
                    whiteKingLocation = location

            row_index += 1

        else:
            continue

    # ============================================================
    # PARSE CASTLING RIGHTS
    # ============================================================
    #
    # White:
    #   K = white can castle kingside
    #   Q = white can castle queenside
    #
    # Black:
    #   k = black can castle kingside
    #   q = black can castle queenside
    #
    # Your engine represents the absence of these rights using
    # the "has moved" flags.
    # ============================================================

    hasWhiteKingMoved = not ('K' in castling_rights or 'Q' in castling_rights)
    hasBlackKingMoved = not ('k' in castling_rights or 'q' in castling_rights)

    hasWhiteLeftRookMoved = 'Q' not in castling_rights
    hasWhiteRightRookMoved = 'K' not in castling_rights

    hasBlackLeftRookMoved = 'q' not in castling_rights
    hasBlackRightRookMoved = 'k' not in castling_rights

    # ============================================================
    # REBUILD ATTACK MAPS
    # ============================================================

    for black in blackPiecesLocation:
        updateAttackSquares(board, black)

    for white in whitePiecesLocation:
        updateAttackSquares(board, white)

    # ============================================================
    # IMPORTANT:
    #
    # DO NOT reverse the board here.
    #
    # FEN already uses:
    #
    # index 0  -> a8
    # index 4  -> e8 (black king)
    # index 60 -> e1 (white king)
    #
    # Reversing board here would move the pieces while leaving
    # their locations inconsistent unless every location variable
    # were also transformed.
    # ============================================================

    return board

DirectionOffsets = [-8, 8, -1, 1, 7, -7, 9, -9]
numSquaresToEdge = []
for i in range(64):
    numSquaresToEdge.append(list())
for row in range(8):
    for col in range(8):
        numNorth = row
        numSouth = 7-row
        numWest = col
        numEast = 7 - col
        numSquaresToEdge[row*8+col] = [
            numNorth,
            numSouth,
            numWest,
            numEast,
            min(numSouth, numWest),
            min(numNorth, numEast),
            min(numSouth, numEast),
            min(numNorth, numWest)
        ]

actualOffsets = {
    -17: (-2, -1),
    -10: (-1, -2),
    6: (1, -2),
    15: (2, -1),
    -15: (-2, 1),
    -6: (-1, 2),
    10: (1, 2),
    17: (2, 1),
    7: (1,-1),
    9: (1, 1),
    -7: (-1, 1),
    -9: (-1, -1),
    -1: (0, -1),
    1: (0, 1),
    8: (1, 0),
    -8: (-1, 0)
}

def legalMoves(board, index, currentTurn):
    KingChecked = False
    if currentTurn: 
        if isKingInCheck(whiteKingLocation, currentTurn): # redundant color specification
            KingChecked = True
        king_index = whiteKingLocation
    else:
        if isKingInCheck(blackKingLocation, currentTurn):
            KingChecked = True
        king_index = blackKingLocation
    PinnedPieces, PinnedMoves = KingPinHandler(board, king_index, currentTurn) # 
    PinnedPieces = set(PinnedPieces)
    piece = board[index]
    if not KingChecked:
        if (piece)//7 == currentTurn:
            if index in PinnedPieces:
                moves = list()
                for PMove in PinnedMoves:
                    if PMove[0] == index:
                        moves.append(PMove)
                return moves
            if isSlidingPiece(piece):
                return (generateSlidingMoves(board, index, currentTurn))
            if isKnight(piece):
                return (generateKnightMoves(board, index, currentTurn))
            if isPawn(piece):
                return (generatePawnMoves(board, index, currentTurn))
            if isKing(piece):
                return (generateKingMoves(board, index, currentTurn))
    else:
        allMovesList = list()
        attackingSquares, doubleCheck = AttackSquaresFinderDuringCheck(board, king_index, currentTurn) # is being called everytimem, needs to be optimised
        if doubleCheck == 2:
            if isKing(piece):
                allMovesList+=(generateKingMovesInCheck(board, index, currentTurn))
            return allMovesList
        if index not in PinnedPieces:
            piece = board[index]
            if (piece)//7 == currentTurn:
                if isSlidingPiece(piece):
                    allMovesList+=(generateSlidingMovesInCheck(board, index, currentTurn, attackingSquares))
                if isKnight(piece):
                    allMovesList+=(generateKnightMovesInCheck(board, index, currentTurn, attackingSquares))
                if isPawn(piece):
                    allMovesList+=(generatePawnMovesInCheck(board, index, currentTurn, attackingSquares))
                if isKing(piece):
                    allMovesList+=(generateKingMovesInCheck(board, index, currentTurn))
        return allMovesList

def generateAttackSquares(board, currentTurn):
    allMovesList = list()
    for startSquare in range(64):
        piece = board[startSquare]
        if (piece)//7 == currentTurn:
            if isSlidingPiece(piece):
                allMovesList+=(generateSlidingMoves(board, startSquare, currentTurn))
            if isKnight(piece):
                allMovesList+=(generateKnightMoves(board, startSquare, currentTurn))
            if isPawn(piece):
                allMovesList+=(pawnAttackSquares(board, startSquare, currentTurn))
            if isKing(piece):
                allMovesList+=(generateKingMoves(board, startSquare, currentTurn))
    return allMovesList

def generateAllMoves(board, currentTurn):
    KingChecked = False
    if currentTurn: 
        if isKingInCheck(whiteKingLocation, currentTurn):
            KingChecked = True
        index = whiteKingLocation
    else:
        if isKingInCheck(blackKingLocation, currentTurn):
            KingChecked = True
        index = blackKingLocation
    PinnedPieces, PinnedMoves = (KingPinHandler(board, index, currentTurn))
    if not KingChecked:
        allMovesList = list()
        if currentTurn:
            for startSquare in whitePiecesLocation: # can optimise here
                if startSquare not in PinnedPieces:
                    piece = board[startSquare]
                    if (piece)//7 == currentTurn:
                        if isSlidingPiece(piece):
                            allMovesList+=(generateSlidingMoves(board, startSquare, currentTurn))
                        if isKnight(piece):
                            allMovesList+=(generateKnightMoves(board, startSquare, currentTurn))
                        if isPawn(piece):
                            allMovesList+=(generatePawnMoves(board, startSquare, currentTurn))
                        if isKing(piece):
                            allMovesList+=(generateKingMoves(board, startSquare, currentTurn))
                else:
                    for PMove in PinnedMoves:
                        if PMove[0] == startSquare:
                            allMovesList.append(PMove)
            return allMovesList
        else:   
            for startSquare in blackPiecesLocation: # can optimise here
                if startSquare not in PinnedPieces:
                    piece = board[startSquare]
                    if (piece)//7 == currentTurn:
                        if isSlidingPiece(piece):
                            allMovesList+=(generateSlidingMoves(board, startSquare, currentTurn))
                        if isKnight(piece):
                            allMovesList+=(generateKnightMoves(board, startSquare, currentTurn))
                        if isPawn(piece):
                            allMovesList+=(generatePawnMoves(board, startSquare, currentTurn))
                        if isKing(piece):
                            allMovesList+=(generateKingMoves(board, startSquare, currentTurn))
                else:
                    for PMove in PinnedMoves:
                        if PMove[0] == startSquare:
                            allMovesList.append(PMove)
            return allMovesList
    else:
        return KingCheckHandler(index, board, currentTurn)

def generateKingMovesInCheck(board, index, currentTurn):
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
    move_list = list()
    piece = board[index]
    for direction in DirectionOffsets:
        targetSquare = index+direction
        if squareWithinBounds(index, direction):
            if board[targetSquare]//7 == currentTurn:
                continue
            if not isKingInCheck(targetSquare, currentTurn):
                move_list.append([index, targetSquare])
    return move_list

def generateKingMoves(board, index, currentTurn):
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
    move_list = list()
    piece = board[index]
    for direction in DirectionOffsets:
        targetSquare = index+direction
        if squareWithinBounds(index, direction):
            if board[targetSquare]//7 == currentTurn:
                continue
            if not isKingInCheck(targetSquare, currentTurn):
                move_list.append([index, targetSquare])
    if ME:
        if isWhite(piece):
            if (not hasWhiteKingMoved):
                if (not hasWhiteLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        if (i != 3) and (isKingInCheck(ctr, True)):
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
                if (not hasWhiteRightRookMoved):
                    RightCastlingPossible = False
                    ctr = index+1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        if (isKingInCheck(ctr, True)):
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
        else:
            if (not hasBlackKingMoved):
                if (not hasBlackLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        if (i != 3) and (isKingInCheck(ctr, False)):
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
                if (not hasBlackRightRookMoved):
                    RightCastlingPossible = False
                    ctr = index+1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        if (isKingInCheck(ctr, False)):
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
    else:
        if isBlack(piece):
            if (not hasBlackKingMoved):
                if (not hasBlackRightRookMoved):
                    LeftCastlingPossible = False
                    ctr = index+1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        if (i != 3) and (isKingInCheck(ctr, False)):
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
                if (not hasBlackLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        if (isKingInCheck(ctr, False)):
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
        else:
            if (not hasWhiteKingMoved):
                if (not hasWhiteRightRookMoved):
                    LeftCastlingPossible = False
                    ctr = index+1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        if (i != 3) and (isKingInCheck(ctr, True)):
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
                if (not hasWhiteLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        if (isKingInCheck(ctr, True)):
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
    return move_list
def generateKnightMoves(board, index, currentTurn):
    move_list = list()
    knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
    for direction in knightDirections:
        targetSquare = index+direction
        if squareWithinBounds(index, direction):
            pieceOnTargetSquare = board[targetSquare]
            if (pieceOnTargetSquare//7 == currentTurn):
                continue
            else:
                move_list.append([index, targetSquare])
    return move_list
def generateSlidingMoves(board, index, currentTurn):
    move_list = list()
    piece = board[index]
    startIndex = (0+4*(isBishop(piece)))
    endIndex = (4+4*(not isRook(piece)))
    for directionIndex in range(startIndex, endIndex):
        for n in range(numSquaresToEdge[index][directionIndex]):
            targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
            pieceOnTargetSquare = board[targetSquare]
            if pieceOnTargetSquare//7 == currentTurn:
                break
            move_list.append([index, targetSquare])
            if (pieceOnTargetSquare)//7 == (not currentTurn):
                break
    return move_list
def generatePawnMoves(board, index, currentTurn):
    move_list = list()
    row, col = index//8, index%8
    piece = board[index]
    if ME:
        if isWhite(piece):
            directions = [-8, -16]
            if board[directions[0]+index]//7 == -1:
                move_list.append([index, directions[0]+index])
                if row == 6:
                    if board[directions[1]+index]//7 == -1:
                        move_list.append([index, directions[1]+index])
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        move_list.append([index, targetSquare])
                    
        else:
            directions = [8, 16]
            if board[directions[0]+index]//7 == -1:
                move_list.append([index, directions[0]+index])
                if row == 1:
                    if board[directions[1]+index]//7 == -1:
                        move_list.append([index, directions[1]+index])
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        move_list.append([index, targetSquare])
    else:
        if isBlack(piece):
            directions = [-8, -16]
            if board[directions[0]+index]//7 == -1:
                move_list.append([index, directions[0]+index])
                if row == 6:
                    if board[directions[1]+index]//7 == -1:
                        move_list.append([index, directions[1]+index])
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        move_list.append([index, targetSquare])
                
        else:
            directions = [8, 16]
            if board[directions[0]+index]//7 == -1:
                move_list.append([index, directions[0]+index])
                if row == 1:
                    if board[directions[1]+index]//7 == -1:
                        move_list.append([index, directions[1]+index])
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        move_list.append([index, targetSquare])
    return move_list
def pawnAttackSquares(board, index, currentTurn):
    move_list = list()
    row, col = index//8, index%8
    piece = board[index]
    if ME:
        if isWhite(piece):
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isWhite(board[targetSquare]):
                        move_list.append([index, targetSquare])
                    
        else:
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isBlack(board[targetSquare]):
                        move_list.append([index, targetSquare])
    else:
        if isBlack(piece):
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isBlack(board[targetSquare]):
                        move_list.append([index, targetSquare])
        else:
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isWhite(board[targetSquare]):
                        move_list.append([index, targetSquare])
    return move_list

def generateKnightMovesInCheck(board, index, currentTurn, AttackSquares):
    move_list = list()
    knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
    for direction in knightDirections:
        targetSquare = index+direction
        if squareWithinBounds(index, direction):
            pieceOnTargetSquare = board[targetSquare]
            if targetSquare not in AttackSquares:
                continue
            if (pieceOnTargetSquare//7 == currentTurn):
                continue
            else:
                move_list.append([index, targetSquare])
    return move_list
def generateSlidingMovesInCheck(board, index, currentTurn, AttackSquares):
    move_list = list()
    piece = board[index]
    startIndex = (0+4*(isBishop(piece)))
    endIndex = (4+4*(not isRook(piece)))
    for directionIndex in range(startIndex, endIndex):
        for n in range(numSquaresToEdge[index][directionIndex]):
            targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
            pieceOnTargetSquare = board[targetSquare]
            if pieceOnTargetSquare//7 == currentTurn:
                break
            if targetSquare in AttackSquares:
                move_list.append([index, targetSquare])
            if (pieceOnTargetSquare)//7 == (not currentTurn):
                break
    return move_list
def generatePawnMovesInCheck(board, index, currentTurn, AttackSquares):
    move_list = list()
    row, col = index//8, index%8
    piece = board[index]
    if ME:
        if isWhite(piece):
            directions = [-8, -16]
            if board[directions[0]+index]//7 == -1 and ((directions[0]+index) in AttackSquares):
                move_list.append([index, directions[0]+index])
            elif row == 6:
                if (board[directions[0]+index]//7 == -1) and (board[directions[1]+index]//7 == -1) and ((directions[1]+index) in AttackSquares):
                    move_list.append([index, directions[1]+index])
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if (board[targetSquare]//7 == (not currentTurn)) and (targetSquare in AttackSquares):
                        move_list.append([index, targetSquare])               
        else:
            directions = [8, 16]
            if (board[directions[0]+index]//7 == -1) and ((directions[0]+index in AttackSquares)):
                move_list.append([index, directions[0]+index])
            elif row == 1:
                if (board[directions[0]+index]//7 == -1) and (board[directions[1]+index]//7 == -1) and ((directions[1]+index in AttackSquares)):
                    move_list.append([index, directions[1]+index])
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        if targetSquare in AttackSquares:
                            move_list.append([index, targetSquare])
    else:
        if isBlack(piece):
            directions = [-8, -16]
            if (board[directions[0]+index]//7 == -1) and ((board[directions[0]+index]//7 in AttackSquares)):
                move_list.append([index, directions[0]+index])
            elif row == 6:
                if (board[directions[0]+index]//7 == -1) and (board[directions[1]+index]//7 == -1) and ((board[directions[1]+index]//7 in AttackSquares)):
                    move_list.append([index, directions[1]+index])
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        if targetSquare in AttackSquares:
                            move_list.append([index, targetSquare])
        else:
            directions = [8, 16]
            if (board[directions[0]+index]//7 == -1) and ((board[directions[0]+index]//7 in AttackSquares)):
                move_list.append([index, directions[0]+index])
            elif row == 1:
                if (board[directions[0]+index]//7 == -1) and (board[directions[1]+index]//7 == -1) and ((board[directions[1]+index]//7 in AttackSquares)):
                    move_list.append([index, directions[1]+index])
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == (not currentTurn):
                        if targetSquare in AttackSquares:
                            move_list.append([index, targetSquare])
    return move_list
def pawnAttackSquares(board, index, currentTurn):
    move_list = list()
    row, col = index//8, index%8
    piece = board[index]
    if ME:
        if isWhite(piece):
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isWhite(board[targetSquare]):
                        move_list.append([index, targetSquare])
                    
        else:
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isBlack(board[targetSquare]):
                        move_list.append([index, targetSquare])
    else:
        if isBlack(piece):
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isBlack(board[targetSquare]):
                        move_list.append([index, targetSquare])
        else:
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if not isWhite(board[targetSquare]):
                        move_list.append([index, targetSquare])
    return move_list

def AttackSquaresFinderDuringCheck(board, index, currentTurn):
    if ME:
        if currentTurn:
            attackingSquares = set()
            doubleCheck = 0
            knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
            for direction in knightDirections: # KNIGHT CHECK DETECTOR
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    pieceOnTargetSquare = board[targetSquare]
                    if isKnight(pieceOnTargetSquare) and isBlack(pieceOnTargetSquare):
                        attackingSquares.add(targetSquare)
                        doubleCheck+=1
                        break
            pinnedPieceList = set()
            pinnedIndex = -1
            startCheckingIfPiecePinned = False
            for directionIndex in range(0, 8): # SLIDING PIECE CHECK DETECTOR + PINNED PIECE DETECTOR
                move_list = list()
                startCheckingIfPiecePinned = False
                pinnedIndex=-1
                for n in range(numSquaresToEdge[index][directionIndex]):
                    targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
                    pieceOnTargetSquare = board[targetSquare]
                    if pieceOnTargetSquare//7 == currentTurn:
                        if startCheckingIfPiecePinned == False:
                            startCheckingIfPiecePinned = True
                            pinnedIndex = targetSquare
                            continue
                        else:
                            startCheckingIfPiecePinned = False
                            break
                    if not startCheckingIfPiecePinned:
                        move_list.append(targetSquare)
                    if (pieceOnTargetSquare)//7 == (not currentTurn):
                        if directionIndex < 4:
                            if pieceOnTargetSquare == BlackQueen or pieceOnTargetSquare == BlackRook:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                                break
                            break
                        else:
                            if pieceOnTargetSquare == BlackQueen or pieceOnTargetSquare == BlackBishop:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                                break
                            break
            if doubleCheck!= 2: # PAWN CHECK DETECTOR
                directionsAttack = [-7, -9]
                for direction in directionsAttack:
                    targetSquare = index+direction
                    if squareWithinBounds(index, direction):
                        if (board[targetSquare] == BlackPawn):
                            attackingSquares.add(targetSquare)
                            break
        else:
            attackingSquares = set()
            doubleCheck = 0
            knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
            for direction in knightDirections: # KNIGHT CHECK DETECTOR
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    pieceOnTargetSquare = board[targetSquare]
                    if isKnight(pieceOnTargetSquare) and isWhite(pieceOnTargetSquare):
                        attackingSquares.add(targetSquare)
                        doubleCheck+=1
                        break
            pinnedPieceList = set()
            pinnedIndex = -1
            startCheckingIfPiecePinned = False
            for directionIndex in range(0, 8): # SLIDING PIECE CHECK DETECTOR + PINNED PIECE DETECTOR
                move_list = list()
                startCheckingIfPiecePinned = False
                pinnedIndex=-1
                for n in range(numSquaresToEdge[index][directionIndex]):
                    targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
                    pieceOnTargetSquare = board[targetSquare]
                    if pieceOnTargetSquare//7 == currentTurn:
                        if startCheckingIfPiecePinned == False:
                            startCheckingIfPiecePinned = True
                            pinnedIndex = targetSquare
                            continue
                        else:
                            startCheckingIfPiecePinned = False
                            break
                    if not startCheckingIfPiecePinned:
                        move_list.append(targetSquare)
                    if (pieceOnTargetSquare)//7 == (not currentTurn):
                        if directionIndex < 4:
                            if pieceOnTargetSquare == WhiteQueen or pieceOnTargetSquare == WhiteRook:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                                break
                        else:
                            if pieceOnTargetSquare == WhiteQueen or pieceOnTargetSquare == WhiteBishop:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                                break
            if doubleCheck!= 2: # PAWN CHECK DETECTOR
                directionsAttack = [-7, -9]
                for direction in directionsAttack:
                    targetSquare = index+direction
                    if squareWithinBounds(index, direction):
                        if (board[targetSquare] == WhitePawn):
                            attackingSquares.add(targetSquare)
                            break
        return attackingSquares, doubleCheck

def KingCheckHandler(index, board, currentTurn):
    if ME:
        allMovesList = list()
        if currentTurn:
            attackingSquares = set()
            doubleCheck = 0
            knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
            for direction in knightDirections: # KNIGHT CHECK DETECTOR
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    pieceOnTargetSquare = board[targetSquare]
                    if isKnight(pieceOnTargetSquare) and isBlack(pieceOnTargetSquare):
                        attackingSquares.add(targetSquare)
                        doubleCheck+=1
                        break
            pinnedPieceList = set()
            for directionIndex in range(0, 8): # SLIDING PIECE CHECK DETECTOR + PINNED PIECE DETECTOR
                move_list = list()
                startCheckingIfPiecePinned = False
                pinnedIndex = -1
                for n in range(numSquaresToEdge[index][directionIndex]):
                    targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
                    pieceOnTargetSquare = board[targetSquare]
                    if pieceOnTargetSquare//7 == currentTurn:
                        if startCheckingIfPiecePinned == False:
                            startCheckingIfPiecePinned = True
                            pinnedIndex = targetSquare
                            continue
                        else:
                            startCheckingIfPiecePinned = False
                            break
                    if not startCheckingIfPiecePinned:
                        move_list.append(targetSquare)
                    if (pieceOnTargetSquare)//7 == (not currentTurn):
                        if directionIndex < 4:
                            if pieceOnTargetSquare == BlackQueen or pieceOnTargetSquare == BlackRook:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    if isQueen(board[pinnedIndex]) or isRook(board[pinnedIndex]):
                                        allMovesList.append([pinnedIndex, targetSquare])
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                            break
                        else:
                            if pieceOnTargetSquare == BlackQueen or pieceOnTargetSquare == BlackBishop:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    if isQueen(board[pinnedIndex]) or isRook(board[pinnedIndex]):
                                        allMovesList.append([pinnedIndex, targetSquare])
                                    if isPawn(board[pinnedIndex]) and ((pinnedIndex - 7 == targetSquare) or (pinnedIndex - 9 == targetSquare)):
                                        allMovesList.append([pinnedIndex, targetSquare])
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                            break
            if doubleCheck!= 2: # PAWN CHECK DETECTOR
                directionsAttack = [-7, -9] 
                for direction in directionsAttack:
                    targetSquare = index+direction
                    if squareWithinBounds(index, direction):
                        if (board[targetSquare] == BlackPawn):
                            attackingSquares.add(targetSquare)
                            break
            king_move_list = list()
            for direction in DirectionOffsets:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == currentTurn:
                        continue
                    if not isKingInCheck(targetSquare, currentTurn):
                        king_move_list.append([index, targetSquare])
            if doubleCheck == 2:
                return king_move_list
        else:
            attackingSquares = set()
            doubleCheck = 0
            knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
            for direction in knightDirections: # KNIGHT CHECK DETECTOR
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    pieceOnTargetSquare = board[targetSquare]
                    if isKnight(pieceOnTargetSquare) and isWhite(pieceOnTargetSquare):
                        attackingSquares.add(targetSquare)
                        doubleCheck+=1
                        break
            pinnedPieceList = set()
            pinnedIndex = -1
            startCheckingIfPiecePinned = False
            for directionIndex in range(0, 8): # SLIDING PIECE CHECK DETECTOR + PINNED PIECE DETECTOR
                move_list = list()
                startCheckingIfPiecePinned = False
                pinnedIndex = -1
                for n in range(numSquaresToEdge[index][directionIndex]):
                    targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
                    pieceOnTargetSquare = board[targetSquare]
                    if pieceOnTargetSquare//7 == currentTurn:
                        if startCheckingIfPiecePinned == False:
                            startCheckingIfPiecePinned = True
                            pinnedIndex = targetSquare
                            continue
                        else:
                            startCheckingIfPiecePinned = False
                            break
                    if not startCheckingIfPiecePinned:
                        move_list.append(targetSquare)
                    if (pieceOnTargetSquare)//7 == (not currentTurn):
                        if directionIndex < 4:
                            if pieceOnTargetSquare == WhiteQueen or pieceOnTargetSquare == WhiteRook:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    if isQueen(board[pinnedIndex]) or isRook(board[pinnedIndex]):
                                        allMovesList.append([pinnedIndex, targetSquare])
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                            break
                        else:
                            if pieceOnTargetSquare == WhiteQueen or pieceOnTargetSquare == WhiteBishop:
                                if startCheckingIfPiecePinned:
                                    startCheckingIfPiecePinned = False
                                    pinnedPieceList.add(pinnedIndex)
                                    if isQueen(board[pinnedIndex]) or isBishop(board[pinnedIndex]):
                                        allMovesList.append([pinnedIndex, targetSquare])
                                    if isPawn(board[pinnedIndex]) and ((pinnedIndex + 7 == targetSquare) or (pinnedIndex + 9 == targetSquare)):
                                        allMovesList.append([pinnedIndex, targetSquare])
                                    pinnedIndex = -1
                                else:
                                    doubleCheck+=1
                                    attackingSquares.update(move_list)
                            break
            if doubleCheck!= 2: # PAWN CHECK DETECTOR
                directionsAttack = [-7, -9]
                for direction in directionsAttack:
                    targetSquare = index+direction
                    if squareWithinBounds(index, direction):
                        if (board[targetSquare] == WhitePawn):
                            attackingSquares.add(targetSquare)
                            break
            king_move_list = list()
            for direction in DirectionOffsets: # KING MOVES
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    if board[targetSquare]//7 == currentTurn:
                        continue
                    if not isKingInCheck(targetSquare, currentTurn):
                        king_move_list.append([index, targetSquare])
            if doubleCheck == 2:
                return king_move_list
        
        if currentTurn:
            for startSquare in whitePiecesLocation:
                if startSquare not in pinnedPieceList:
                    piece = board[startSquare]
                    if isSlidingPiece(piece):
                        allMovesList+=(generateSlidingMovesInCheck(board, startSquare, currentTurn, attackingSquares))
                    if isKnight(piece):
                        allMovesList+=(generateKnightMovesInCheck(board, startSquare, currentTurn, attackingSquares))
                    if isPawn(piece):
                        allMovesList+=(generatePawnMovesInCheck(board, startSquare, currentTurn, attackingSquares))
            return allMovesList+king_move_list
        else:
            for startSquare in blackPiecesLocation:
                if startSquare not in pinnedPieceList:
                    piece = board[startSquare]
                    if isSlidingPiece(piece):
                        allMovesList+=(generateSlidingMovesInCheck(board, startSquare, currentTurn, attackingSquares))
                    if isKnight(piece):
                        allMovesList+=(generateKnightMovesInCheck(board, startSquare, currentTurn, attackingSquares))
                    if isPawn(piece):
                        allMovesList+=(generatePawnMovesInCheck(board, startSquare, currentTurn, attackingSquares))
                
            return allMovesList+king_move_list
        
def KingPinHandler(board, index, currentTurn):
    if currentTurn:
        pinnedPieceList = list()
        pinnedMoves = list()
        pinnedIndex = -1
        startCheckingIfPiecePinned = False
        for directionIndex in range(0, 8): # SLIDING PIECE CHECK DETECTOR + PINNED PIECE DETECTOR
            move_list = list()  
            startCheckingIfPiecePinned = False
            pinnedIndex = -1
            for n in range(numSquaresToEdge[index][directionIndex]):
                targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
                pieceOnTargetSquare = board[targetSquare]
                if pieceOnTargetSquare//7 == currentTurn:
                    if startCheckingIfPiecePinned == False:
                        startCheckingIfPiecePinned = True
                        pinnedIndex = targetSquare
                        continue
                    else:
                        startCheckingIfPiecePinned = False
                        break
                move_list.append(targetSquare)
                if (pieceOnTargetSquare)//7 == (not currentTurn):
                    if directionIndex < 4:
                        if pieceOnTargetSquare == BlackQueen or pieceOnTargetSquare == BlackRook:
                            if startCheckingIfPiecePinned:
                                startCheckingIfPiecePinned = False
                                pinnedPieceList.append(pinnedIndex)
                                if isQueen(board[pinnedIndex]) or isRook(board[pinnedIndex]):
                                    pinnedMoves.append([pinnedIndex, targetSquare])
                                pinnedIndex = -1
                        break
                    else:
                        if pieceOnTargetSquare == BlackQueen or pieceOnTargetSquare == BlackBishop:
                            if startCheckingIfPiecePinned:
                                startCheckingIfPiecePinned = False
                                pinnedPieceList.append(pinnedIndex)
                                if isQueen(board[pinnedIndex]) or isBishop(board[pinnedIndex]):
                                    pinnedMoves.append([pinnedIndex, targetSquare])
                                if isPawn(board[pinnedIndex]) and ((pinnedIndex - 7 == targetSquare) or (pinnedIndex - 9 == targetSquare)):
                                    pinnedMoves.append([pinnedIndex, targetSquare])
                                pinnedIndex = -1
                        break
    else:
        pinnedPieceList = list()
        pinnedMoves = list()
        pinnedIndex = -1
        startCheckingIfPiecePinned = False
        for directionIndex in range(0, 8): # SLIDING PIECE CHECK DETECTOR + PINNED PIECE DETECTOR
            move_list = list()
            startCheckingIfPiecePinned = False
            pinnedIndex = -1
            for n in range(numSquaresToEdge[index][directionIndex]):
                targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
                pieceOnTargetSquare = board[targetSquare]
                if pieceOnTargetSquare//7 == currentTurn:
                    if startCheckingIfPiecePinned == False:
                        startCheckingIfPiecePinned = True
                        pinnedIndex = targetSquare
                        continue
                    else:
                        startCheckingIfPiecePinned = False
                        break
                move_list.append(targetSquare)
                if (pieceOnTargetSquare)//7 == (not currentTurn):
                    if directionIndex < 4:
                        if pieceOnTargetSquare == WhiteQueen or pieceOnTargetSquare == WhiteRook:
                            if startCheckingIfPiecePinned:
                                startCheckingIfPiecePinned = False
                                pinnedPieceList.append(pinnedIndex)
                                if isQueen(board[pinnedIndex]) or isRook(board[pinnedIndex]):
                                    pinnedMoves.append([pinnedIndex, targetSquare])
                                pinnedIndex = -1
                        break
                    else:
                        if pieceOnTargetSquare == WhiteQueen or pieceOnTargetSquare == WhiteBishop:
                            if startCheckingIfPiecePinned:
                                startCheckingIfPiecePinned = False
                                pinnedPieceList.append(pinnedIndex)
                                if isQueen(board[pinnedIndex]) or isBishop(board[pinnedIndex]):
                                    pinnedMoves.append([pinnedIndex, targetSquare])
                                if isPawn(board[pinnedIndex]) and ((pinnedIndex + 7 == targetSquare) or (pinnedIndex + 9 == targetSquare)):
                                    pinnedMoves.append([pinnedIndex, targetSquare])
                                pinnedIndex = -1
                        break
    return pinnedPieceList, pinnedMoves


def pawnAttackSquares(board, index, currentTurn):
    move_list = list()
    row, col = index//8, index%8
    piece = board[index]
    if ME:
        if isWhite(piece):
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    move_list.append([index, targetSquare])
                    
        else:
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    move_list.append([index, targetSquare])
    else:
        if isBlack(piece):
            directionsAttack = [-7, -9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    move_list.append([index, targetSquare])
        else:
            directionsAttack = [7, 9]
            for direction in directionsAttack:
                targetSquare = index+direction
                if squareWithinBounds(index, direction):
                    move_list.append([index, targetSquare])
    return move_list
def generateKingMovesInAttack(board, index, currentTurn):
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
    move_list = list()
    piece = board[index]
    for direction in DirectionOffsets:
        targetSquare = index+direction
        if squareWithinBounds(index, direction):
            if not isKingInCheck(targetSquare, currentTurn):
                move_list.append([index, targetSquare])
    if ME:
        if isWhite(piece):
            if (not hasWhiteKingMoved):
                if (not hasWhiteLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
                if (not hasWhiteRightRookMoved):
                    RightCastlingPossible = False
                    ctr = index+1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
        else:
            if (not hasBlackKingMoved):
                if (not hasBlackLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
                if (not hasBlackRightRookMoved):
                    RightCastlingPossible = False
                    ctr = index+1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
    else:
        if isBlack(piece):
            if (not hasBlackKingMoved):
                if (not hasBlackRightRookMoved):
                    LeftCastlingPossible = False
                    ctr = index+1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
                if (not hasBlackLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
        else:
            if (not hasWhiteKingMoved):
                if (not hasWhiteRightRookMoved):
                    LeftCastlingPossible = False
                    ctr = index+1
                    for i in range(1,4):
                        if board[ctr]!= -1:
                            break
                        ctr+=1
                    else:
                        RightCastlingPossible = True
                    if RightCastlingPossible:
                        move_list.append([index, index+2])
                if (not hasWhiteLeftRookMoved):
                    LeftCastlingPossible = False
                    ctr = index-1
                    for i in range(5,7):
                        if board[ctr]!= -1:
                            break
                        ctr-=1
                    else:
                        LeftCastlingPossible = True
                    if LeftCastlingPossible:
                        move_list.append([index, index-2])
    return move_list
def generateKnightMovesInAttack(board, index, currentTurn):
    move_list = list()
    knightDirections = [-15, -17, 15, 17, 10, -6, -10, 6]
    for direction in knightDirections:
        targetSquare = index+direction
        if squareWithinBounds(index, direction):
            move_list.append([index, targetSquare])
                
    return move_list
def generateSlidingMovesInAttack(board, index, currentTurn):
    move_list = list()
    piece = board[index]
    startIndex = (0+4*(isBishop(piece)))
    endIndex = (4+4*(not isRook(piece)))
    for directionIndex in range(startIndex, endIndex):
        for n in range(numSquaresToEdge[index][directionIndex]):
            targetSquare = index + DirectionOffsets[directionIndex]*(n+1)
            pieceOnTargetSquare = board[targetSquare]
            move_list.append([index, targetSquare])
            if pieceOnTargetSquare//7 == currentTurn:
                break
            if ((pieceOnTargetSquare)//7 == (not currentTurn)) and (not isKing(pieceOnTargetSquare)):
                break
    return move_list
def removeAttackSquares(board, index):
    global blackAttackSquares, whiteAttackSquares
    piece =board[index]
    if isWhite(piece):
        if isSlidingPiece(piece):
            for move in generateSlidingMovesInAttack(board, index, 1):
                whiteAttackSquares[move[1]]-=1
        elif isKnight(piece):
            for move in generateKnightMovesInAttack(board, index, 1):
                whiteAttackSquares[move[1]]-=1
        elif isKing(piece):
            for move in generateKingMovesInAttack(board, index, 1):
                whiteAttackSquares[move[1]]-=1
        elif isPawn(piece):
            for move in pawnAttackSquares(board, index, 1):
                whiteAttackSquares[move[1]]-=1
    elif isBlack(piece):
        if isSlidingPiece(piece):
            for move in generateSlidingMovesInAttack(board, index, 0):
                blackAttackSquares[move[1]]-=1
        elif isKnight(piece):
            for move in generateKnightMovesInAttack(board, index, 0):
                blackAttackSquares[move[1]]-=1
        elif isKing(piece):
            for move in generateKingMovesInAttack(board, index, 0):
                blackAttackSquares[move[1]]-=1
        elif isPawn(piece):
            for move in pawnAttackSquares(board, index, 0):
                blackAttackSquares[move[1]]-=1
def updateAttackSquares(board, index):
    global blackAttackSquares, whiteAttackSquares
    piece =board[index]
    if isWhite(piece):
        if isSlidingPiece(piece):
            for move in generateSlidingMovesInAttack(board, index, 1):
                whiteAttackSquares[move[1]]+=1
        elif isKnight(piece):
            for move in generateKnightMovesInAttack(board, index, 1):
                whiteAttackSquares[move[1]]+=1
        elif isKing(piece):
            for move in generateKingMovesInAttack(board, index, 1):
                whiteAttackSquares[move[1]]+=1
        elif isPawn(piece):
            for move in pawnAttackSquares(board, index, 1):
                whiteAttackSquares[move[1]]+=1
    elif isBlack(piece):
        if isSlidingPiece(piece):
            for move in generateSlidingMovesInAttack(board, index, 0):
                blackAttackSquares[move[1]]+=1
        elif isKnight(piece):
            for move in generateKnightMovesInAttack(board, index, 0):
                blackAttackSquares[move[1]]+=1
        elif isKing(piece):
            for move in generateKingMovesInAttack(board, index, 0):
                blackAttackSquares[move[1]]+=1
        elif isPawn(piece):
            for move in pawnAttackSquares(board, index, 0):
                blackAttackSquares[move[1]]+=1

def removeSlidingAttackSquares(board):
    global whiteAttackSquares, blackAttackSquares
    for square in whitePiecesLocation:
        if isSlidingPiece(board[square]):
            removeAttackSquares(board, square) 
    for square in blackPiecesLocation:
        if isSlidingPiece(board[square]):
            removeAttackSquares(board, square) 
def addSlidingAttackSquares(board):
    global whiteAttackSquares, blackAttackSquares
    for square in whitePiecesLocation:
        if isSlidingPiece(board[square]):
            updateAttackSquares(board, square) 
    for square in blackPiecesLocation:
        if isSlidingPiece(board[square]):
            updateAttackSquares(board, square) 

def makeMove(board, move): # also return the piece captured
    global blackPiecesLocation, whitePiecesLocation, blackKingLocation, whiteKingLocation
    removeSlidingAttackSquares(board)
    if not isSlidingPiece(board[move[0]]):
        removeAttackSquares(board, move[0])
        
    if not isSlidingPiece(board[move[1]]): # the clicked pieces attack squares removed
        removeAttackSquares(board, move[1]) # the captured piece's attack squres removed
    flag = 0
    clicked_piece = board[move[0]]
    captured_piece = board[move[1]]
    board[move[1]] = clicked_piece
    board[move[0]] = -1
    piece = board[move[1]]

    #promotion handler
    if isPawn(piece) and ((move[1]//8 == 0) or (move[1]//8 == 7)):
        board[move[1]] = 7*(isWhite(piece))+2
        flag = 2
    if not isSlidingPiece(board[move[1]]):
        updateAttackSquares(board, move[1])  # the clicked piece's new attack squares updated
    #castling handler
    if isKing(piece):
        changeKingStatus(piece)
        if isWhite(piece):
            whiteKingLocation = move[1]
        elif isBlack(piece):
            blackKingLocation = move[1]
        if ((move[1]%8 - move[0]%8 == 2) or (move[1]%8 - move[0]%8 == -2)):
            if (move[1]%8 - move[0]%8 == 2): # right castling
                board[move[1]-1] = board[((move[1]//8)+1)*8 - 1]
                board[((move[1]//8)+1)*8 - 1] = -1
                updatePieceLocationMoved(board[move[1]-1], [((move[1]//8)+1)*8 - 1, move[1]-1])
                changeRightRookStatus(board[move[1]-1])

            else: # left castling
                board[move[1]+1] = board[((move[1]//8))*8]
                board[((move[1]//8))*8] = -1
                updatePieceLocationMoved(board[move[1]+1], [((move[1]//8))*8, move[1]+1])
                changeLeftRookStatus(board[move[1]+1])
            flag = 1

    if isRook(piece):
        changeRookStatus(piece, move[0])

    # rook capture handler  # can be written more efficiently
    if isRook(captured_piece):
        if currentTurn:
            if not (hasBlackLeftRookMoved and hasBlackRightRookMoved):
                if move[1]//8 == (0+7*OPP): # the captured rook is not the unmoved one
                    if move[1]%8 == 0 and not hasBlackLeftRookMoved:
                        changeLeftRookStatus(captured_piece)
                    elif move[1]%8 == 7 and not hasBlackRightRookMoved:
                        changeRightRookStatus(captured_piece)
        else:
            if not (hasWhiteLeftRookMoved and hasWhiteRightRookMoved):
                if move[1]//8 == ((7-7*OPP)): # the captured rook is not the unmoved one
                    if move[1]%8 == 0 and not hasWhiteLeftRookMoved:
                        changeLeftRookStatus(captured_piece)
                    elif move[1]%8 == 7 and not hasWhiteRightRookMoved:
                        changeRightRookStatus(captured_piece)
    updatePieceLocationMoved(piece, move)
    updatedPieceLocationCaptured(captured_piece, move)
    addSlidingAttackSquares(board)
    return captured_piece, flag
def unmakeMove(board, move, captured_piece, flag): # the move should be as it was made before and not like reverse the move or something
    if flag == 0:
        clicked_piece = board[move[1]]
        board[move[0]] = clicked_piece
        board[move[1]] = captured_piece
        restoreCapturePieceLocation(captured_piece, move)
        # restoreMovedPieceLocation(clicked_piece, move)
        # updatedPieceLocationCaptured(captured_piece, move)
            
    elif flag == 1:
        if (move[1]%8 - move[0]%8 == 2):
            clicked_piece = board[move[1]]
            board[move[0]] = clicked_piece
            board[move[1]] = captured_piece
            restoreCapturePieceLocation(captured_piece, move)
            # restoreMovedPieceLocation(clicked_piece, move)
            cancelRightCastelling(board, move)
            
        else:
            clicked_piece = board[move[1]]
            board[move[0]] = clicked_piece
            board[move[1]] = captured_piece
            # restoreMovedPieceLocation(clicked_piece, move)
            restoreCapturePieceLocation(captured_piece, move)
            cancelLeftCastelling(board, move)
    elif flag == 2:
        clicked_piece = board[move[1]]
        if isWhite(clicked_piece):
            board[move[0]] = WhitePawn
        else:
            board[move[0]] = BlackPawn
        board[move[1]] = captured_piece
        updatedPieceLocationCaptured(clicked_piece, [move[0], move[1]])

def cancelRightCastelling(board, move):
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
    if isWhite(board[move[1]]):
        hasWhiteKingMoved = False
        hasWhiteRightRookMoved = False
    else:
        hasBlackKingMoved = False
        hasBlackRightRookMoved = False
    board[((move[1]//8)+1)*8 - 1] = board[move[1]-1]
    board[move[1]-1] = -1
    updatePieceLocationMoved(board[move[1]-1], [move[1]-1, ((move[1]//8)+1)*8 - 1])
def cancelLeftCastelling(board, move):
    global hasWhiteKingMoved, hasBlackKingMoved, hasWhiteLeftRookMoved, hasBlackLeftRookMoved, hasWhiteRightRookMoved, hasBlackRightRookMoved
    if isWhite(board[move[1]]):
        hasWhiteKingMoved = False
        hasWhiteLeftRookMoved = False
    else:
        hasBlackKingMoved = False
        hasBlackLeftRookMoved = False
    board[((move[1]//8))*8] =  board[move[1]+1]
    board[move[1]+1] = -1
    updatePieceLocationMoved(board[move[1]+1], [move[1]+1, ((move[1]//8))*8])
def updatedPieceLocationCaptured(captured_piece,move):
    if isWhite(captured_piece):
        whitePiecesLocation.remove(move[1])
    elif isBlack(captured_piece):
        blackPiecesLocation.remove(move[1])
def updatePieceLocationMoved(piece, move):
    global whitePiecesLocation, blackPiecesLocation
    if isWhite(piece):
        whitePiecesLocation.remove(move[0])
        whitePiecesLocation.append(move[1])
    elif isBlack(piece):
        blackPiecesLocation.remove(move[0])
        blackPiecesLocation.append(move[1])
def restoreCapturePieceLocation(captured_piece, move):
    global whitePiecesLocation, blackPiecesLocation
    if isWhite(captured_piece):
        whitePiecesLocation.append(move[1])
    elif isBlack(captured_piece):
        blackPiecesLocation.append(move[1])
def restoreMovedPieceLocation(piece, move):
    global whitePiecesLocation, blackPiecesLocation
    if isWhite(piece):
        whitePiecesLocation.remove([move[1]])
        whitePiecesLocation.append(move[0])
    elif isBlack(piece):
        whitePiecesLocation.remove([move[1]])
        whitePiecesLocation.append(move[0])

def displayGird(board):
    for row in range(8):
        for col in range(8):
            piece = board[row*8+col]
            if piece == -1:
                print("", piece, end = " ")
            elif piece<10:
                print(" ", piece, end = " ")
            else:
                print("",piece, end = " ")
        print()

def printMyStats(board, index, prev_index):
    print("\n--------------------MADE MY MOVE ------------------------")
    print("piece_moved is: ", board[index])
    print("move played:", [prev_index, index])
    displayGird(board)
    print("constants status:, ")
    printConstants()
    print("----------------------------------------------------------")
def printCompStats(board, index, prev_index):
    print("\n--------------------COMPUTER MOVE ------------------------")
    print("piece_moved is: ", board[index])
    print("move played:", [prev_index, index])
    displayGird(board)
    print("constants status:, ")
    printConstants()
    print("----------------------------------------------------------")
def printStats(board):
    displayGird(board)
    printConstants()

def generateCaptureMoves(board, currentTurn):
    captureMoves = list()
    if currentTurn:
        for move in generateAllMoves(board, currentTurn):
            if move[1] in blackPiecesLocation:
                captureMoves.append(move)
    else:
        for move in generateAllMoves(board, currentTurn):
            if move[1] in whitePiecesLocation:
                captureMoves.append(move)