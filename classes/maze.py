class Maze:
    def __init__(self):
        self.grid = [(x, y) for y in range(4) for x in range(4)]
        self.rewards = {pos: 1 for pos in self.grid}
        self.states = [(pos, reward, False) for pos, reward in self.rewards.items()]
        self.actions = [0, 1, 2, 3]  

    def step(self, state, action):
        pos, reward, terminal = state
        x, y = pos
        if action == 0 and x > 0: 
            x -= 1
        elif action == 1 and x < 3:  
            x += 1
        elif action == 2 and y > 0: 
            y -= 1
        elif action == 3 and y < 3: 
            y += 1

        pos = (x, y)
        next_reward = self.rewards.get(pos, 0)
        next_terminal = (pos == (0, 0)) or (pos == (3, 3))
        next_state = (pos, next_reward, next_terminal)
        return next_state
