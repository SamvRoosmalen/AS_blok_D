class Agent:
    def __init__(self, policy, start_state, start_reward):
        """
        Initialize the agent with the policy.

        Args:
        - policy (Policy): the policy object
        - start_state (tuple): the initial state of the agent
        - start_reward (int): the initial reward of the agent
        """
        self.policy = policy
        self.state = start_state
        self.reward = start_reward

    def act(self, grid_size, rewards):
        """
        Act based on the current state of the agent.

        Args:
        - grid_size (tuple): the size of the grid

        Returns:
        - next_state: the next state of the agent after taking an action based on the policy
        """
        action = self.policy.select_action(self.state)
        next_state = self.calculate_next_state(self.state, action, grid_size, rewards)
        self.reward += next_state[1]
        self.state = next_state
        return next_state

    def calculate_next_state(self, state, action, grid_size, rewards):
        """
        Calculate the next state based on the current state and action.

        Args:
        - state: the current state of the agent
        - action: the action to take
        - grid_size (tuple): the size of the grid

        Returns:
        - next_state: the next state of the agent after taking the action
        """
        pos, reward, terminal = state
        next_pos = self.move(pos, action, grid_size)
        next_reward = rewards[next_pos]  
        next_terminal = (next_pos == (0, 0)) or (next_pos == (grid_size[0] - 1, grid_size[1] - 1))
        next_state = (next_pos, next_reward, next_terminal)
        return next_state

    def move(self, pos, action, grid_size):
        """
        Move to the next position based on the selected action.

        Args:
            pos (tuple): A tuple representing the current position with (x, y) values.
            action (int): An integer representing the action to take.
            grid_size (tuple): the size of the grid

        Returns:
            tuple: A tuple representing the new position with (x, y) values.
        """
        x, y = pos

        if action == 0 and x > 0:  # move left
            x -= 1
        elif action == 1 and x < grid_size[0] - 1:  # move right
            x += 1
        elif action == 2 and y > 0:  # move up
            y -= 1
        elif action == 3 and y < grid_size[1] - 1:  # move down
            y += 1

        next_pos = (x, y)
        return next_pos
