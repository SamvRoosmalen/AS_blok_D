import pygame

class Maze:
    def __init__(self):
        self.grid_size = (4, 4)
        self.cell_size = 50
        self.grid = [(x, y) for y in range(self.grid_size[1]) for x in range(self.grid_size[0])]
        self.rewards = {pos: 1 for pos in self.grid}
        self.states = [(pos, reward, False) for pos, reward in self.rewards.items()]
        self.actions = [0, 1, 2, 3]  
        self.screen_size = (self.grid_size[0] * self.cell_size, self.grid_size[1] * self.cell_size)

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Maze")
        self.font = pygame.font.SysFont(None, 30)

    def step(self, state, action):
        pos, reward, terminal = state
        x, y = pos
        if action == 0 and x > 0:  
            x -= 1
        elif action == 1 and x < self.grid_size[0] - 1:  
            x += 1
        elif action == 2 and y > 0:  
            y -= 1
        elif action == 3 and y < self.grid_size[1] - 1: 
            y += 1

        pos = (x, y)
        next_reward = self.rewards.get(pos, 0)
        next_terminal = (pos == (0, 0)) or (pos == (self.grid_size[0] - 1, self.grid_size[1] - 1))
        next_state = (pos, next_reward, next_terminal)
        return next_state

    def draw(self, current_state):
        self.screen.fill((255, 255, 255))

        
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if (x, y) == current_state[0]:
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)
                elif (x, y) == (0, 0) or (x, y) == (self.grid_size[0] - 1, self.grid_size[1] - 1):
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                else:
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        
        for pos, reward in self.rewards.items():
            x, y = pos
            text = self.font.render(str(reward), True, (255, 0, 0))
            text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2))
            self.screen.blit(text, text_rect)

        pygame.display.update()
