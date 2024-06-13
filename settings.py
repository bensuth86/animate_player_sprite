from os import path

repos = r"C:\Users\ben_s\Documents\Python_Scripts\Pygame_Templates\animate_player_sprite"  # working directory

# game options/settings
TITLE = "Animate player"
TILESIZE = 36  # length in pixels
WIDTH = TILESIZE * 32  # screen width in tiles
HEIGHT = TILESIZE * 18  # screen height in tiles
FPS = 60

# Background
BACKGROUND = path.join(repos, "Images", "UnderwaterBackground.png")

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player properties
PLAYER_WIDTH = 1 * TILESIZE
PLAYER_HEIGHT = 2 * TILESIZE

# Animations #

