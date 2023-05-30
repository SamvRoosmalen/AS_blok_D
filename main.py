# Import necessary classes and libraries
from classes.agent import Agent
from classes.policy import Policy
from classes.maze import Maze
import pygame

def draw_policy_table(policy_table):

    # Create a 4x4 grid with default actions as None
    grid = [['-' for _ in range(4)] for _ in range(4)]

    # Assign the actions to the corresponding grid cells
    for state, action in policy_table.items():
        position = state[0]
        action_string = 'R' if action == 1 else 'U' if action == 2 else 'L' if action == 0 else 'D'
        grid[position[1]][position[0]] = action_string

    # Print the grid
    for row in grid:
        print(row)

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

# Set the starting state for the agent
start_state = ((2, 3), -1, False)  

# Run the value iteration algorithm on the maze to find the optimal policy
# policy_table = maze.value_iteration()

# print(f"TD LEARNING WITH GAMMA = 1")
# policy_table = maze.TD_learning(learning_rate=0.1, 
#                                    gamma=0.9, 
#                                    num_episodes=1000, 
#                                    policy_table=policy_table, 
#                                    starting_state=start_state)

# print(f"SARSA CONTROL")
# policy_table = maze.sarsa_control(num_episodes=10000, 
#                                         learning_rate=0.1, 
#                                         gamma=0.9, 
#                                         epsilon=0.1)

print(f"Q LEARNING")
policy_table = maze.q_learning(num_episodes=10000, 
                                        learning_rate=0.01, 
                                        gamma=0.9, 
                                        epsilon=0.1)

# Create a policy object using the optimal policy table
policy = Policy(policy_table)

draw_policy_table(policy_table=policy_table)

# Create an agent object using the maze, policy, and initial reward
agent = Agent(policy=policy, start_state=start_state, start_reward=-1)

# Set the current state to the starting state
current_state = start_state

# Draw the maze
maze.draw(start_state, terminal_states) 

# Delay for 1000 milliseconds (1 second)
pygame.time.delay(1000)  

# Loop until the current state is a terminal state
while current_state[0] not in terminal_states: 
    # Print the current position and reward
    print(f"CURRENT POSITION: {current_state[0]}")
    print(f"CURRENT REWARD  : {current_state[1]}")
    
    # Have the agent act in the current state
    current_state = agent.act(maze.grid_size, maze.rewards)
    
    # Draw the maze
    maze.draw(current_state, terminal_states)  
    
    # Delay for 1000 milliseconds (1 second)
    pygame.time.delay(1000) 



# Print the final state position, reward, and total reward obtained by the agent
print(f"FINAL STATE POSITION: {current_state[0]}")
print(f"FINAL STATE REWARD  : {current_state[1]}")
print(f"TOTAL REWARD: {agent.reward}") 

pygame.time.delay(50000)

# Quit pygame
pygame.quit()