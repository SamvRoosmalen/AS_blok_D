    
class Agent:
    def __init__(self, maze, policy):
        self.maze = maze
        self.policy = policy
        self.values = {state: 0 for state in maze.states}

    def value(self, state):
        return self.values[state]

    def act(self, state):
        action = self.policy.select_action(state)
        next_state = self.maze.step(state, action)
        reward = self.maze.rewards.get(next_state[0], 0)
        self.values[state] += reward
        return next_state
