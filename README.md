<h1>SOLVING MAZE BY ONLINE SEARCH</h1>

## Implementing the "Fiance escape" 

The maze was implemented using the numpy library for the game logic and the pygame library for the interface. The maze grid is generated automatically through a generator inspired by a randomized version of Kruskal's algorithm in which the resulting tree represents the maze (so it has a unique path from the origin to the goal).

The game has three screens explained below:

![Home Screen](https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/home_screen.jpeg?raw=true)

The home screen displays a hidden grid (only allowing you to observe the dimensions of the maze) and the **Play** button that launches the game when clicked. It also has an **i** button that takes you to the creator's github profile.

![Game Screen](https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/game_screen.jpeg?raw=true)

When starting the game, it displays the time count while allowing the user to go through the maze. The buttons above allow the user to return to the initial screen or activate one of the solvers to win the game.

![Winner Screen](https://github.com/filipemedeiross/solving_maze_by_online_search/blob/main/examples/winner_screen.jpeg?raw=true)

When you win the game, time is paused and interaction with the maze grid and related functions are disabled, leaving only the function to return to the initial screen.

## Resolution Strategy Implemented in the Game

Considering that the task environment is partially observable (fiancee perceives only the actions immediately following her position), the intelligent agent cannot assemble a complete action plan towards the goal and then carry it out. It is necessary to use online problem solving strategies, that is, strategies in which the intelligent agent elaborates partial plans while executing actions.

The first solver implements an online version analogous to depth-first search with backtracking (backtracking is necessary because the agent is traversing the state space while performing the search and builds a map of the environment), while the second solver implements a scheme called learning real-time A* (LRTA*) in which a “current best estimate” of the cost to reaching the goal from each visited state is stored and this value is used to guide the search instead of randomization.

For this relatively simple task, the first solver proved to be more effective since, considering the origin and goal positions, the execution order of the actions is the most efficient ('d', 'r', 'u' and 'l').

## `fiance_escape` Pack Organization
```
fiance_escape/                      Top-level package
      __init__.py
      constants.py
      maze.py
      fiancee.py
      fiancee_escape.py             It brings together the functionalities of the modules to implement the fiance escape
      media/                        Folder with the .png and .ogg files used in the game
              ...
      generators/                   Can be extended with different maze generators
              __init__.py
              kruskal_generator.py  Implements the maze generator
      solvers/                      Collect maze solvers        
              __init__.py
              online_dfs.py         Solver using online depth search strategy
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

Norvig, Peter. Inteligência Artificial. Grupo GEN, 2013.

Images and sounds used: <https://opengameart.org/>

Numpy: <https://numpy.org/doc/stable/>

Pygame: <https://www.pygame.org/docs/>
