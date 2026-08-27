import pygame
import sys
import tkinter as tk
from utils import search
from utils import logic
from utils import graphics
from random import randint
from time import time
from copy import deepcopy
from utils import eval, misc
from collections import defaultdict
TRANSPOSITION_TABLE = defaultdict(lambda: 0.1)

# Constants

screen = pygame.display.set_mode((graphics.WIDTH, graphics.HEIGHT))
pygame.display.set_caption('Chess Board')
misc.initZobrist()
board = [-1]*64
# example_fen = '4QB2/1k6/1Np5/3p4/2p1PN2/2r1pP2/5P2/K2n3q w - - 0 1'
example_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# example_fen = '3qr2k/pbpp2pp/1p5N/3Q2b1/2P1P3/P7/1PP2PPP/R4RK1 w - - 0 1'
# example_fen = '8/8/8/8/8/8/8/5B2'
board = logic.readFen(example_fen)
# board[5] = logic.WhiteRook
# logic.displayGird(logic.whiteAttackSquares)
# board[9] = logic.WhitePawn


#def kingCheckmateValue(board, currentTurn, whiteKing, blackKing, whitePiecesLocation, blackPiecesLocation):
#    return eval.KingDistanceValue(currentTurn, whiteKing, blackKing)*eval.endgameWeight(board, currentTurn, blackPiecesLocation, whitePiecesLocation)

def mouseClickHandler(board, firstclick, index, prev_index):
    if firstclick:
        graphics.highlightSquare(board,index,screen)
        if board[index]//7 == currentTurn:
            for move in logic.legalMoves(board, index, currentTurn):
                if board[move[1]]//7 == (not currentTurn):
                    graphics.drawCaptureSquare(board, move[1], screen)
                else:
                    graphics.drawFreeSquares(board, move[1], screen)
    else:
        if board[index]//7 == currentTurn:
            mouseClickHandler(board, True, index, prev_index)
        else:
            if [prev_index, index] in logic.legalMoves(board, prev_index, currentTurn):
                logic.updateLastMove([prev_index, index])
                captured_piece, flag = logic.makeMove(board, [prev_index, index])
                graphics.generateBoard(board, screen)
                # castling constants handler
                if logic.isKing(board[index]):
                    logic.changeKingStatus(board[index])
                    if logic.isKing(board[index]) and ((index%8 -prev_index%8 == 2) or (index%8 -prev_index%8 == -2)):
                        if (index%8 - prev_index%8 == 2):
                            logic.changeRightRookStatus(board[index])
                        else:
                            logic.changeLeftRookStatus(board[index])
                        # logic.printConstants()

                #rook constant handler
                if logic.isRook(board[index]):
                    logic.changeRookStatus(board[index], prev_index)

                # rook capture handler  # can be written more efficiently
                if logic.isRook(captured_piece):
                    if currentTurn:
                        if not (logic.hasBlackLeftRookMoved and logic.hasBlackRightRookMoved):
                            if index//8 == (0+7*logic.OPP): # the captured rook is not the unmoved one
                                if index%8 == 0 and not logic.hasBlackLeftRookMoved:
                                    logic.changeLeftRookStatus(captured_piece)
                                elif index%8 == 7 and not logic.hasBlackRightRookMoved:
                                    logic.changeRightRookStatus(captured_piece)
                    else:
                        if not (logic.hasWhiteLeftRookMoved and logic.hasWhiteRightRookMoved):
                            if index//8 == ((7-7*logic.OPP)): # the captured rook is not the unmoved one
                                if index%8 == 0 and not logic.hasWhiteLeftRookMoved:
                                    logic.changeLeftRookStatus(captured_piece)
                                elif index%8 == 7 and not logic.hasWhiteRightRookMoved:
                                    logic.changeRightRookStatus(captured_piece)
                # printMyStafts(board, index, prev_index)
                if writeNow:
                    misc.write_to_file("ME: "+str(board[index]) +" --> "+ str([prev_index//8, prev_index%8])+"="+str([index//8, index%8])+"\n")
                
                if currentTurn:
                    return False
                else:
                    return True
            else:
                graphics.generateBoard(board, screen)
                if currentTurn:
                    return True
                else:
                    return False



graphics.generateBoard(board, screen)

running = True
currentTurn = True
firstclick = 1
prev_index = 0
firstclick = True
computer_depth = 4
starttime = time()
automatic = True
writeNow = (not automatic)
myMoves = misc.getMyMovesOld("30_12_2023_09_53_40.txt")
myMoveIndex = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not (currentTurn ^ logic.ME):
            if not automatic:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_pos = graphics.getSquareFromClick(pygame.mouse.get_pos())
                        row, col = clicked_pos
                        index = row*8+col
                        if firstclick:
                            if board[index]//7 != currentTurn:
                                continue
                            prev_index = index
                            mouseClickHandler(board, firstclick, index, prev_index)
                            firstclick = False
                            
                        else:
                            if board[index]//7 == currentTurn:
                                prev_index = index
                                mouseClickHandler(board, firstclick, index, prev_index)
                                continue
                            currentTurn = mouseClickHandler(board, firstclick, index, prev_index)
                            firstclick = True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        move = myMoves[myMoveIndex]
                        logic.makeMove(board, move)
                        graphics.generateBoard(board, screen)
                        myMoveIndex+=1
                        if myMoveIndex == len(myMoves):
                            automatic = False
                            print("Ran out of the archived moves. Switched to Manual Mode")
                            writeNow = False
                        if currentTurn:
                            currentTurn = False
                        else:
                            currentTurn = True
                    elif event.key == pygame.K_BACKSPACE:
                        print("THE CURRENT EVAL CALCULATED BY EVAUL FUNCTION IS:", eval.evaluateBoard(board)/100) 
                        logic.printConstants()  
                    elif event.key == pygame.K_TAB:
                        print("Switched to Manual mode")
                        automatic = False
                        writeNow = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_pos = graphics.getSquareFromClick(pygame.mouse.get_pos())
                        row, col = clicked_pos
                        index = row*8+col
                        if firstclick:
                            if board[index]//7 != currentTurn:
                                continue
                            prev_index = index
                            mouseClickHandler(board, firstclick, index, prev_index)
        else:
            depth = computer_depth
            starttime = time()
            # print("before computer move")
            # logic.displayGird(board)
            # logic.printConstants()
            computer = computerMakeMove(board, depth, currentTurn, depth, -10000, 10000)
            if isinstance(computer, int) == 1:
                if computer == 0:
                    graphics.show_winner(-1)
                else:
                    if currentTurn:
                        graphics.show_winner(0)
                    else:
                        graphics.show_winner(1)

            else:
                move, bestEval = computer
            if not move:
                print("NO MOVE DETECTED")
                if currentTurn:
                    if logic.isKingInCheck(logic.whiteKingLocation, currentTurn):
                        graphics.show_winner(0)
                    else:
                        graphics.show_winner(-1)
                else:
                    if logic.isKingInCheck(logic.blackKingLocation, currentTurn):
                        graphics.show_winner(1)
                    else:
                        graphics.show_winner(-1)
                break
                
            print(move,bestEval)
            logic.makeMove(board, move)
            logic.updateLastMove(move)
            graphics.generateBoard(board, screen)
            print("Time taken by computer:-", time()-starttime)
            if (bestEval > 500000) and (not logic.generateAllMoves(board, False)):
                graphics.show_winner(1)
                break
            elif (bestEval < -500000) and (not logic.generateAllMoves(board, True)):
                graphics.show_winner(0)
                break
            # printCompStats(board, move[1], move[0])
            if writeNow:
                misc.write_to_file("COMP: "+str(board[move[1]]) +" --> "+ str([(move[0]//8, move[0]%8), (move[1]//8, move[1]%8)])+"\n")
            if currentTurn:
                currentTurn = False
            else:
                currentTurn = True
    pygame.display.flip()

pygame.quit()
sys.exit()
