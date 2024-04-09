<h1>SOLVING MAZE WITH ONLINE SEARCH ALGORITHMS</h1>

## Introduction

This project is the third in a series of projects in which simple games will be developed using the pygame library, and these games will be conquered using machine learning algorithms and artificial intelligence in general.

The motivation behind this approach lies in frequent situations where certain evaluation metrics, when applied to specific algorithms, prove to be inaccurate and obscure their true practical significance. In extreme cases, algorithms with poor performance may be inaccurately assessed positively by specific metrics that, in practice, do not reflect their true effectiveness and distort their evaluation.

When developing algorithms to win games, we have two main evaluation metrics that are simple and have empirical significance:

1. Whether the algorithm won or not.
2. If it won, how efficient its performance was.

## Implementing the Maze

The maze implementation utilizes the numpy library for game logic and the pygame library for the interface. The game features three distinct screens:

<p align="center">
    <img src="https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/home_screen.jpeg?raw=true" width="250" height="400">
</p>

The home screen presents a concealed grid, revealing only the maze's dimensions, alongside the **Play** button, which launches the game upon clicking. Additionally, there's an **i** button that directs you to the creator's gitHub profile.

<p align="center">
    <img src="https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/game_screen.jpeg?raw=true" width="250" height="400">
</p>

Upon starting the game, it showcases a timer while allowing users to navigate through the maze. The buttons above provide options to return to the initial screen, upgrade the maze for another round, or activate one of the solvers to triumph.

<p align="center">
    <img src="https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/winner_screen.jpeg?raw=true" width="250" height="400">
</p>

When you emerge victorious, the timer halts, and interaction with the maze grid and its related functions are disabled. The only available options are to return to the initial screen or update the grid for another round.

## A Dive into Maze Generation Algorithms

The maze grid is automatically generated using three algorithms.

### Depth-First Search
The randomized depth-first search algorithm explores the grid space randomly, prioritizing unvisited cells at each step. Its recursive nature facilitates efficient backtracking when no unvisited cells are available, ensuring thorough exploration. By introducing randomness into the direction selection process, the algorithm generates unique and intricate mazes.

### Prim's Algorithm
Prim's algorithm is favored for its efficiency and simplicity in maze generation. It begins by selecting point 0 as the starting point and incrementally expands the maze by adding paths, randomly selecting available edges from the set of unexplored cells. This process continues until all cells are connected, creating a complete maze without cycles.

### Kruskal's Algorithm
Kruskal's algorithm employs a disjoint set data structure to generate mazes (initially, each disjoint set has a single vertex, and the algorithm defines an auxiliary class with n representing the number of supernodes and v representing the parents). The maze generator inspired by a randomized version of Kruskal's algorithm represents the maze using an adjacency list, as the resulting graph is expected to be sparse. The resulting tree represents the maze, ensuring a unique path from the origin to the goal.

The behavior of the three distinct maze generation algorithms is depicted below:

<p align="center">
    <img src="https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/maze_generator_methods.gif?raw=true" width="600" height="400">
</p>

## Game Resolution Strategy

Given the partially observable task environment, where the agent perceives only immediate actions, complete action planning towards the goal isn't feasible. Utilizing online problem-solving strategies becomes imperative, where the agent formulates partial plans while executing actions.

The first solver implements an online version similar to depth-first search with backtracking, essential for traversing the state space and mapping the environment dynamically. Conversely, the second solver employs a learning real-time A* (LRTA*) approach, storing the "current best estimate" of reaching the goal from each visited state to guide the search instead of relying on randomization.

In this relatively simple task, the first solver demonstrates greater effectiveness. Considering the origin and goal positions, the optimal action execution sequence ('d', 'r', 'u', and 'l') contributes to its efficiency.

Adopting the average number of steps required to win the game across 100 random instances of each maze generator as the efficiency metric for the algorithms. It was observed that, overall, in this relatively simple task environment, the online depth-first search algorithm yielded better results across all three maze generators, particularly excelling with the generator utilizing depth-first search due to similarities in their constructions.

<p align="center">
    <img src="https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/comparison_search_methods.png?raw=true" width="600" height="400">
</p>

## Maze Pack Organization

```
maze/                               Top-level package
      __init__.py
      constants.py
      maze.py
      fiancee.py
      fiance_escape.py              It brings together the functionalities of the modules to implement the fiance escape
      media/                        Folder with the .png and .ogg files used in the game
              ...
      generators/                   Collect maze generators
              __init__.py
              dfs_generator.py
              prim_generator.py
              kruskal_generator.py
      solvers/                      Collect maze solvers        
              __init__.py
              constants.py
              odfs.py               Solver using online depth search strategy
              lrta.py               Solver using online search strategy with real-time learning A*
```

## Running the Game

Using some Linux distro and make sure you have [Python 3](https://www.python.org/) installed.

Clone the project:

```bash
  git clone https://github.com/filipemedeiross/solving_maze_by_online_search.git
```

Access the project directory:

```bash
  cd solving_maze_by_online_search
```

Creating a virtual environment (for the example we use the location directory parameter as `.venv`):

```bash
  python3 -m venv .venv
```

Activating the virtual environment:

```bash
  source .venv/bin/activate
```

Install all required packages specified in requirements.txt:

```bash
  pip install -r requirements.txt
```

Use the following command to run the game:

```bash
  python3 main.py
```

## References

Stuart Russell and Peter Norvig. **Artificial Intelligence: A Modern Approach**. 3rd ed., Pearson, 2009.

Numpy: <https://numpy.org/doc/stable/>

NetworkX: <https://networkx.org/documentation/stable/index.html>

Pygame: <https://www.pygame.org/docs/>

Images used: <https://opengameart.org/>
