import sys
from pygame.locals import *
from src.extra import *
from typing import List, Tuple

FPS = 60  # frames per second, the general speed of the program
WINDOWWIDTH = 800  # size of window's width in pixels
GAPSIZE = 1  # size of gap between boxes in pixels
BOARDSIZE = 100

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWWIDTH))
fps_clock = pygame.time.Clock()

board = Board(BOARDSIZE, GAPSIZE, WINDOWWIDTH)

board.create_board()

moving = False
cur_col = "RED"

instruction = """

a: continuous drawing with RED
d: continuous drawing with BLUE
b: continuous drawing with BLACK (wall)
left click: draw 1 block with RED
right click: draw 1 block with BLUE

"""


def check_collision(event: pygame.event,
                    board: Board,
                    color: str = "RED") -> None:
    """
    Check if mouse event touches any cells and change that cell color
    :param event: pygame event
    :param board: board to play on
    :param color: color to draw on board
    :return:
    """
    rects = board.get_board2()
    for item in rects:
        if item.collidepoint(event.pos):
            item.set_color(color)


def color_all(board: Board, color: str):
    """
    Color all cells on board
    :param board: board to color
    :param color:
    :return:
    """
    board = board.get_board2()
    for b in board:
        b.set_color(color)


def get_bcoord(event: pygame.event, board: Board) -> Tuple[int, int]:
    """
    Get the board coordinate of a mouse event
    :param event: pygame event
    :param board:
    :return:
    """
    rects = board.get_board1()
    n = len(rects)
    for i in range(n):
        for j in range(n):
            if rects[i][j].collidepoint(event.pos):
                return i, j


def draw_board(surface: pygame.display, board: Board) -> None:
    """
    Draw the whole board on a surface
    :param surface: pygame display
    :param board:
    :return:
    """
    rects = board.get_board2()
    for item in rects:
        pygame.draw.rect(surface, item.get_color(), item)


# def check_surrounding(x: int, y: int, board: Board) -> int:
#     s = 0
#     if board.get_col(x - 1, y) == "WHITE":
#         s += 1
#     elif board.get_col(x + 1, y) == "WHITE":
#         s += 1
#     elif board.get_col(x, y - 1) == "WHITE":
#         s += 1
#     elif board.get_col(x, y + 1) == "WHITE":
#         s += 1
#     return s


# def create_maze(board):
#     """
#     Generate maze on board using randomized Prim algorithm
#     :param board:
#     :return:
#     """
#     color_all(board, "YELLOW")
#     paths = [[0 for i in board.size] for j in board.size]
#     sx, sy = board.random_cell("YELLOW", True)
#     paths[sx][sy] = "C"
#     board.change_cell_col(sx, sy, "WHITE")
#     board.mark_rects(board.get_neighbors(sx, sy, True), "BLACK")
#
#     while board.count_dist("BLACK") > 0:
#         rwx, rwy = board.random_cell("BLACK")
#
#         if 0 < rwy < board.size:
#             if board.get_col(rwx, rwy - 1) == "YELLOW" and board.get_col(rwx, rwy + 1) == "WHITE":
#                 if check_surrounding(rwx, rwy, board) < 2:
#                     board[rwx][rwy].color_str = "WHITE"
#             elif board.get_col(rwx, rwy - 1) == "WHITE" and board.get_col(rwx, rwy + 1) == "YELLOW":
#                 pass
#         if 0 < rwx < board.size:
#             if board.get_col(rwx - 1, rwy) == "YELLOW" and board.get_col(rwx + 1, rwy) == "WHITE":
#                 pass
#             elif board.get_col(rwx - 1, rwy) == "WHITE" and board.get_col(rwx + 1, rwy) == "YELLOW":
#                 pass

def dijstra(board: Board):
    

while True:
    DISPLAYSURF.fill(colors["NAVYBLUE"])
    draw_board(DISPLAYSURF, board)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            check_collision(event, board)
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            check_collision(event, board, "DARKBLUE")
        elif event.type == MOUSEMOTION and moving:
            check_collision(event, board, cur_col)
        elif event.type == KEYDOWN:
            if event.key == pygame.K_a:
                moving = not moving
                cur_col = "RED"
            elif event.key == pygame.K_d:
                moving = not moving
                cur_col = "DARKBLUE"
            elif event.key == pygame.K_r:
                board.reset_color()

    pygame.display.update()
    fps_clock.tick(FPS)
