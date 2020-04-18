from typing import List

import cmsh

from .board import Board


class Life:
    boards: List[Board]

    width: int
    height: int

    model: cmsh.Model

    def __init__(self, width: int, height: int):
        self.boards = []
        self.width = width
        self.height = height

        self.model = cmsh.Model()

    def step_time(self, count: int = 1) -> Board:
        result = None
        for _ in range(count):
            result = Board(self.model, self.width, self.height)
            self.boards.append(result)

        return result

    def add_rules(self, previous: Board, current: Board):
        for y in range(self.height):
            for x in range(self.width):
                neighbors = []
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue
                        if dy + y < 0:
                            continue
                        if dx + x < 0:
                            continue
                        if dy + y >= self.height:
                            continue
                        if dx + x >= self.width:
                            continue
                        past_var = previous.bvars[dy + y][dx + x]
                        neighbors.append(past_var)

                past = previous.bvars[y][x]
                square = current.bvars[y][x]

                self.add_rule(square, past, neighbors)

    def add_rule(self, square: cmsh.Variable, past: cmsh.Variable, neighbors: List[cmsh.Variable]):
        v_neighbors = self.model.to_vec(neighbors)
        is_alive = ((past & (v_neighbors.bit_sum() == 2)) | 
                    (past & (v_neighbors.bit_sum() == 3)) |
                    ((past == False) & (v_neighbors.bit_sum() == 3)))
        is_dead = is_alive == False
        self.model.add_assert((square & is_alive) | ((square == False) & is_dead))

    def solve(self):
        for board in self.boards:
            board.add_asserts()

        for index, past in enumerate(self.boards[:-1]):
            current = self.boards[index+1]
            self.add_rules(past, current)

        return self.model.solve()
