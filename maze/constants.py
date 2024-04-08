# Settings
N = 100
SHAPE = int(N**0.5)
ELEM  = 2 * SHAPE + 1

FONT_TYPE  = 'tlwgtypo'
FONT_SIZE  = 20
FONT_COLOR = 0, 100, 0

BG_PATH           = 'maze/media/bg.png'
WIN_PATH          = 'maze/media/win.png'
PLAY_PATH         = 'maze/media/play.png'
INFO_PATH         = 'maze/media/info.png'
MAIN_PATH         = 'maze/media/main.png'
TIME_PATH         = 'maze/media/time.png'
SOLVE_PATH        = 'maze/media/solve.png'
UPDATE_PATH       = 'maze/media/update.png'
FIANCEE_PATH      = 'maze/media/fiancee.png'
WIN_MUSIC_PATH    = 'maze/media/win.ogg'
GAME_MUSIC_PATH   = 'maze/media/jungle_groove.ogg'
GROUND_TILES_PATH = 'maze/media/ground_tiles.png'

# Dimensions of screen elements
SIZE = WIDTH, HEIGHT = 480, 600

SPC = 20
SPC_BU = SPC // 2
GRID_LEFT = SPC
GRID_TOP  = HEIGHT // 8

MAZE_SIDE = WIDTH - 2 * GRID_LEFT
MAZE_SIZE = MAZE_SIDE, MAZE_SIDE

SIDE = MAZE_SIDE / ELEM
BUTTON_SIDE = 1.5 * SIDE
VIEW_SIDE = 3 * SIDE

WIN_SIZE    = MAZE_SIDE - 2 * GRID_LEFT, MAZE_SIDE // 5
VIEW_SIZE   = VIEW_SIDE, VIEW_SIDE
TIME_SIZE   = 2 * BUTTON_SIDE, BUTTON_SIDE
BLOCK_SIZE  = SIDE, SIDE
BUTTON_SIZE = BUTTON_SIDE, BUTTON_SIDE

# Definitions of the game's classes and objects
BUTTONS_BOT = GRID_TOP - SPC
WIN_POS     = 2 * GRID_LEFT, GRID_TOP + MAZE_SIDE // 5 * 2
FIANCEE_POS = int(GRID_LEFT + SIDE), int(GRID_TOP + SIDE)

FIANCEE_I = 3
FIANCEE_J = 4
FIANCEE_W = 48
FIANCEE_H = 64
FIANCEE_INIT = 4
FIANCEE_SPRITE = {'u' : 0,
                  'r' : 3,
                  'd' : 6,
                  'l' : 9}

DEST = {'l' : lambda rect, p: rect[p - 2].topleft,
        'r' : lambda rect, p: rect[p + 2].topleft,
        'u' : lambda rect, p: rect[p - 2*ELEM].topleft,
        'd' : lambda rect, p: rect[p + 2*ELEM].topleft}
