class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

    def next_state(self, state):
        if state == 0:
            return 2
        elif state == 2:
            return 1
        elif state == 1:
            return 0
