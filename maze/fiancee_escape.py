import pygame
from pygame.image import load
from pygame.transform import scale
from webbrowser import open

from .constants import *
from .maze import Maze
from .fiancee import Fiancee
from .solvers import OnlineDFSAgent, \
                     LRTAStar


class FianceeEscape:
    def __init__(self):
        # Initializing game logic and defining the rects
        self.maze    = Maze(N)
        self.fiancee = Fiancee(FIANCEE_POS)
        self.solver  = None

        self.rects = [pygame.Rect((GRID_LEFT + SIDE * j, GRID_TOP + SIDE * i), BLOCK_SIZE)
                      for i in range(ELEM)
                      for j in range(ELEM)]

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

        self.music_game.set_volume(0.6)

        # Loading images used in the game
        self.load_tiles(TILES_PATH)
        self.load_bg(BG_PATH)

        self.button_play = self.load_image(PLAY_PATH, BUTTON_SIZE)
        self.button_play_rect = self.button_play.get_rect(midtop=(WIDTH / 2, self.rects[-1].bottom + SPC))

        self.button_info = self.load_image(INFO_PATH, BUTTON_SIZE)
        self.button_info_rect = self.button_info.get_rect(bottomright=(WIDTH - GRID_LEFT, BUTTONS_BOT))

        self.button_return = self.load_image(MAIN_PATH, BUTTON_SIZE)
        self.button_return_rect = self.button_return.get_rect(bottomleft=(GRID_LEFT, BUTTONS_BOT))

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
            self.main_screen()
            self.play()

    def main_screen(self):
        self.update()
        self.display_main_screen()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
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
        self.screen.blit(self.bg, (0, 0))  # overriding home screen buttons

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

    def update(self):
        self.maze.reset()
        self.fiancee.reset()
        self.solver = None

        self.load_maze()

        if not self.channel_game.get_busy():
            self.channel_game.play(self.music_game, -1)

    def display_main_screen(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.button_info, self.button_info_rect)
        self.screen.blit(self.button_play, self.button_play_rect)

        pygame.display.flip()

    def display_grid(self):
        ref_pos = self.fiancee.rect.left - SIDE, self.fiancee.rect.top - SIDE

        # Hiding the area of the maze and showing known part
        self.screen.blit(self.bg, self.rects[0].topleft, (self.rects[0].topleft, MAZE_SIZE))
        self.screen.blit(self.maze_surface, ref_pos, (ref_pos, VIEW_SIZE))

    def display_time(self, time):
        time_text = self.font.render(f'{time // 1000 // 60}:{time // 1000 % 60}',
                                     True, FONT_COLOR)

        left = self.button_time_rect.centerx - time_text.get_width() / 2
        top = self.button_time_rect.centery - time_text.get_height() / 2

        self.screen.blit(self.button_time, self.button_time_rect)
        self.screen.blit(time_text, (left, top))

    def move_fiancee(self, move, place):
        topleft = DEST[move](self.rects, place)

        while self.fiancee.rect.topleft != topleft:
            self.fiancee.update(move)
            self.display_grid()
            self.screen.blit(self.fiancee.image, self.fiancee.rect)

            pygame.display.flip()

    def load_tiles(self, tiles_path):
        tiles = self.load_image(tiles_path)

        self.path    = scale(tiles.subsurface(( 64,  0), (64, 64)), BLOCK_SIZE)
        self.wall    = scale(tiles.subsurface((128, 64), (64, 64)), BLOCK_SIZE)
        self.limit   = scale(tiles.subsurface((  0, 64), (64, 64)), BLOCK_SIZE)
        self.unknown = scale(tiles.subsurface((320,  0), (64, 64)), BLOCK_SIZE)

    def load_bg(self, bg_path):
        self.bg = self.load_image(bg_path, SIZE)

        self.bg.blit(scale(self.path, MAZE_SIZE), MAZE_POS)
        for rect in self.rects:
            self.bg.blit(self.unknown, rect.topleft)

    def load_maze(self):
        # Maze background
        self.maze_surface = scale(self.path.copy(), SIZE)

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

    def grid_to_place(self, x, y):
        x_, y_ = self.grid_to_rect(x, y)

        return x_ + ELEM * y_

    @staticmethod
    def grid_to_rect(x, y):
        return 2 * x + 1, 2 * y + 1

    @staticmethod
    def load_image(path, size=None):
        img = load(path)
        if size:
            img = scale(img, size)

        return img
