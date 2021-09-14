import random
from typing import Optional

from square import Square


class Board:
    RESET = 0
    KEEP_PLAYING = 1
    WIN = 2
    LOSS = 3

    def __init__(self, columns: int, rows: int, number_of_mines: int):
        self.squares = [Square() for _ in range(columns * rows)]
        self.columns = columns
        self.rows = rows
        self.number_of_mines = number_of_mines
        self.current_state = Board.RESET
        self._set_square_neighbors()
        self.reset()

    def keep_playing(self) -> bool:
        return self.current_state == Board.KEEP_PLAYING or self.current_state == Board.RESET

    def won(self) -> bool:
        return self.current_state == Board.WIN

    def lost(self) -> bool:
        return self.current_state == Board.LOSS

    def reset(self):
        self.current_state = Board.RESET
        for square in self.squares:
            square.reset()

    def _sweep(self, square: Square, is_empty_space_sweep: bool = False):
        if square.is_flagged:
            return

        if not square.is_swept:
            square.sweep()
            if square.is_mine:
                self.current_state = Board.LOSS

            # We've encountered empty space. Sweep everything around us.
            if not square.is_mine and square.mines_counter == 0:
                self._sweep_empty_space(square)
        elif not is_empty_space_sweep and not square.is_mine:
            flagged_neighbors_count = self._count_flagged_neighbors(square)
            if flagged_neighbors_count == square.mines_counter:
                self._sweep_neighbors(square)

        if self.current_state != Board.LOSS:
            if all((square.is_mine for square in self.squares if not square.is_swept)):
                self.current_state = Board.WIN

    def sweep_by_index(self, x, y):
        if self.current_state == Board.RESET:
            self._place_mines(x, y)

        square = self.get_square(x, y)
        self._sweep(square)

    def flag(self, x, y):
        square = self.get_square(x, y)
        if square is not None:
            square.toggle_flag()

    def get_square(self, x, y) -> Optional[Square]:
        if not (0 <= y < self.rows) or not (0 <= x < self.columns):
            return None

        return self.squares[y * self.columns + x]

    def _increase_neighbor_mines_counter(self, square: Square):
        for neighbor in square.neighbors:
            neighbor.increase_mine_counter()

    def _sweep_empty_space(self, square: Square):
        for neighbor in square.neighbors:
            self._sweep(neighbor, is_empty_space_sweep=True)

    def _count_flagged_neighbors(self, square: Square) -> int:
        flags = 0
        for neighbor in square.neighbors:
            if neighbor.is_flagged:
                flags += 1

        return flags

    def _sweep_neighbors(self, square: Square):
        for neighbor in square.neighbors:
            if not neighbor.is_flagged:
                neighbor.sweep()
                if neighbor.is_mine:
                    self.current_state = Board.LOSS

                if neighbor.mines_counter == 0:
                    self._sweep_empty_space(neighbor)

    def _set_neighbors(self, x, y):
        top_y = y - 1
        bottom_y = y + 1
        left_x = x - 1
        right_x = x + 1

        square = self.get_square(x, y)
        for current_y in range(top_y, bottom_y + 1):
            for current_x in range(left_x, right_x + 1):
                if current_x == x and current_y == y:
                    continue
                neighbor = self.get_square(current_x, current_y)
                if neighbor is not None:
                    square.neighbors.append(neighbor)

    def _set_square_neighbors(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self._set_neighbors(x, y)

    def _place_mines(self, x: int, y: int):
        self.current_state = Board.KEEP_PLAYING
        placed_mines = 0
        random.seed()
        while placed_mines < self.number_of_mines:
            current_x, current_y = random.randrange(0, self.columns), random.randrange(0, self.rows)
            if (x - 1 <= current_x <= x + 1) and (y - 1 <= current_y <= y + 1):
                continue

            square = self.get_square(current_x, current_y)
            if not square.is_mine:
                square.set_as_mine()
                placed_mines += 1
                self._increase_neighbor_mines_counter(square)
