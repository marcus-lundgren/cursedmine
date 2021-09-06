import curses
from board import Board


class View:
    COLOR_PAIR_NORMAL = 1
    COLOR_PAIR_HIGHLIGHT = 2
    COLOR_PAIR_UNSWEPT = 3
    COLOR_PAIR_FLAGGED = 4
    COLOR_PAIR_MINE = 5

    def __init__(self, stdscr: curses.window, rows: int, columns: int, board: Board):
        self.stdscr = stdscr
        self.columns = columns
        self.rows = rows
        self.board = board

        self.stdscr.clear()

        # Hide the cursor
        curses.curs_set(0)

        curses.init_pair(View.COLOR_PAIR_NORMAL, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(View.COLOR_PAIR_HIGHLIGHT, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(View.COLOR_PAIR_UNSWEPT, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(View.COLOR_PAIR_FLAGGED, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(View.COLOR_PAIR_MINE, curses.COLOR_BLACK, curses.COLOR_RED)

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
        square_value = " "
        color_pair = View.COLOR_PAIR_HIGHLIGHT if highlight else View.COLOR_PAIR_UNSWEPT
        if square.is_flagged:
            color_pair = View.COLOR_PAIR_HIGHLIGHT if highlight else View.COLOR_PAIR_FLAGGED
            square_value = "+"
        elif square.is_swept:
            color_pair = View.COLOR_PAIR_HIGHLIGHT if highlight else View.COLOR_PAIR_NORMAL
            if square.is_mine:
                color_pair = View.COLOR_PAIR_MINE
                square_value = "X"
            else:
                mines_counter = square.mines_counter
                square_value = str(mines_counter) if 0 < mines_counter else " "

        self.stdscr.addstr(y * 2 + 1, x * 2 + 1, square_value, curses.color_pair(color_pair))

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
            mod_mine_count = (self.board.number_of_mines % 10)
            flagged_squares = str(sum([1 for square in self.board.squares if square.is_flagged]))
            self.stdscr.addstr(1, self.columns * 2 + 1,
                               f"{flagged_squares}/{self.board.number_of_mines}".rjust(5),
                               curses.color_pair(View.COLOR_PAIR_NORMAL))
            self.stdscr.addstr(2, self.columns * 2 + 1, str(current_key), curses.color_pair(View.COLOR_PAIR_NORMAL))
            pass
