import curses
from board import Board


class View:
    def __init__(self, stdscr: curses.window, rows: int, columns: int, board: Board):
        self.stdscr = stdscr
        self.columns = columns
        self.rows = rows
        self.board = board

    def reset_color_of_square(self, x: int, y: int):
        self.print_square(x, y, False)

    def highlight_square(self, x: int, y: int):
        self.print_square(x, y, True)

    def print_squares(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.print_square(x, y)

    def print_square(self, x, y, highlight: bool = False):
        square = self.board.get_square(x, y)
        square_value = "-"
        if square.is_flagged:
            square_value = "^"
        elif square.is_swept:
            if square.is_mine:
                square_value = "X"
            else:
                mines_counter = square.mines_counter
                square_value = str(mines_counter) if 0 < mines_counter else " "

        self.stdscr.addstr(y * 2 + 1, x * 2 + 1, square_value, curses.color_pair(3 if highlight else 1))

    def loop(self):
        self.print_squares()
        current_x, current_y = 0, 0

        while True:
            current_key = self.stdscr.getch()
            if current_key == curses.KEY_LEFT:
                if current_x == 0:
                    continue

                self.reset_color_of_square(current_x, current_y)
                current_x -= 1
                self.highlight_square(current_x, current_y)
            elif current_key == curses.KEY_RIGHT:
                if current_x == self.columns - 1:
                    continue

                self.reset_color_of_square(current_x, current_y)
                current_x += 1
                self.highlight_square(current_x, current_y)
            elif current_key == curses.KEY_UP:
                if current_y == 0:
                    continue

                self.reset_color_of_square(current_x, current_y)
                current_y -= 1
                self.highlight_square(current_x, current_y)
            elif current_key == curses.KEY_DOWN:
                if current_y == self.rows - 1:
                    continue

                self.reset_color_of_square(current_x, current_y)
                current_y += 1
                self.highlight_square(current_x, current_y)
            elif current_key == 102:
                self.board.flag(current_x, current_y)
                self.print_square(current_x, current_y)
            elif current_key == 114:
                self.board.reset()
                self.print_squares()
                self.highlight_square(current_x, current_y)
            elif current_key == 115:
                self.board.sweep(current_x, current_y)
                self.print_squares()
                self.highlight_square(current_x, current_y)
            elif current_key == 113:
                break

            self.stdscr.refresh()
            self.stdscr.addstr(self.rows * 2 + 1, 0, f"({current_x}, {current_y})", curses.color_pair(1))
            self.stdscr.addstr(self.rows * 2 + 2, 0, str(current_key), curses.color_pair(1))
            pass
