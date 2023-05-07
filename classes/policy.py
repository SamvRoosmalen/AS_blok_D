class Policy:
    def __init__(self, policy_table):
        """
        Initialize a new instance of the Policy class.

        Args:
            policy_table (dict): A dictionary mapping each state to the action with the highest value for that state.
        """
        # Store the policy table
        self.policy_table = policy_table

    def select_action(self, state):
        """
        Select the action with the highest value for the given state.

        Args:
            state (tuple): A tuple representing the state with (position, reward, terminal) values.

        Returns:
            int: The action with the highest value for the given state.
        """
        # Get the action with the highest value from the policy table for the given state
        return self.policy_table[state]
