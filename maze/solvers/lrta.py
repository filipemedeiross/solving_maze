from collections import defaultdict


class LRTAStar:
    def __init__(self):
        self.R = defaultdict(lambda: None)
        self.H = dict()

        self.s = None
        self.a = None

    def step_online(self, maze, s):
        shape = maze.shape - 1

        if s not in self.H:
            self.H[s] = self.dist(shape, *s)
        if self.s:
            self.R[self.s, self.a] = s
            self.H[self.s] = min(self.cost(shape, self.s, self.R[self.s, act])
                                 for act in self.actions(maze, self.s))

        self.s = s
        self.a = min([act for act in self.actions(maze, s)],
                     key=lambda act: self.cost(shape, s, self.R[s, act]))        

        return self.a

    def actions(self, maze, p):
        actions = []

        place = p[0] + maze.shape*p[1]

        if maze[place, place-1]:
            actions.append('l')
        if maze[place, place+1]:
            actions.append('r')
        if maze[place, place-maze.shape]:
            actions.append('u')
        if maze[place, place+maze.shape]:
            actions.append('d')

        return actions

    def cost(self, shape, s, s_):
        return 1 + self.H[s_] \
               if s_          \
               else self.dist(shape, *s)

    @staticmethod
    def dist(shape, x, y):
        return (shape - x) + (shape - y)
