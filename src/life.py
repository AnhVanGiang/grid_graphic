from extra import Board, COLORS
from itertools import product
import time
import sys


class Life:
    def __init__(self, board: Board):
        self._board = board

    def _get_live_neighbors(self, x: int, y: int) -> int:
        return len(list(filter(lambda x: self._board.get_rect(x[0], x[1]).color == COLORS["RED"],
                               self._board.get_neighbors_diag(x, y))))

    def _to_die(self, x: int, y: int) -> bool:
        return (self._is_live(x, y) and self._get_live_neighbors(x, y) < 2) or \
               (self._is_live(x, y) and self._get_live_neighbors(x, y) > 3)

    def _is_live(self, x: int, y: int) -> bool:
        return self._board.get_rect(x, y).color == COLORS["RED"]

    def _is_dead(self, x: int, y: int) -> bool:
        return self._board.get_rect(x, y).color == COLORS["WHITE"]

    def _to_live(self, x, y) -> bool:
        return (self._is_dead(x, y) and self._get_live_neighbors(x, y) == 3) or \
               (self._is_live(x, y) and self._get_live_neighbors(x, y) in (2, 3))

    def game(self):
        size = self._board.size
        while True:
            for x in range(size):
                for y in range(size):
                    if self._to_live(x, y):
                        self._board.get_rect(x, y).set_color(COLORS["RED"])
                    elif self._to_die(x, y):
                        self._board.get_rect(x, y).set_color(COLORS["WHITE"])
            time.sleep(sys.float_info.min)





