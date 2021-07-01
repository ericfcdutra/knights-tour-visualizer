import pygame
import time

BG_COLOR = (50, 50, 50)
DARK_TILE_COLOR = (95, 120, 49)
LIGHT_TILE_COLOR = (223, 225, 196)
N = 6
SIZE = 110 + N * 100

knight = pygame.image.load('knight.png')
KNIGHT = pygame.transform.scale(knight, (45, 70))

X = 0
Y = 0
# Variable to keep track of each step of the tour
# This will allow us to visualize all the tour steps
track = 0

# All possible moves for a given position
moves_x = [1, 2, 2, 1, -1, -2, -2, -1]
moves_y = [-2, -1, 1, 2, 2, 1, -1, -2]

# DRAW FUNCTIONS
def drawKnight(win, x, y):
    win.blit(KNIGHT, (80 + 100 * x, 65 + 100 * y))
    pygame.display.update()

def deleteDrawing(win, x, y):
    if (x + y) % 2 == 0:
        pygame.draw.rect(win, LIGHT_TILE_COLOR, (50 + 100 * x, 50 + 100 * y, 100, 100))
    else:
        pygame.draw.rect(win, DARK_TILE_COLOR, (50 + 100 * x, 50 + 100 * y, 100, 100))
    pygame.display.update()


def drawTrack(win, x, y, i=0):
    font = pygame.font.SysFont('Arial Bold', 32)
    text = font.render(str(track - i), True, (255, 0, 0))
    win.blit(text, ((120 + 100 * x), (120 + 100 * y)))
    pygame.display.update()

def drawBoard(win, n):
    pygame.draw.rect(win, (0, 0, 0), (45, 45, (100 * n + 10), (100 * n + 10)), 5)

    for i in range(n):
        for j in range(n):
            if (i + j) % 2 == 0:
                pygame.draw.rect(win, LIGHT_TILE_COLOR, (50 + 100 * j, 50 + 100 * i, 100, 100))
            else:
                pygame.draw.rect(win, DARK_TILE_COLOR, (50 + 100 * j, 50 + 100 * i, 100, 100))
    pygame.display.update()

def drawPath(win, b):
    xi = X * 100 + 100
    yi = Y * 100 + 100
    PURPLE = (100, 40, 115)
    pygame.draw.circle(win, PURPLE, (xi, yi), 10)
    for i in range(0, track + 1):
        for sublist in b:
            if i in sublist:
                x = sublist.index(i)
                y = b.index(sublist)
                pygame.draw.line(win, PURPLE, (xi, yi), ((x * 100 + 100), (y * 100 + 100)), 6)
                pygame.draw.circle(win, PURPLE, ((x * 100 + 100), (y * 100 + 100)), 10)
                pygame.display.update()
                time.sleep(0.2)
                xi = x * 100 + 100
                yi = y * 100 + 100


# KNIGHT'S TOUR SOLVER
# Create nested list for the board
def createBoard(n):
    b = [[-1 for i in range (n)] for j in range (n)]
    return b
# Validates moves
def isValid(b, next_x, next_y):
    if ((next_x) >= 0 and (next_x) <= (N - 1)):
        if ((next_y) >= 0 and (next_y) <= (N - 1)):
            if ((b[next_y][next_x] == -1)):
                return (True)
            else:
                return (False)
        else:
            return (False)
    else:
        return (False)
# Recursive function to solve tour
def solveTour(board, pos_x, pos_y, win):
    if N <= 5:
        time.sleep(0.05)

    global track
    # Base Case: all cells visited, no more -1
    if not (any(-1 in sublist for sublist in board)):
        return (True)

    prev_x = pos_x
    prev_y = pos_y

    track = track + 1

    for i in range(8):
        next_x = pos_x + moves_x[i]
        next_y = pos_y + moves_y[i]
        if isValid(board, next_x, next_y):
            board[next_y][next_x] = track
            deleteDrawing(win, prev_x, prev_y)
            drawTrack(win, prev_x, prev_y, 1)
            drawKnight(win, next_x, next_y)
            drawTrack(win, next_x, next_y)
            if solveTour(board, next_x, next_y, win):
                return (True)
    track = track - 1
    board[prev_y][prev_x] = -1
    deleteDrawing(win, prev_x, prev_y)

    return (False)

def main():
    pygame.init()
    WIN = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Knight's Tour Visualizer")
    WIN.fill(BG_COLOR)

    board = createBoard(N)
    board[Y][X] = track
    drawBoard(WIN, N)
    drawTrack(WIN, X, Y)
    drawKnight(WIN, X, Y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYUP:
                solveTour(board, X, Y, WIN)
                drawPath(WIN, board)
if __name__ == '__main__':
    main()