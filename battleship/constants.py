import pygame as p
from enum import Enum, unique

# SCREEN/BOARDS
WIDTH,HEIGHT = 600,800
ROWS,COLS = 6,10
TOP_PADDING,MIDDLE_PADDING,BOTTOM_PADDING= 70,60,70 #Should not exceed height in total
SIDE_PADDING = 50
CELL_SIZE = 50
BOARDHEIGHT = CELL_SIZE*ROWS
BOARDWIDTH = CELL_SIZE*COLS

# SHIPS
SHIP_SIZES = [5,4,3,3,2]
TOTAL_SHIPS  = 5

# IMAGES
SHIP_FN = p.image.load("Assets\Ship_FireNation.png")
SHIP_EK = p.image.load("Assets\Ship_EarthKingdom.png")
CELL_IMAGE = p.image.load("Assets\water.png")
SETUP_GAME_START_IMG = p.image.load("Assets\start_in_game.png")
RESTART_IMG = p.image.load("Assets\\restart.png")
YOU_WIN_IMG = p.image.load("Assets\you_win.png")
YOU_LOSE_IMG = p.image.load("Assets\you_lose.png")


# COLORS
BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
BLUE_DARKER = "#30C3FE"
BLUE_LIGHT = "#58C5F4"
GREEN = "#41FF63"

# GAME STATES
@unique
class GameState(Enum):
    MAIN_MENU = 0
    SETUP = 1
    MAIN_GAME = 2
    END = 3

@unique
class Tile(Enum):
    MISS = 0
    OPEN = 1
    HIT = 2

@unique
class BoardType(Enum):
    Player = 1
    CPU = 2

@unique 
class GameTurn(Enum):
    Player = 1
    CPU = 2