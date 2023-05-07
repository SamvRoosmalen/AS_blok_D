# Import necessary classes and libraries
from classes.agent import Agent
from classes.policy import Policy
from classes.maze import Maze
import pygame

# Define a dictionary of positions and their respective rewards
important_pos = {
    (0, 3) : 10,
    (1, 3) : -2,
    (3, 0) : 40,
    (2, 1) : -10,
    (3, 1) : -10    
}

# Define a list of terminal states
terminal_states = [
    (3,0), 
    (0,3)
    ]

# Create a maze object and set it up with the terminal states and rewards
maze = Maze()
maze.setup_maze(terminal_states, important_pos)

# Run the value iteration algorithm on the maze to find the optimal policy
policy_table = maze.value_iteration()

# Create a policy object using the optimal policy table
policy = Policy(policy_table)

# Create an agent object using the maze, policy, and initial reward
agent = Agent(maze=maze,
              policy=policy,
              start_reward=-1)

# Set the starting state for the agent
start_state = ((2, 3), -1, False)  

# Set the current state to the starting state
current_state = start_state

# Draw the maze
maze.draw(current_state, terminal_states) 

# Delay for 1000 milliseconds (1 second)
pygame.time.delay(1000)  

# Loop until the current state is a terminal state
while current_state[0] not in terminal_states: 
    # Print the current position and reward
    print(f"CURRENT POSITION: {current_state[0]}")
    print(f"CURRENT REWARD  : {current_state[1]}")
    
    # Have the agent act in the current state
    current_state = agent.act(current_state)
    
    # Draw the maze
    maze.draw(current_state, terminal_states)  
    
    # Delay for 1000 milliseconds (1 second)
    pygame.time.delay(1000)  
  
# Print the final state position, reward, and total reward obtained by the agent
print(f"FINAL STATE POSITION: {current_state[0]}")
print(f"FINAL STATE REWARD  : {current_state[1]}")
print(f"TOTAL REWARD: {agent.reward}") 

# Quit pygame
pygame.quit()
