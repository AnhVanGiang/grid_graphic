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
s: 
left click: draw 1 block with RED
right click: draw 1 block with BLUE

"""


def check_collision(event: pygame.event,
                    board: Board,
                    color: str = "RED",
                    coords: Tuple[int, int] = (0, 0)) -> None:
    """
    Check if mouse event touches any cells and change that cell color
    :param event: pygame event
    :param board: board to play on
    :param color: color to draw on board
    :param coords:
    :return:
    """
    x, y = coords
    if x + y == 0:
        board.get_rect(x, y).set_color(color)
    else:
        board.get_rect(*get_coord_click(event, board)).set_color(color)


def get_coord_click(event: pygame.event, board: Board) -> Tuple[int, int]:
    """
    Get board coordinate of click event
    :param event:
    :param board:
    :return:
    """
    for i in range(board.size):
        for j in range(board.size):
            if board.get_rect(i, j).collidepoint(event.pos):
                return i, j


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


def dijstra(board: Board, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    shortest = {start: (None, 0)}
    current = start
    visited = set()

    while current != end:
        pygame.event.get()
        visited.add(current)
        board.get_rect(*current).set_color("RED")
        neighbors = board.get_neighbors(*current, walls=True)
        weight_to_cur = shortest[current][1]

        for next_node in neighbors:
            weight = weight_to_cur + 1
            if next_node not in shortest:
                shortest[next_node] = (current, weight)
            else:
                current_lowest_weight = shortest[next_node][1]
                if current_lowest_weight > weight:
                    shortest[next_node] = (current, weight)
        next_dests = {node: shortest[node] for node in shortest if node not in visited}

        if not next_dests:
            board.reset_color()
            return [(0, 0)]
        current = min(next_dests, key=lambda k: next_dests[k][1])

        draw_board(DISPLAYSURF, board)
        pygame.display.update()

    path = []

    while current is not None:
        path.append(current)
        next_node = shortest[current][0]
        current = next_node

    path = path[::-1]

    board.reset_color()
    return path


def draw_slow(board: Board, paths: List[Tuple[int, int]]) -> None:
    for x, y in paths:
        board.get_rect(x, y).set_color("RED")
        draw_board(DISPLAYSURF, board)
        pygame.display.update()


keys = {
    pygame.K_a: "RED",
    pygame.K_d: "DARKBLUE",
    pygame.K_b: "BLACK",
}

start_end = []
paths = []

while True:
    DISPLAYSURF.fill(colors["NAVYBLUE"])
    draw_board(DISPLAYSURF, board)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            try:
                ev = get_coord_click(event, board)
                if ev is not None:
                    start_end.append(ev)
                check_collision(event, board, "RED", ev)
            except TypeError:
                continue
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            try:
                check_collision(event, board, "BLACK", event.pos)
            except TypeError:
                continue
        elif event.type == MOUSEMOTION and moving:
            try:
                check_collision(event, board, cur_col, event.pos)
            except TypeError:
                continue
        elif event.type == KEYDOWN:
            if event.key in keys:
                moving = not moving
                cur_col = keys[event.key]
            elif event.key == pygame.K_r:
                board.reset_color()
            elif event.key == pygame.K_s:
                paths = dijstra(board, start_end[0], start_end[1])
                draw_slow(board, paths)
    pygame.display.update()
    fps_clock.tick(FPS)
