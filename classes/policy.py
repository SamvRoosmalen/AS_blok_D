import random

class Policy:
    def __init__(self, actions):
        self.actions = actions

    def select_action(self, state):
        return random.choice(self.actions)
