# For detailed testing see `tests/solvers_online.ipynb`

from collections import defaultdict

class LRTAStar:
    def __init__(self):
        self.results = defaultdict(lambda: None)
        self.H = dict()
        
        self.s = None
        self.a = None
        
    # The s_line argument is a percept that identifies the current state
    def step_online(self, maze, s_line):
        if s_line not in self.H:
            self.H[s_line] = self.manhattan(maze, *s_line)
            
        if self.s:
            self.results[self.s, self.a] = s_line
            
            self.H[self.s] = min([self.LRTA_cost(maze, self.s, self.results[self.s, b])
                                  for b in self.actions(maze, self.s)])
            
        self.s = s_line
        self.a = min([b for b in self.actions(maze, s_line)],
                     key=lambda b: self.LRTA_cost(maze, s_line, self.results[s_line, b]))        
        
        return self.a
            
    def actions(self, maze, pos):
        place = pos[0] + maze.shape*pos[1]
        
        actions = []
        
        if maze[place, place + maze.shape]:
            actions.append('d')
        if maze[place, place + 1]:
            actions.append('r')
        if maze[place, place - 1]:
            actions.append('l')
        if maze[place, place - maze.shape]:
            actions.append('u')

        return actions
    
    def LRTA_cost(self, maze, s, s_line):
        return self.H[s_line] + 1 if s_line else self.manhattan(maze, *s)
    
    @staticmethod
    def manhattan(maze, x, y):
        return abs(x - (maze.shape-1)) + abs(y - (maze.shape-1))  # manhattan heuristic