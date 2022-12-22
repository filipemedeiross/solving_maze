# For detailed implementation see: tests/maze_generator.ipynb
import numpy as np

class UnionFind:
    def __init__(self, n):
        self.n = n  # number of supernodes
        self.v = [i for i in range(n)]  # represents the parents (initially each disjoint set has a single vertex)

    def find(self, u):
        while u != self.v[u]:
            self.v[u] = self.v[self.v[u]]  # compression technique
            u = self.v[u]
            
        return u
    
    def union(self, u, v):
        root_u, root_v = self.find(u), self.find(v)
        
        if root_u == root_v:
            return False  # union was not performed
        else:
            self.v[root_v] = root_u
            self.n -= 1

            return True  # union was not performed

# Class for the maze generator
# Inspired by a randomized Kruskal algorithm
class KruskalMazeGenerator:
    def __init__(self, N=100):
        self.N = N  # number os cells (default is a 10x10 grid)
        
        self.walls = self.generate_walls()
        
    def new_maze(self):
        maze = [[] for _ in range(self.N)]  # data structure to store the maze
        
        # Copy the walls (edges) and create a set for each cell
        walls = self.walls.copy()
        forest = UnionFind(self.N)
        
        # Generate a maze (represented by an adjacency list)
        while forest.n > 1:
            v, w = walls.pop(np.random.randint(0, len(walls)))
            
            if forest.union(v, w):
                maze[v].append(w)  # adding (v,w) in the maze
                maze[w].append(v)  # adding (w,v) in the maze
                
        return maze
                
    @staticmethod
    def actions(N, v):
        maze_shape = int(N**0.5)

        actions = []
        if v % maze_shape != 0:
            actions.append((v, v-1))
        if (v+1) % maze_shape != 0:
            actions.append((v, v+1))
        if v >= maze_shape:
            actions.append((v, v-maze_shape))
        if v+maze_shape < N:
            actions.append((v, v+maze_shape))

        return actions  # possible actions in cell v

    def generate_walls(self):
        walls = []
        
        # Movement represents the existence or not of a wall
        for v in range(self.N):
            walls.extend(self.actions(self.N, v))

        return walls
