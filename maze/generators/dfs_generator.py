from collections import deque
from numpy.random import shuffle


class DFSMazeGenerator:
    def __init__(self, n=100):
        self.n = n
        self.shape = int(n**0.5)

        self.edges = self.generate_edges()

    def moves(self, v):
        moves = []

        if v % self.shape:
            moves.append(v - 1)
        if (v + 1) % self.shape:
            moves.append(v + 1)
        if v >= self.shape:
            moves.append(v - self.shape)
        if v < self.n - self.shape:
            moves.append(v + self.shape)

        return moves

    def generate_edges(self):
        return [self.moves(v)
                for v in range(self.n)]

    def shuffle_edges(self):
        edges = self.generate_edges()
        for adj in edges:
            shuffle(adj)

        return edges

    def generate_maze(self):
        maze = [[] for _ in range(self.n)]

        stack  = deque([])
        explored = set([])
        frontier = self.shuffle_edges()

        v = 0
        explored.add(v)
        while True:
            while not frontier[v]:
                if not stack:
                    return maze

                v = stack.pop()

            w = frontier[v].pop()

            if w not in explored:
                maze[v].append(w)
                maze[w].append(v)

                stack.append(v)
                explored.add(w)
                v = w
