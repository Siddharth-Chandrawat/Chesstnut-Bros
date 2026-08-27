from datetime import datetime
import random


filename = ""
def write_to_file(text):
    global filename
    if not filename:
        filename =  "match_data/"+datetime.now().strftime("%d_%m_%Y")+"_"+datetime.now().strftime("%H_%M_%S")+".txt"
    try:
        with open(filename, 'a') as file:
            file.write(text)
        # print(f"Text has been written to {filename} successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
        
def getMyMovesOld(filename):
    with open("match_data/"+filename, 'r') as file:
        lines = file.readlines()
    myMoves = list()
    for line in lines:
        if line[:2] == "ME":
            startIndex = -1
            endIndex = -1
            line = line.split(" --> ")[1].split("=")
            startIndex = int(line[0][1])*8+int(line[0][4])
            endIndex = int(line[1][1])*8+int(line[1][4])
            myMoves.append([startIndex, endIndex])
    return myMoves


# Constants for piece codes
BlankSquare = -1
BlackKing = 1
WhiteKing = 8
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

def initZobrist():
    keys = {}
    for piece_code in [BlankSquare, BlackKing, WhiteKing, BlackQueen, WhiteQueen,
                       BlackRook, WhiteRook, BlackKnight, WhiteKnight,
                       BlackBishop, WhiteBishop, BlackPawn, WhitePawn]:
        keys[piece_code] = [random.getrandbits(64) for _ in range(64)]  # Generating 64 random 64-bit keys for each square
        
    return keys

zobrist_keys = initZobrist()

def genZobrist(board):
    hash_key = 0
    for i, piece in enumerate(board):
        if piece != BlankSquare:
            hash_key ^= zobrist_keys[piece][i]
    
    return hash_key