import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Create the Pygame window
window_size = (300, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic Tac Toe")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# The board is represented by a 3x3 matrix
board = np.zeros((3, 3), dtype=np.uint8)

# Constants for player and AI
PLAYER = 1
AI = 2

# Function to initialize the board
def initializeBoard():
    board.fill(0)

# Function to print the board using Pygame
def printBoard():
    screen.fill(WHITE)

    symbols = {0: ' ', PLAYER: 'X', AI: 'O'}
    for i in range(3):
        for j in range(3):
            symbol = symbols[board[i][j]]
            font = pygame.font.Font(None, 80)
            text = font.render(symbol, True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (100*j+50, 100*i+80)
            screen.blit(text, text_rect)

        if i != 2:
            pygame.draw.line(screen, BLACK, (0, (i+1)*100), (300, (i+1)*100), 3)

    pygame.display.flip()
    pygame.time.wait(500)

# Function to check if the board is full
def isBoardFull():
    return np.all(board != 0)

# Function to check if there is a win
def checkWin(player):
    # Check rows
    for i in range(3):
        if np.all(board[i, :] == player):
            return True

    # Check columns
    for i in range(3):
        if np.all(board[:, i] == player):
            return True

    # Check diagonals
    if np.all(board.diagonal() == player) or np.all(np.fliplr(board).diagonal() == player):
        return True

    return False

# Function to get all possible moves
def getValidMoves():
    return np.argwhere(board == 0)

# Alpha-Beta algorithm
def alphaBeta(maximizingPlayer):
    if checkWin(PLAYER):
        return -1

    if checkWin(AI):
        return 1

    if isBoardFull():
        return 0

    if maximizingPlayer:
        maxEval = -np.inf

        moves = getValidMoves()
        for move in moves:
            row, col = move

            board[row][col] = AI
            eval = alphaBeta(False)
            board[row][col] = 0

            maxEval = max(maxEval, eval)

        return maxEval
    else:
        minEval = np.inf

        moves = getValidMoves()
        for move in moves:
            row, col = move

            board[row][col] = PLAYER
            eval = alphaBeta(True)
            board[row][col] = 0

            minEval = min(minEval, eval)

        return minEval

# Function to make AI move
def makeAIMove():
    maxEval = -np.inf
    bestMove = None

    moves = getValidMoves()
    for move in moves:
        row, col = move

        board[row][col] = AI
        eval = alphaBeta(False)
        board[row][col] = 0

        if eval > maxEval:
            maxEval = eval
            bestMove = move

    row, col = bestMove
    board[row][col] = AI

# Function to make player move
def makePlayerMove():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // 100
                row = mouse_pos[1] // 100

                if row >= 0 and row < 3 and col >= 0 and col < 3 and board[row][col] == 0:
                    board[row][col] = PLAYER
                    return

# Main function
def main():
    initializeBoard()

    while not isBoardFull() and not checkWin(PLAYER) and not checkWin(AI):
        printBoard()

        makePlayerMove()

        if isBoardFull() or checkWin(PLAYER) or checkWin(AI):
            break

        makeAIMove()

    printBoard()

    if checkWin(PLAYER):
        print("Congratulations! You won!")
    elif checkWin(AI):
        print("Sorry, you lost. AI won!")
    else:
        print("It's a draw!")

    pygame.time.wait(2000)
    pygame.quit()

if __name__ == '__main__':
    main()
