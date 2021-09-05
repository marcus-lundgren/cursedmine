class Square:
    def __init__(self):
        self.is_mine = False
        self.mines_counter = 0
        self.is_swept = False
        self.is_flagged = False

    def reset(self):
        self.is_swept = False
        self.is_flagged = False
        self.mines_counter = 0
        self.is_mine = False

    def increase_mine_counter(self):
        self.mines_counter += 1

    def set_as_mine(self):
        self.is_mine = True

    def toggle_flag(self):
        if not self.is_swept:
            self.is_flagged = not self.is_flagged

    def sweep(self):
        if not self.is_flagged:
            self.is_swept = True

    def get_mines_counter(self) -> str:
        return str(self.mines_counter)
