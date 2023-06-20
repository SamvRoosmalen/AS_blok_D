import random
import torch
from torch import nn
import numpy as np


class Policy(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.state_size = state_size
        self.action_size = action_size
        self.hidden_size = 128
        
        self.model = nn.Sequential(
            nn.Linear(self.state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_size)
        )
        
    def forward(self, state):
        return self.model(state)
        
    def select_action(self, state, epsilon):
        if random.uniform(0, 1) < epsilon:
            return random.choice(range(self.action_size))
        else:
            self.eval()
            with torch.no_grad():
                action_values = self.model(state)
            self.train()    
            return np.argmax(action_values.data.numpy())