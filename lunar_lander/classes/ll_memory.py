import random
from collections import deque

class Memory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)
    
    def store(self, transition):
        self.memory.append(transition)
    
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)