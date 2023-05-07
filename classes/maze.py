import pygame

class Maze:
    def __init__(self):
        # Define the size of the grid and the size of each cell
        self.grid_size = (4, 4)
        self.cell_size = 50
        
        # Create a grid with all possible (x, y) coordinates
        self.grid = [(x, y) for y in range(self.grid_size[1]) for x in range(self.grid_size[0])]
        
        # Set a reward of -1 for each cell in the grid
        self.rewards = {pos: -1 for pos in self.grid}
        
        # Create a list of states, where each state is a tuple of (position, reward, is_terminal)
        self.states = [(pos, reward, False) for pos, reward in self.rewards.items()]
        
        # Define a list of possible actions
        self.actions = [0, 1, 2, 3]  
        
        # Calculate the size of the screen based on the grid size and cell size
        self.screen_size = (self.grid_size[0] * self.cell_size, self.grid_size[1] * self.cell_size)
        
        # Create dictionaries to store the value and policy for each state
        self.values = {}
        self.policy_table = {}

        # Initialize Pygame
        pygame.init()
        
        # Create a display window with the specified screen size and set the caption
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Maze")
        
        # Create a font for displaying text
        self.font = pygame.font.SysFont(None, 30)


    def setup_maze(self, terminal_states, updated_rewards):
        """
        Update the maze with new terminal states and rewards.

        Args:
            terminal_states (list): A list of (x, y) coordinates that are terminal states.
            updated_rewards (dict): A dictionary where the keys are (x, y) coordinates and the values are the updated rewards.

        Returns:
            None
        """
        # Update the rewards for each (x, y) coordinate in the maze
        for key, value in updated_rewards.items():
            self.rewards[key] = value
        
        # Update the states list to include terminal states
        self.states = [(pos, reward, False) if pos not in terminal_states else (pos, reward, True) for pos, reward in self.rewards.items()]


    def step(self, state, action):
        """
        Take a step in the environment based on the current state and action.

        Args:
            state (tuple): A tuple representing the current state, with (position, reward, terminal) values.
            action (int): An integer representing the action to take.

        Returns:
            tuple: A tuple representing the next state, with (position, reward, terminal) values.
        """
        # Unpack the state tuple into separate variables
        pos, reward, terminal = state

        # Move to the next position based on the selected action
        pos = self.move(pos, action)
        
        # Get the reward for the next position, or 0 if the position is not in the rewards dictionary
        next_reward = self.rewards.get(pos, 0)
        
        # Check if the next position is a terminal state (i.e. the start or end position)
        next_terminal = (pos == (0, 0)) or (pos == (self.grid_size[0] - 1, self.grid_size[1] - 1))
        
        # Create a tuple representing the next state
        next_state = (pos, next_reward, next_terminal)
        
        # Return the next state
        return next_state


    def move(self, pos, action):
        """
        Move to the next position based on the selected action.

        Args:
            pos (tuple): A tuple representing the current position with (x, y) values.
            action (int): An integer representing the action to take.

        Returns:
            tuple: A tuple representing the new position with (x, y) values.
        """
        x, y = pos
        
        # Check the action and make sure the new position is within the bounds of the grid
        if action == 0 and x > 0:  # move left
            x -= 1
        elif action == 1 and x < self.grid_size[0] - 1:  # move right
            x += 1
        elif action == 2 and y > 0:  # move up
            y -= 1
        elif action == 3 and y < self.grid_size[1] - 1:  # move down
            y += 1
        
        # Return the new position
        return (x, y)

        
    def draw(self, current_state, terminal_states):
        """
        Draw the maze on the screen.

        Args:
            current_state (tuple): A tuple representing the current state with (position, reward, terminal) values.
            terminal_states (list): A list of tuples representing the terminal states with (position, reward, terminal) values.

        Returns:
            None
        """
        # Fill the screen with white
        self.screen.fill((255, 255, 255))
        
        # Loop through each cell in the grid
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                # Create a rectangle for the cell
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                
                # Get the state for the current cell
                state = [state for state in self.states if state[0] == (x, y)][0]
                
                # Draw the cell with a blue color if it's the current state
                if state == current_state:
                    pygame.draw.rect(self.screen, (0, 0, 255), rect)
                # Draw the cell with a dark red color if it's a terminal state
                elif state[0] in terminal_states:
                    pygame.draw.rect(self.screen, (100, 0, 0), rect)
                # Draw the cell with a light gray color otherwise
                else:
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                
                # Draw a black border around the cell
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                
                # Create a font for displaying the reward and value
                font_size = self.cell_size // 3
                font = pygame.font.SysFont(None, font_size)
                
                # Draw the reward value in red text
                reward_text = font.render(str(state[1]), True, (255, 0, 0))
                reward_text_rect = reward_text.get_rect(center=(x * self.cell_size + self.cell_size // 4, y * self.cell_size + self.cell_size // 2))
                self.screen.blit(reward_text, reward_text_rect)
                
                # Get the value for the current state and draw it in blue text
                value = self.values[state]
                value_text = font.render(f"{value:.1f}", True, (0, 0, 255))
                value_text_rect = value_text.get_rect(center=(x * self.cell_size + 3 * self.cell_size // 4, y * self.cell_size + self.cell_size // 2))
                self.screen.blit(value_text, value_text_rect)

        # Update the display to show the new maze
        pygame.display.update()


    def value_iteration(self, tolerance=0.1, gamma=1, delta=0):
        """
        Perform value iteration to calculate the optimal policy for the maze.

        Args:
            tolerance (float): A small positive number that determines the stopping condition for the algorithm.
            gamma (float): A discount factor for future rewards.
            delta (float): An initial value for the maximum change in the value function.

        Returns:
            dict: A dictionary representing the optimal policy for each state.
        """
        # Print a message to indicate that value iteration is starting
        print(f"STARTING VALUE ITERATION")
        
        # Initialize the value function for each state to 0
        self.values = {state: 0 for state in self.states}
        
        # Perform value iteration until the maximum change in the value function is less than the tolerance
        while True:
            delta = 0
            for state in self.states:
                # Calculate the utility of the state
                u = self.Utility(state, gamma)
                
                # Calculate the maximum change in the value function
                delta = max(delta, (self.values[state] - u))
                
                # Update the value function for the state
                self.values[state] = u
                
            # If the maximum change in the value function is less than the tolerance, stop the algorithm
            if delta < tolerance:
                print(f"VALUE ITERATION COMPLETE")
                break
        
        # Print the values for each state on the board
        for i in self.create_board(self.values):
            print(i)
        
        # Return the optimal policy table
        return self.policy_table


    def Utility(self, state, gamma):
        """
        Calculate the utility of a given state.

        Args:
            state (tuple): A tuple representing the state with (position, reward, terminal) values.
            gamma (float): A discount factor for future rewards.

        Returns:
            float: The utility of the state.
        """
        _, _, terminal = state
        
        # If the state is terminal, set the policy to 4 and return 0
        if terminal:
            self.policy_table[state] = 4
            return 0
        
        # Get the next possible states from the current state
        next_states = self.get_next_states(state)
        
        # Calculate the value for each possible action
        value_per_action = [(action, (next_state[1] + (gamma * self.values[next_state[0]]))) for action, next_state in next_states.items()]
            
        # Choose the action with the maximum value
        action, value = max(value_per_action, key=lambda x: x[1])
        
        # Update the policy table for the current state
        self.policy_table[state] = action
        
        # Return the calculated value
        return value
        
        
    def get_next_states(self, state):
        """
        Get the possible next states and rewards given a state.

        Args:
            state (tuple): A tuple representing the state with (position, reward, terminal) values.

        Returns:
            dict: A dictionary mapping each possible action to a tuple of the next state and the reward for that action.
        """
        pos, _, _ = state
        next_states = {}
        
        # Loop through each possible action and calculate the next state and reward for that action
        for action in self.actions:
            next_pos = self.move(pos, action)
            if next_pos in self.rewards:
                reward = self.rewards[next_pos]
                boolean = [state[2] for state in self.states if state[0] == next_pos][0]
                next_state = (next_pos, reward, boolean)
            else:
                reward = 0
                boolean = [state[2] for state in self.states if state[0] == next_pos][0]
                next_state = (next_pos, reward, boolean)
            next_states[action] = (next_state, reward)
        
        # Return a dictionary mapping each possible action to the next state and the reward for that action
        return next_states


    def create_board(self, updated_values):
        """
        Create a board with the updated values for each state.

        Args:
            updated_values (dict): A dictionary mapping each state to its updated value.

        Returns:
            list: A list of lists representing the board with the updated values.
        """
        # Create an empty board with zeros
        board = [[0 for _ in range(4)] for _ in range(4)]
        
        # Loop through each state and update the board with its value
        for key, value in updated_values.items():
            x, y = key[0]
            y = 3 - y
            board[y][x] = value
        
        # Reverse the board and return it
        return reversed(board)


    def value_iteration_stochastic(self, tolerance=0.001, gamma=1, delta=0, probability=0.7):
        
        self.values = {state: 0 for state in self.states}
        
        while True:
            delta = 0
            for state in self.states:
                if state[2]:
                    continue
                else:
                    u = self.Utility_stochastic(state, gamma, probability)
                    delta = max(delta, (self.values[state] - u))
                    self.values[state] = u
                
            if delta < tolerance:
                break
        
        for i in self.create_board(self.values):
            print(i)
            
    def Utility_stochastic(self, state, gamma, probability):
        _, reward, _ = state

        next_states = self.get_next_states(state)
        
        lst_values = []
        
        for action, next_state in next_states.items():
            other_states = [other_state for action, other_state in next_states.items() if other_state != next_state]
            value = sum([(probability * (next_state[1] + gamma * self.values[next_state[0]]))] + [((1-probability)/3) * (other_state[1] + gamma * self.values[other_state[0]]) for other_state in other_states])
            lst_values.append(value)
            
        return max(lst_values)