import pygame
from webbrowser import open

from .constants import *
from .maze import Maze
from .fiancee import Fiancee
from .solvers import OnlineDFSAgent, \
                     LRTAStar


class FianceeEscape:
    def __init__(self):
        # Initializing game logic
        self.maze    = Maze(N)
        self.fiancee = Fiancee(FIANCEE_POS)
        self.solver  = None

        # Instantiating the font, clock, screen and mixer
        pygame.init()

        self.font   = pygame.font.SysFont(FONT_TYPE, size=FONT_SIZE, bold=True)
        self.clock  = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SIZE)

        pygame.display.set_caption("Fiancee Escape")

        self.music_game = pygame.mixer.Sound(GAME_MUSIC_PATH)
        self.music_win  = pygame.mixer.Sound(WIN_MUSIC_PATH)
        self.channel_game = pygame.mixer.Channel(0)
        self.channel_win  = pygame.mixer.Channel(1)

        self.music_game.set_volume(0.5)

        # Defining the rects that will place the blocks on the screen
        self.rects = [pygame.Rect(GRID_LEFT + SIDE * j, GRID_TOP + SIDE * i, SIDE, SIDE)
                      for i in range(ELEM)
                      for j in range(ELEM)]

        self.dest = {'l' : lambda p: self.rects[p - 2].topleft,
                     'r' : lambda p: self.rects[p + 2].topleft,
                     'u' : lambda p: self.rects[p - 2*ELEM].topleft,
                     'd' : lambda p: self.rects[p + 2*ELEM].topleft}

        # Loading images used in the game
        self.load_bg(BG_PATH, GROUND_TILES_PATH)

        self.button_play = self.load_image(PLAY_PATH, BUTTON_SIZE)
        self.button_play_rect = self.button_play.get_rect(midtop=(WIDTH / 2, self.rects[-1].bottom + SPC))

        self.button_info = self.load_image(INFO_PATH, BUTTON_SIZE)
        self.button_info_rect = self.button_info.get_rect(bottomright=(WIDTH - GRID_LEFT, BUTTONS_TOP))

        self.button_return = self.load_image(MAIN_PATH, BUTTON_SIZE)
        self.button_return_rect = self.button_return.get_rect(bottomleft=(GRID_LEFT, BUTTONS_TOP))

        self.button_update = self.load_image(UPDATE_PATH, BUTTON_SIZE)
        self.button_update_rect = self.button_update.get_rect(topleft=(self.button_return_rect.right + SPC_BU,
                                                                       self.button_return_rect.top))

        self.button_solve = self.load_image(SOLVE_PATH, BUTTON_SIZE)
        self.button_solve_rect = self.button_solve.get_rect(topleft=(self.button_update_rect.right + SPC_BU,
                                                                        self.button_update_rect.top))

        self.button_solve_2 = self.load_image(SOLVE_PATH, BUTTON_SIZE)
        self.button_solve_2_rect = self.button_solve_2.get_rect(topleft=(self.button_solve_rect.right + SPC_BU,
                                                                            self.button_solve_rect.top))

        self.button_time = self.load_image(TIME_PATH, TIME_SIZE)
        self.button_time_rect = self.button_time.get_rect(center=self.button_play_rect.center)

        self.button_win = self.load_image(WIN_PATH, WIN_SIZE)
        self.button_win_rect = self.button_win.get_rect(topleft=WIN_POS)

    def init_game(self):
        while True:
            self.update()

            self.main_screen()
            self.play()

    def main_screen(self):
        # Preparing the main screen
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.button_info, self.button_info_rect)
        self.screen.blit(self.button_play, self.button_play_rect)

        pygame.display.flip()  # displaying the screen

        while True:
            # Getting input from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)  # leaving the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play_rect.collidepoint(event.pos):
                        return
                    if self.button_info_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

    def play(self):
        # Update the clock
        self.clock.tick()
        time = 0

        # Displaying fixed screen elements
        self.screen.blit(self.background, (0, 0))  # overriding home screen buttons

        self.screen.blit(self.button_return, self.button_return_rect)
        self.screen.blit(self.button_update, self.button_update_rect)
        self.screen.blit(self.button_solve, self.button_solve_rect)
        self.screen.blit(self.button_solve_2, self.button_solve_2_rect)

        self.display_grid()
        self.screen.blit(self.fiancee.image, self.fiancee.rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_return_rect.collidepoint(event.pos):
                        return
                    if self.button_update_rect.collidepoint(event.pos):
                        self.update()  # update the game

                        self.clock.tick()
                        time = 0

                        self.display_grid()
                        self.screen.blit(self.fiancee.image, self.fiancee.rect)

                if not self.maze.won(self.fiancee.x, self.fiancee.y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_solve_rect.collidepoint(event.pos):
                            self.solver = OnlineDFSAgent()
                        if self.button_solve_2_rect.collidepoint(event.pos):
                            self.solver = LRTAStar()

                    if self.solver:
                        while not self.maze.won(self.fiancee.x, self.fiancee.y):
                            place = self.grid_to_place(self.fiancee.x, self.fiancee.y)  # represents the place on the grid
                            action = self.solver.step_online(self.maze, self.fiancee.xy)

                            self.fiancee.move(action)
                            self.move_fiancee(action, place)
                    elif event.type == pygame.KEYDOWN:
                        pos = self.fiancee.x + self.fiancee.y*SHAPE  # represents the vertex
                        place = self.grid_to_place(self.fiancee.x, self.fiancee.y)  # represents the place on the grid

                        action = None

                        if event.key == pygame.K_UP and self.maze[pos, pos-SHAPE]:
                            action = 'u'
                        elif event.key == pygame.K_DOWN and self.maze[pos, pos+SHAPE]:
                            action = 'd'
                        elif event.key == pygame.K_RIGHT and self.maze[pos, pos + 1]:
                            action = 'r'
                        elif event.key == pygame.K_LEFT and self.maze[pos, pos - 1]:
                            action = 'l'

                        if action:
                            self.fiancee.move(action)
                            self.move_fiancee(action, place)

                    if self.maze.won(self.fiancee.x, self.fiancee.y):
                        self.screen.blit(self.button_win, self.button_win_rect)

                        self.channel_game.stop()
                        self.channel_win.play(self.music_win)
                    
            if not self.maze.won(self.fiancee.x, self.fiancee.y):
                # Game time
                time += self.clock.tick(10)
                self.display_time(time)

            pygame.display.flip()

    def load_bg(self, filename, tiles):
        tiles = pygame.image.load(tiles)

        self.path = pygame.transform.scale(tiles.subsurface((64, 0), (64, 64)), BLOCK_SIZE)
        self.wall = pygame.transform.scale(tiles.subsurface((128, 64), (64, 64)), BLOCK_SIZE)
        self.limit = pygame.transform.scale(tiles.subsurface((0, 64), (64, 64)), BLOCK_SIZE)
        self.unknown = pygame.transform.scale(tiles.subsurface((320, 0), (64, 64)), BLOCK_SIZE)

        background = pygame.transform.scale(pygame.image.load(filename), SIZE)

        background.blit(pygame.transform.scale(self.path.copy(), maze_shape), self.rects[0].topleft)

        for rect in self.rects:
            background.blit(self.unknown, rect.topleft)

        self.background = background

    def load_maze(self):
        # Maze background
        self.maze_surface = pygame.transform.scale(self.path.copy(), SIZE)

        # Grid limits (superior and inferior)
        last_line = ELEM*(ELEM-1)
        for i in range(ELEM):
            self.maze_surface.blit(self.limit, self.rects[i])
            self.maze_surface.blit(self.limit, self.rects[i + last_line])

        # Grid limits (side)
        for j in range(1, ELEM-2):
            self.maze_surface.blit(self.limit, self.rects[j*ELEM])            
            self.maze_surface.blit(self.limit, self.rects[j*ELEM + ELEM - 1])

        self.maze_surface.blit(self.limit, self.rects[last_line - ELEM])            
        self.maze_surface.blit(self.path, self.rects[last_line - 1])

        # Checking and displaying elements of the graph representing the maze
        for j in range(SHAPE):
            for i in range(SHAPE):
                i_pos, j_pos = self.grid_to_rect(i, j)

                self.maze_surface.blit(self.path, self.rects[j_pos*ELEM + i_pos])

                if (i != SHAPE-1):
                    if (self.maze[j*SHAPE + i, j*SHAPE + i + 1]):
                        self.maze_surface.blit(self.path, self.rects[j_pos*ELEM + i_pos + 1])
                    else:
                        self.maze_surface.blit(self.wall, self.rects[j_pos*ELEM + i_pos + 1])

                    if (j != SHAPE-1):
                        self.maze_surface.blit(self.wall, self.rects[(j_pos+1)*ELEM + i_pos + 1])

                if (j != SHAPE-1):
                    if (self.maze[j*SHAPE + i, (j+1)*SHAPE + i]):
                        self.maze_surface.blit(self.path, self.rects[(j_pos+1)*ELEM + i_pos])
                    else:
                        self.maze_surface.blit(self.wall, self.rects[(j_pos+1)*ELEM + i_pos])

    def display_grid(self):
        ref_pos = self.fiancee.rect.left - SIDE, self.fiancee.rect.top - SIDE

        # Hiding the area of the maze and showing known part
        self.screen.blit(self.background, self.rects[0].topleft, (self.rects[0].topleft, maze_shape))
        self.screen.blit(self.maze_surface, ref_pos, (ref_pos, view_size))

    def move_fiancee(self, move, place):
        topleft = self.dest[move](place)

        while self.fiancee.rect.topleft != topleft:
            self.fiancee.update(move)
            self.display_grid()
            self.screen.blit(self.fiancee.image, self.fiancee.rect)

            pygame.display.flip()

    def display_time(self, time):
        time_text = self.font.render(f'{time // 1000 // 60}:{time // 1000 % 60}',
                                     True, FONT_COLOR)

        left = self.button_time_rect.centerx - time_text.get_width() / 2
        top = self.button_time_rect.centery - time_text.get_height() / 2

        self.screen.blit(self.button_time, self.button_time_rect)
        self.screen.blit(time_text, (left, top))

    def update(self):
        self.maze.update_maze()  # update the grid
        self.fiancee.reset()  # reset the fiance
        self.solver = None  # reset the solver
        self.load_maze()  # update the maze

        # Game background music
        if not self.channel_game.get_busy():
            self.channel_game.play(self.music_game, -1)
            
    @staticmethod
    def grid_to_rect(x, y):
        return (1 + 2*x, 1 + 2*y)  # transforms the (x, y) to the grid of rects

    def grid_to_place(self, x, y):
        x_pos, y_pos = self.grid_to_rect(x, y)

        return x_pos + y_pos*ELEM

    @staticmethod
    def load_image(path, size):
        return pygame.transform.scale(pygame.image.load(path), size)
