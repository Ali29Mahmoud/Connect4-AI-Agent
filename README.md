# Expected Minimax Tree Visualization

This project implements a graphical user interface (GUI) to visualize the Expected Minimax Tree. The tree structure represents a decision-making process, typically used in game theory or AI algorithms. The visualization is built using the Pygame library, allowing users to interact with the tree by expanding/collapsing nodes and viewing details of the selected nodes.

# Visual Inspiration

The GUI for the Connect 4 game is inspired by *Squid Game*, where players compete for a prize, and losing results in elimination. The game's design reflects this high-stakes environment, adding excitement to the gameplay.
All assets credits used from 

[*Squid Game Assets*](https://mdesign.dk/squid_game/assets/assets.html)


## Features

- **Model Selection**: User selects how the tree is built "With or Without" Pruning and number of tree levels for evaluation
- **Selection screen**: User choose whether to start first or second
- **Tree Visualization**: The tree is represented with trapezoidal and circular nodes, alternating based on the node's level.
- **Interactive Nodes**: Users can click on nodes to toggle their expanded/collapsed states, showing or hiding child nodes.
- **Content Window**: When a node is clicked, additional details (like state, column, value, alpha, and beta) are displayed in a floating window near the node.
- **Scrolling**: The tree is drawn on a large virtual surface, with horizontal and vertical scrollbars to navigate through it.
- **Custom TKinter**: The application screens is built using ctk. 
- **Pygame-based Interface**: The Tree is built using Pygame for an interactive, graphical interface.

## Requirements

To run the project, you need Python 3 and the following libraries:

- **Custom Tkinter**: CustomTkinter is a Python library for modern, customizable Tkinter widgets.
- **pygame**: A library for writing video games, used here for creating the interactive GUI.

You can install the required libraries using pip:

```bash
pip install pygame
pip install customtkinter
```
## How to Run
```
python main_screen.py

```
