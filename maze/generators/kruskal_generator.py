from numpy.random import shuffle


class UnionFind:
    def __init__(self, n):
        self.n = n
        self.v = list(range(n))

    def find(self, u):
        while u != self.v[u]:
            self.v[u] = self.v[self.v[u]]
            u = self.v[u]

        return u

    def union(self, u, v):
        root_u, root_v = self.find(u), self.find(v)

        if root_u == root_v:
            return False
        else:
            self.v[root_v] = root_u
            self.n -= 1

            return True

class KruskalMazeGenerator:
    def __init__(self, n=100):
        self.n = n
        self.shape = int(n**0.5)

        self.edges = self.generate_edges()

    def moves(self, v):
        moves = []

        if (v + 1) % self.shape:
            moves.append((v, v + 1))
        if v + self.shape < self.n:
            moves.append((v, v + self.shape))

        return moves

    def generate_edges(self):
        return [edge
                for v in range(self.n)
                for edge in self.moves(v)]

    def generate_maze(self):
        forest = UnionFind(self.n)
        maze   = [[] for _ in range(self.n)]

        shuffle(self.edges)

        for v, w in self.edges:
            if forest.union(v, w):
                maze[v].append(w)
                maze[w].append(v)

                if forest.n == 1:
                    return maze
