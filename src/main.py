#!/usr/bin/env python
# coding: utf-8
import sys
from pygame.locals import *
from extra import *
from typing import List, Tuple
import cv2
# from skimage.measure import block_reduce
import numpy as np
import pygame
from graph import Graph
import multiprocessing as mp
import threading
from life import Life

FPS = 60  # frames per second, the general speed of the program
WINDOWWIDTH = 800  # size of window's width in pixels
GAPSIZE = 1  # size of gap between boxes in pixels
BOARDSIZE = 100

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWWIDTH))
fps_clock = pygame.time.Clock()


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
                    color: Tuple[int, int, int] = COLORS["RED"],
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
    return event.pos[0] // (board.bsize + GAPSIZE), event.pos[1] // (board.bsize + GAPSIZE)


def color_all(board: Board, color: Tuple[int, int, int]):
    """
    Color all cells on board
    :param board: board to color
    :param color:
    :return:
    """
    board = board.get_board2()
    for b in board:
        b.set_color(color)


def draw_board(surface: pygame.display, rects: List[NRect]) -> None:
    """
    Draw the whole board on a surface
    :param rects:
    :param surface: pygame display
    :return:
    """
    for item in rects:
        pygame.draw.rect(surface, item.color, item)


def draw_slow(board: Board, paths: List[Tuple[int, int]], color: Tuple[int, int, int]) -> None:
    for x, y in paths:
        board.get_rect(x, y).set_color(color)
        # draw_board(DISPLAYSURF, board)
        pygame.display.update()


keys = {
    pygame.K_a: "RED",
    pygame.K_d: "DARKBLUE",
    pygame.K_b: "BLACK",
}


# def vid_cap(board: Board, surface: pygame.display):
#     downsample = (5, 8)
#     vc = cv2.VideoCapture(0)
#
#     if vc.isOpened():  # try to get the first frame
#         rval, frame = vc.read()
#     else:
#         rval = False
#
#     while rval:
#         pygame.event.get()
#         rval, frame = vc.read()
#         ds_array = frame / 255
#
#         r = block_reduce(ds_array[:, :, 0], downsample, np.mean)
#         g = block_reduce(ds_array[:, :, 1], downsample, np.mean)
#         b = block_reduce(ds_array[:, :, 2], downsample, np.mean)
#
#         ds_array = np.stack((r, g, b), axis=-1)
#
#         board.image_on_board(ds_array)
#
#         draw_board(surface, board)
#         pygame.display.update()


def main():
    pressed = False
    moving = False
    cur_col = COLORS["RED"]
    board = Board(BOARDSIZE, GAPSIZE, WINDOWWIDTH)
    board.create_board()
    rects = board.get_board2()
    graph = Graph(board)
    life = Life(board)
    c = 0
    proc = None
    DISPLAYSURF.fill(COLORS["NAVYBLUE"])
    while True:
        draw_board(DISPLAYSURF, rects)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_q):
                print("exited")
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and not pressed:
                try:
                    ev = get_coord_click(event, board)
                    if ev is not None:
                        graph.start_end[c] = ev
                        check_collision(event, board, COLORS["RED"], ev)
                        c = not c
                except TypeError:
                    continue
            elif event.type == MOUSEBUTTONDOWN and event.button == 3 and not pressed:
                try:
                    check_collision(event, board, COLORS["BLACK"], event.pos)
                except TypeError:
                    continue
            elif event.type == MOUSEMOTION and moving and event.buttons[0]:
                try:
                    check_collision(event, board, COLORS[cur_col], event.pos)
                except TypeError:
                    continue
            elif event.type == MOUSEMOTION and not moving and event.buttons[0]:
                try:
                    check_collision(event, board, COLORS["RED"], event.pos)
                except TypeError:
                    continue
            elif event.type == KEYDOWN:
                if event.key in keys:
                    moving = not moving
                    pressed = not pressed
                    cur_col = keys[event.key]
                elif event.key == pygame.K_r:
                    board.reset_color(eve=True)
                elif event.key == pygame.K_s:
                    t = threading.Thread(target=graph.dijstra, daemon=True)
                    t.start()
                elif event.key == pygame.K_t:
                    t = threading.Thread(target=graph.astar, daemon=True)
                    t.start()
                elif event.key == pygame.K_l:
                    t = threading.Thread(target=life.game, daemon=True)
                    t.start()
                # elif event.key == pygame.K_c:
                #     t = threading.Thread(target=vid_cap, args=(board, DISPLAYSURF,))
                #     t.start()
        if graph.is_finished():
            draw_slow(board, graph.path(), COLORS["RED"])
            graph.not_finished()
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == "__main__":
    main()
