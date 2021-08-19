import pygame
from pygame import Rect, Color
import random
from typing import List, Tuple

colors = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "NAVYBLUE": (60, 60, 100),
    "DARKBLUE": (0, 0, 139),
    "YELLOW": (255, 255, 0),
    "BLACK": (0, 0, 0)
}

directions = [
    (0, -1),
    (0, 1),
    (1, 0),
    (-1, 0)
]


class NRect(Rect):
    """
    New rectangle object inheritted from pygame.Rect
    """

    def __init__(self,
                 x: int, y: int, width: int, height: int,
                 color: str = "WHITE"):
        super(NRect, self).__init__(x, y, width, height)
        self._color = color

    def get_color(self) -> Tuple[int, int, int]:
        """
        Get color of the rectangle as a RGB tuple
        :return:
        """
        return colors[self._color]

    def set_color(self, color: str) -> None:
        """
        Set color
        :param color:
        :return:
        """
        self._color = color

    @property
    def color_str(self) -> str:
        """
        Get color of the rectangle as string
        :return:
        """
        return self._color


class Board:
    def __init__(self, size: int, gap_size: int, wind_width: int):
        self._boards = []
        self._gap = gap_size
        self._wwidth = wind_width
        self._size = size

    @property
    def bsize(self):
        return self._wwidth // self._size + self._gap

    def change_cell_col(self, x: int, y: int, color: str) -> None:
        self._boards[x][y].set_color(color)

    def get_col(self, x: int, y: int) -> str:
        return self._boards[x][y].color_str

    def box_coords(self, x: int, y: int) -> Tuple[int, int]:
        """
        Convert cell's coordinate on board to screen coordinate
        :param x: row
        :param y: column
        :return:
        """
        x = x * (self.bsize + self._gap)
        y = y * (self.bsize + self._gap)
        return x, y

    @property
    def size(self) -> int:
        """
        Get size of the board
        :return:
        """
        return self._size

    def create_board(self) -> None:
        """
        Create the whole board
        :return:
        """
        for i in range(self._size):
            self._boards.append([])
            for j in range(self._size):
                x, y = self.box_coords(i, j)
                rect = NRect(x, y, self.bsize, self.bsize)
                self._boards[i].append(rect)

    def get_rect(self, x: int, y: int) -> NRect:
        """
        Get the NRect object at a board coordinate
        :param x:
        :param y:
        :return:
        """
        return self._boards[x][y]

    def set_rect(self, x: int, y: int, rect: NRect) -> None:
        """
        Change the NRect object at a coordinate
        :param x:
        :param y:
        :param rect:
        :return:
        """
        self._boards[x][y] = rect

    def get_board1(self) -> List[List[NRect]]:
        """
        Get the whole board as 2d array
        :return:
        """
        return self._boards

    def get_board2(self) -> List[NRect]:
        """
        Get the whole board as 1d array
        :return:
        """
        b = []
        for lst in self._boards:
            b.extend(lst)
        return b

    def reset_color(self, color: str = "ALL") -> None:
        """
        Change the colors of every cell to WHITE
        :return:
        """
        board = self.get_board2()
        for rect in board:
            if color != "ALL":
                if rect.color_str == color:
                    rect.set_color("WHITE")
            else:
                rect.set_color("WHITE")

    def count_dist(self, color: str) -> int:
        """
        Count the number of cells of a color
        :param color:
        :return:
        """
        c = 0
        board = self.get_board2()
        for rect in board:
            if rect.color_str == color:
                c += 1
        return c

    def get_neighbors(self, x: int, y: int, walls: False) -> List[Tuple[int, int]]:
        """
        Get the four directional neighbors of a cell. If walls is True, only get the ones where they arent black
        :param x:
        :param y:
        :param walls:
        :return:
        """
        ret = []
        for i in directions:
            nx, ny = x + i[0], y + i[1]
            if not walls:
                if (0 <= nx < self._size - 1) and (0 <= ny < self._size - 1):
                    ret.append((nx, ny))
            else:
                board = self.get_board1()
                if (0 <= nx < self._size - 1) \
                        and (0 <= ny < self._size - 1) \
                        and board[nx][ny].color_str != "BLACK":
                    ret.append((nx, ny))
        return ret

    def mark_rects(self, rects: List[Tuple[int, int]], color: str = "YELLOW") -> None:
        """
        Paint the list of cells as a color
        :param rects:
        :param color:
        :return:
        """
        board = self.get_board1()
        for i in rects:
            board[i[0]][i[1]].set_color(color)

    # def random_cell(self, color: str = "WHITE", edge: bool = False) -> Tuple[int, int]:
    #     """
    #     Get a random cell on the board
    #     :return:
    #     """
    #     lst = []
    #     board = self.get_board1()
    #     if edge:
    #         a = 1
    #     else:
    #         a = 0
    #     for i in range(a, self.size - a):
    #         for j in range(a, self.size - a):
    #             if board[i][j].color_str == color:
    #                 lst.append((i, j))
    #     return random.choice(lst)