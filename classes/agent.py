class Agent:
    def __init__(self, maze, policy, start_reward):
        """
        Initialize the agent with the maze and the policy.

        Args:
        - maze (Maze): the maze object
        - policy (Policy): the policy object
        """
        self.maze = maze
        self.policy = policy
        self.reward = start_reward

    def act(self, state):
        """
        Act based on the current state of the agent.

        Args:
        - state: the current state of the agent

        Returns:
        - next_state: the next state of the agent after taking an action based on the policy
        """
        action = self.policy.select_action(state)
        next_state = self.maze.step(state, action)
        self.reward += next_state[1]
        return next_state

