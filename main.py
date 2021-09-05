import curses

from board import Board
from view import View


def main(stdscr: curses.window):
    stdscr.clear()

    # Hide the cursor
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    rows, columns, number_of_mines = 10, 10, 10
    board = Board(columns=columns, rows=rows, number_of_mines=number_of_mines)
    view = View(stdscr=stdscr, rows=rows, columns=columns, board=board)
    view.loop()


curses.wrapper(main)
