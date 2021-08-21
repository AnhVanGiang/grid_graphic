#!/usr/bin/env python
# coding: utf-8
from typing import Tuple, List
from extra import Board, COLORS
import heapq
import time
import sys


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent: Tuple[int, int] = None, position: Tuple[int, int] = None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


class Graph:
    def __init__(self, board: Board):
        self._board = board
        self._start_end = [(0, 0), (0, 0)]
        self._path: List[Tuple[int, int]] = [(0, 0)]
        self._proc: List[Tuple[int, int]] = []
        self._color: Tuple[int, int, int] = COLORS["DARKBLUE"]

    def set_se(self, se: List[Tuple[int, int]]):
        self._start_end = se

    def set_start(self, start: Tuple[int, int]):
        self._start_end[0] = start

    def set_end(self, end: Tuple[int, int]):
        self._start_end[1] = end

    @property
    def start(self) -> Tuple[int, int]:
        return self._start_end[0]

    @property
    def end(self) -> Tuple[int, int]:
        return self._start_end[1]

    @property
    def start_end(self):
        return self._start_end

    def return_path(self, current_node: Node) -> None:
        current = current_node
        while current is not None:
            self._path.append(current.position)
            current = current.parent
            time.sleep(sys.float_info.min)

        self._path = self._path[::-1]  # Return reversed path

    def empty(self) -> None:
        self._path = []
        self._proc = []

    def astar(self) -> None:
        self.empty()
        """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        https://gist.github.com/Nicholas-Swift/003e1932ef2804bebef2710527008f44
        """

        # Create start and end node
        start_node = Node(None, self.start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.end)
        end_node.g = end_node.h = end_node.f = 0

        print(end_node.position)

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Heapify the open_list and Add the start node
        heapq.heapify(open_list)
        heapq.heappush(open_list, start_node)

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = (self._board.size ** 2)

        # Loop until you find the end
        while len(open_list) > 0:
            outer_iterations += 1
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)
            if outer_iterations > max_iterations:
                # if we hit this point return the path such as it is
                # it will not contain the destination
                self.return_path(current_node)
                return
                # Get the current node
            # Found the goal
            if current_node == end_node:
                self.return_path(current_node)
                return
            # Generate children
            children = []
            neighbors = self._board.get_neighbors(current_node.position[0], current_node.position[1], True)
            for new_position in neighbors:  # Adjacent squares
                # Create new node
                new_node = Node(current_node, new_position)
                # Append
                children.append(new_node)
            # Loop through children
            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in open_list if
                        child.position == open_node.position and child.g > open_node.g]) > 0:
                    continue
                # Add the child to the open list
                heapq.heappush(open_list, child)
                self._board.get_rect(*current_node.position).set_color(COLORS["DARKBLUE"])
            time.sleep(sys.float_info.min)

        self._path = [(0, 0)]
        return

    def dijstra(self):
        self.empty()

        shortest = {self.start: (None, 0)}
        current = self.start
        visited = set()

        while current != self.end:
            visited.add(current)
            neighbors = self._board.get_neighbors(*current, walls=True)
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
                self._board.reset_color(self._color)
                return
            current = min(next_dests, key=lambda k: next_dests[k][1])

            self._board.get_rect(*current).set_color(self._color)
            time.sleep(sys.float_info.min)

        while current is not None:
            self._path.append(current)
            next_node = shortest[current][0]
            current = next_node
            time.sleep(sys.float_info.min)

        self._path = self._path[::-1]
        return
