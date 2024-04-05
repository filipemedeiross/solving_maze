from random import choice
from .generators import DFSMazeGenerator,  \
                        PrimMazeGenerator, \
                        KruskalMazeGenerator


class Maze:
    def __init__(self, n=100):
        self.n = n
        self.shape = int(n**0.5)

        self.generator = choice([DFSMazeGenerator,
                                 PrimMazeGenerator,
                                 KruskalMazeGenerator])(n)

        self.update_maze()

    def __getitem__(self, move):
        pre, pos = move

        if 0 <= pos < self.n:
            return pre in self.grid[pos]

        return False

    def update_maze(self):
        self.grid = self.generator.generate_maze()

    def won(self, x, y):
        return x == y == self.shape-1
