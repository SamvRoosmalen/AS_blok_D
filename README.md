# AS Maze 2.1

This is a Python implementation of a maze solver using the value iteration algorithm. The solver finds the optimal policy for a given maze using the Bellman equation to calculate the utility of each state.

## Installation

To use the maze solver, you will need to have Python 3 installed on your system. You can download Python 3 from the official website at https://www.python.org/downloads/.

You will also need to install the Pygame library to run the maze visualization. You can install Pygame using pip:

## Usage

To use the maze solver, run the `main.py` script:

The script will load a default maze and display the initial values and policy for each state. The solver will then run the value iteration algorithm to find the optimal policy for the maze, and display the updated values and policy for each state. You can modify the maze by editing the `maze.txt` file in the `data` directory.

## Files

- `main.py`: The main script for running the maze solver.
- `maze.py`: The implementation of the maze class.
- `policy.py`: The implementation of the policy class.
- `utils.py`: Utility functions for the maze solver.
- `data/maze.txt`: The text file containing the maze data.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
