import numpy as np
from .generators import KruskalMazeGenerator


# Class responsible for the maze
# Default is a 10x10 grid
class Maze:
    def __init__(self, N=100):  # creates a new grid representing a maze
        self.__N = N
        self.__shape = int(N**0.5)

        self.__generator = KruskalMazeGenerator(self.__N)
        self.__grid = self.__generator.new_maze()

    # Checks for the existence of an edge between two vertices
    def __getitem__(self, move):
        if isinstance(move, tuple) and len(move) == 2:
            pre, pos = move

            if 0 <= pos <= self.N-1:
                return pre in self.grid[pos]
            else:
                return False

        return None

    def won(self, x, y):
        return x == self.shape-1 and y == self.shape-1

    def update_maze(self):
        self.__grid = self.__generator.new_maze()

    @property
    def N(self):
        return self.__N

    @property
    def shape(self):
        return self.__shape

    @property
    def grid(self):
        return self.__grid
