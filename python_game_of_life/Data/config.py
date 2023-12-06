import numpy as np
import pygame

# SCREEN DIMENSIONS
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

# BUTTON DIMENSIONS
button_width, button_height = 150, 40
button_spacing = 5

# GRID DIMENSIONS:
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y
