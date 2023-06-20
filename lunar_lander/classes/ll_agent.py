import torch
import numpy as np
from torch import nn
from classes.ll_memory import Memory
from classes.ll_policy import Policy
import torch.nn.functional as F


class Agent:
    def __init__(self, state_size, action_size, memory_capacity=10000):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = Memory(memory_capacity)
        self.policy = Policy(state_size, action_size)
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=0.001)
        self.gamma = 0.99

    def decay_epsilon(self):        
        self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)

    def train(self, batch_size=64):
        
        if len(self.memory.memory) < batch_size:
            return -1

        batch = self.memory.sample(batch_size)
        states, actions, rewards, next_states, terminals = zip(*batch)
        
        states = torch.tensor(np.array(states), dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float)
        terminals = torch.tensor(terminals, dtype=torch.bool)
        
        current_q_values = self.policy(states).gather(1, actions.unsqueeze(1))
        
        next_q_values = max(self.policy(next_states)).max(1)[0]
        
        target_q_values = rewards + self.gamma * next_q_values * (~terminals)
        
        loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
               
        return loss.item()