import numpy as np
from .generators import KruskalMazeGenerator


# Class responsible for the maze
# Default is a 10x10 grid
class Maze:
    def __init__(self, N=100):  # creates a new grid representing a maze
        self.__N = N
        self.__maze_shape = int(N**0.5)

        self.__generator = KruskalMazeGenerator(self.__N)
        
        self.__grid = self.__generator.new_maze()

    def __getitem__(self, move):
        if isinstance(move, tuple) and len(move) == 2:
            return move[0] in self.__grid[move[1]]

        return None

    def won(self, x, y):
        return x == self.__maze_shape-1 and y == self.__maze_shape-1

    def update_maze(self):
        self.__grid = self.__generator.new_maze()

    @property
    def grid(self):
        return self.__grid
