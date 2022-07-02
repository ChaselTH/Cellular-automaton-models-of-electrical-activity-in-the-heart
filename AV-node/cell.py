class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.is_changed = False

    def next_state(state):
        if state == 2:
            return 1
        elif state == 1:
            return 0
