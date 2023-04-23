from classes.agent import Agent
from classes.policy import Policy
from classes.maze import Maze

maze = Maze()
policy = Policy(maze.actions)
agent = Agent(maze, policy)

start_state = ((0, 3), 0, False)  

agent.values[start_state] = 0  

current_state = start_state

while not current_state[2]: 
    print("Current state:", current_state)
    current_state = agent.act(current_state)

print("Final state:", current_state)