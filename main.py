from classes.agent import Agent
from classes.policy import Policy
from classes.maze import Maze
import pygame

maze = Maze()
policy = Policy(maze.actions)
agent = Agent(maze, policy)

start_state = ((0, 3), 0, False)  
agent.values[start_state] = 0  
current_state = start_state

maze.draw(current_state)  

pygame.time.delay(1000)  

while not current_state[2]: 
    current_state = agent.act(current_state)
    maze.draw(current_state)  
    pygame.time.delay(500)  

print("Final state:", current_state)

pygame.quit() 