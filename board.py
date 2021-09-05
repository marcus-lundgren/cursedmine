import random
from typing import Optional

from square import Square


class Board:
    def __init__(self, columns: int, rows: int, number_of_mines: int):
        self.squares = [Square() for _ in range(columns * rows)]
        self.columns = columns
        self.rows = rows
        self.number_of_mines = number_of_mines
        self.reset()

    def reset(self):
        for square in self.squares:
            square.reset()

        # Place the mines
        placed_mines = 0
        random.seed()
        while placed_mines < self.number_of_mines:
            x, y = random.randrange(0, self.columns), random.randrange(0, self.rows)
            square = self.get_square(x, y)
            if not square.is_mine:
                square.set_as_mine()
                placed_mines += 1
                self.increase_neighbor_mines_counter(x, y)

    def sweep(self, x, y, is_empty_space_sweep: bool = False):
        square = self.get_square(x, y)
        if square is None or square.is_flagged:
            return

        if not square.is_swept:
            square.sweep()

            # We've encountered empty space. Sweep everything around us.
            if not square.is_mine and square.mines_counter == 0:
                self.sweep_empty_space(x, y)
        elif not is_empty_space_sweep and not square.is_mine:
            flagged_neighbors_count = self.count_flagged_neighbors(x, y)
            if flagged_neighbors_count == square.mines_counter:
                self.sweep_neighbors(x, y)

    def flag(self, x, y):
        square = self.get_square(x, y)
        if square is not None:
            square.toggle_flag()

    def get_square(self, x, y) -> Optional[Square]:
        if not (0 <= y < self.rows) or not (0 <= x < self.columns):
            return None

        return self.squares[y * self.columns + x]

    def increase_neighbor_mines_counter(self, x: int, y: int):
        top_y = y - 1
        bottom_y = y + 1
        left_x = x - 1
        right_x = x + 1

        for current_y in range(top_y, bottom_y + 1):
            for current_x in range(left_x, right_x + 1):
                if current_x == x and current_y == y:
                    continue

                square = self.get_square(current_x, current_y)
                if square is not None:
                    square.increase_mine_counter()

    def sweep_empty_space(self, x: int, y: int):
        top_y = y - 1
        bottom_y = y + 1
        left_x = x - 1
        right_x = x + 1

        for current_y in range(top_y, bottom_y + 1):
            for current_x in range(left_x, right_x + 1):
                if current_x == x and current_y == y:
                    continue

                self.sweep(current_x, current_y, is_empty_space_sweep=True)

    def count_flagged_neighbors(self, x: int, y: int) -> int:
        top_y = y - 1
        bottom_y = y + 1
        left_x = x - 1
        right_x = x + 1

        flags = 0
        for current_y in range(top_y, bottom_y + 1):
            for current_x in range(left_x, right_x + 1):
                if current_x == x and current_y == y:
                    continue

                square = self.get_square(current_x, current_y)
                if square is not None and square.is_flagged:
                    flags += 1

        return flags

    def sweep_neighbors(self, x: int, y: int):
        top_y = y - 1
        bottom_y = y + 1
        left_x = x - 1
        right_x = x + 1

        for current_y in range(top_y, bottom_y + 1):
            for current_x in range(left_x, right_x + 1):
                if current_x == x and current_y == y:
                    continue

                square = self.get_square(current_x, current_y)
                if square is not None and not square.is_flagged:
                    square.sweep()
                    if square.mines_counter == 0:
                        self.sweep_empty_space(current_x, current_y)
