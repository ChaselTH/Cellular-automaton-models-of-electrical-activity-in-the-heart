class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.is_changed = False

    def next_state(self):
        if self.state == 15:
            self.state = 12
        elif self.state == 12:
            self.state = 8
        elif self.state == 8:
            self.state = 20
