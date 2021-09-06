import curses

from board import Board
from view import View


def main(stdscr: curses.window):
    rows, columns, number_of_mines = 16, 30, 99
    board = Board(columns=columns, rows=rows, number_of_mines=number_of_mines)
    view = View(stdscr=stdscr, rows=rows, columns=columns, board=board)
    view.loop()


curses.wrapper(main)
