import pygame
from operator import add
import time
from copy import deepcopy
import tkinter as tk
# from logic import actualOffsets


WIDTH, HEIGHT = 512, 512
SQUARE_SIZE = WIDTH // 8  # Size of each square
WIDTH = 512
# Colors (Green and Ivory)
GREEN = (118, 150, 86)
LIGHT_GREEN = (173, 255, 47)
# LIGHT_GREEN = (144, 216, 141)
DARK_GREEN = (50, 80, 30)
# LIGHT_GREEN = (144, 216, 141)
IVORY = (255, 247, 228)
LIGHT_IVORY = (210, 255, 0)
# LIGHT_IVORY = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)

def isWhite(piece_code):
    if piece_code//7 == 1:
        return True
    else:
        return False
def isPawn(piece_code):
    if piece_code%7 == 6:
        return True
    else:
        return False
def isKing(piece_code):
    if piece_code%7 == 1:
        return True
    else:
        return False

def drawSquare(board, index, screen):
    row = index//8
    col = index%8
    color = IVORY if (row + col) % 2 == 0 else GREEN
    pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    piece_code = board[row*8+col]  # Reverse row iteration
    if piece_code != -1:
        # Construct the image path based on piece code (assuming filenames match piece codes)
        image_path = f'pieces_new/{piece_code}.png'
        try:
            piece_image = pygame.image.load(image_path)
            piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        except pygame.error as e:
            print(f"Error loading image '{image_path}': {e}")

def highlightSquare(board, index, screen):
    row = index//8
    col = index%8
    generateBoard(board, screen)
    color = LIGHT_IVORY if (row + col) % 2 == 0 else LIGHT_GREEN
    pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    piece_code = board[row*8+col]  # Reverse row iteration
    if piece_code != -1:
        # Construct the image path based on piece code (assuming filenames match piece codes)
        image_path = f'pieces_new/{piece_code}.png'
        try:
            piece_image = pygame.image.load(image_path)
            piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        except pygame.error as e:
            print(f"Error loading image '{image_path}': {e}")

def drawFreeSquares(board, index, screen):
    row = index//8
    col = index%8
    if (board[row*8+col]//7 == -1):
        base_color = IVORY if (row + col) % 2 == 0 else GREEN
        pygame.draw.rect(screen, base_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Calculate the center coordinates of the square
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        circle_radius = SQUARE_SIZE // 6  # Smaller radius for the circle
        darker_color = DARK_GREEN if base_color == GREEN else LIGHT_GREY
        
        pygame.draw.circle(screen, darker_color, (center_x, center_y), circle_radius)
        piece_code = board[row*8+col]  # Reverse row iteration
        if piece_code != -1:
            # Construct the image path based on piece code (assuming filenames match piece codes)
            image_path = f'pieces_new/{piece_code}.png'
            try:
                piece_image = pygame.image.load(image_path)
                piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            except pygame.error as e:
                print(f"Error loading image '{image_path}': {e}")

def drawCaptureSquare(board, index, screen):
    row, col = index//8, index%8
    base_color = IVORY if (row + col) % 2 == 0 else GREEN
    pygame.draw.rect(screen, base_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Calculate the center coordinates of the square
    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

    circle_radius = SQUARE_SIZE // 2.0 # Further increased radius for the hollow circle
    border_width = 5  # Increased width of the border for the hollow circle
    darker_color = DARK_GREEN if base_color == GREEN else LIGHT_GREY
    
    # Draw hollow circle
    pygame.draw.circle(screen, darker_color, (center_x, center_y), circle_radius, border_width)

    piece_code = board[row*8+col]  # Reverse row iteration
    if piece_code != -1:
        # Construct the image path based on piece code (assuming filenames match piece codes)
        image_path = f'pieces_new/{piece_code}.png'
        try:
            piece_image = pygame.image.load(image_path)
            piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        except pygame.error as e:
            print(f"Error loading image '{image_path}': {e}")

def generateBoard(board, screen):
    for row in range(8):
        for col in range(8):
            drawSquare(board, 8*row + col, screen)

def getSquareFromClick(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def displayGird(board):
    for row in range(8):
        for col in range(8):
            print(board[row*8+col], end = " ")
        print()

def show_winner(result):
    root = tk.Tk()
    
    if result == 0:
        label = tk.Label(root, text="BLACK WINGS BY CHECKMATE", font=("Arial", 18))
    elif result == 1:
        label = tk.Label(root, text="WHITE WINS BY CHECKMATE", font=("Arial", 18))
    else:
        label = tk.Label(root, text="DRAW BY STALEMATE", font=("Arial", 18))
    
    label.pack(padx=20, pady=20)
    root.mainloop()