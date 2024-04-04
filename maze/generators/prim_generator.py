from numpy.random import randint


class PrimMazeGenerator:
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

    def generate_maze(self):
        maze = [[] for _ in range(self.n)]

        V = [True ] + \
            [False] * (self.n - 1)
        E = [(0, w) for w in self.edges[0]]

        n = 1
        while n < self.n:
            v, w = E.pop(randint(0, len(E)))

            if not V[w]:
                maze[v].append(w)
                maze[w].append(v)

                V[w] = True
                for w2 in self.edges[w]:
                    if not V[w2]:
                        E.append((w, w2))

                n += 1

        return maze
