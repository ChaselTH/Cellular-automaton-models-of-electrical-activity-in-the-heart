class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.is_changed = False

    def next_state(self):
        if self.state == 5:
            self.state = 2
        elif self.state == 2:
            self.state = 1
