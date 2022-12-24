# Defining the constants

# Game settings
N = 100
shape = int(N**0.5)

# Colors
COLOR_FONT = 0, 100, 0

# Dimensions
size = width, height = 480, 600

# Indent
grid_top = height // 8
grid_left = 20
spacing_buttons = 20

# Dimensions of screen elements
font_size = 20

maze_area = width - 2*grid_left
maze_shape = maze_area, maze_area
n_elem = 2*shape + 1

block_side = maze_area / n_elem
button_side = 1.5*block_side
view_side = 3*block_side

block_size = block_side, block_side
button_size = button_side, button_side
view_size = view_side, view_side

# Location of movements in sprites_sheets
sprite_fiancee = {'u' : 0, 'd' : 6, 'r' : 3, 'l' : 9}