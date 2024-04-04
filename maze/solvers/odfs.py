from .constants import *
from collections import defaultdict


class OnlineDFSAgent:
    def __init__(self):
        self.result  = defaultdict(lambda: None)
        self.untried = defaultdict(list)
        self.unback  = defaultdict(list)

        self.s = None
        self.a = None

    def step_online(self, maze, s):
        if s not in self.untried:
            self.untried[s] = self.actions(maze, s)

        if self.s and s != self.result[self.s, self.a]:
            self.result[self.s, self.a]    = s
            self.result[s, UNDONE[self.a]] = self.s

            self.unback[s].append(UNDONE[self.a])

        self.s = s
        if self.untried[s]:
            self.a = self.untried[s].pop()
        elif self.unback[s]:
            self.a = self.unback[s].pop()
        else:
            self.a = None

        return self.a

    def actions(self, maze, p):
        actions = []

        pos = p[0] + maze.shape*p[1]

        if self.a != 'r' and maze[pos, pos-1]:
            actions.append('l')
        if self.a != 'l' and maze[pos, pos+1]:
            actions.append('r')
        if self.a != 'd' and maze[pos, pos-maze.shape]:
            actions.append('u')
        if self.a != 'u' and maze[pos, pos+maze.shape]:
            actions.append('d')

        return actions
