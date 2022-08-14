class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.is_changed = False
        self.wait = 0

    def next_fast(self):
        if self.state == 33:
            self.state = 40
        elif self.state == 76:
            self.state = 100
        elif self.state != 100:
            print(self.wait)
            if self.wait == 2:
                self.state += 4
                self.wait = 0
            else:
                self.wait += 1

    def next_slow(self):
        if self.wait == 1:
            if self.state == 33:
                self.state = 56
            elif self.state == 72:
                self.state = 100
            elif self.state != 100:
                self.state = self.state + 16
            self.wait = 0
        else:
            self.wait += 1
