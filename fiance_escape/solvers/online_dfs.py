# For detailed testing see `tests/solvers_online.ipynb`

from collections import defaultdict

# Undo actions
undone = {'u' : 'd',
          'd' : 'u',
          'r' : 'l',
          'l' : 'r'}

# Class that represents the intelligent agent
class OnlineDFSAgent:
    def __init__(self):
        self.results = defaultdict(lambda: None)
        self.untried = defaultdict(list)
        self.unbacktracked = defaultdict(list)
        
        self.s = None
        self.a = None
        
    # The s_line argument is a percept that identifies the current state
    def step_online(self, maze, s_line):        
        if s_line not in self.untried:
            self.untried[s_line] = self.actions(maze, s_line)
            
        if self.s and s_line != self.results[self.s, self.a]:
            self.results[self.s, self.a] = s_line
            self.results[s_line, undone[self.a]] = self.s
            
            self.unbacktracked[s_line].append(undone[self.a])
        
        if self.untried[s_line]:
            self.a = self.untried[s_line].pop()
        elif self.unbacktracked[s_line]:
            self.a = self.unbacktracked[s_line].pop()
        else:
            return None
            
        self.s = s_line
        
        return self.a
            
    def actions(self, maze, pos):
        place = pos[0] + maze.shape*pos[1]
        
        actions = []
        
        if maze[place, place - maze.shape] and self.a != 'd':
            actions.append('u')
        if maze[place, place + 1] and self.a != 'l':
            actions.append('r')
        if maze[place, place + maze.shape] and self.a != 'u':
            actions.append('d')
        if maze[place, place - 1] and self.a != 'r':
            actions.append('l')

        return actions
