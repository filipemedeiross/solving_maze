# Defining the constants

# Game settings
N = 100
shape = int(N**0.5)

# Colors
COLOR_FONT = 0, 0, 0

# Dimensions
size = width, height = 480, 600

# Indent
grid_top = height // 8
grid_left = 20
spacing_buttons = 20

# Dimensions of screen elements
font_size = 20

maze_area = width - 2*grid_left
n_elem = 2*shape + 1

block_side = maze_area / n_elem
block_size = block_side, block_side
button_size = 1.5*block_side, 1.5*block_side
