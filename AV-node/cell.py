class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.is_changed = False
        self.wait = 0

    def next_state(self):
        if self.state == 15:
            self.state = 12
        elif self.state == 12:
            self.state = 8
        elif self.state == 8:
            self.state = 20

    def next_fast(self):
        if self.state == 33:
            self.state = 36
        elif self.state == 90:
            self.state = 100
        elif self.state != 100:
            if self.wait == 2:
                self.state = self.state + 2
                self.wait = 0
            else:
                self.wait += 1

    def next_slow(self):
        if self.state == 33:
            self.state = 52
        elif self.state == 72:
            self.state = 100
        elif self.state != 100:
            self.state = self.state + 16

