import numpy as np
import random
from abc import ABC, abstractmethod
from battleship.constants import ROWS, COLS

class AI(ABC):
    def __init__(self,board,opponent_board):
        self.board = board
        self.opponent_board = opponent_board
        self.opponent_board_fixed = []
        self.opponent_shot_map = np.zeros((6, 10))
        self.opponent_ships = None
        self.ship_tiles_hit = 0
        self.setup_board()


    def setup_board(self):
        # Setup Ships in random places on board 
        for ship in self.board.ships:
            placed = False
            # Randomly rotate
            rotate = random.choice([True,False])
            while not placed:
                # Keep trying to move and place ship
                row = random.randint(0,ROWS-1)
                col = random.randint(0,COLS-1)
                ship.move(row,col)
                if self.board.place_ship(ship):
                    # Keep trying to rotate ship
                    if not rotate:
                        placed = True
                    if self.board.rotate_ship(ship):
                        placed = True

    def set_fixed_opponent_board(self):
        for row in range(ROWS):
            self.opponent_board_fixed.append([])
            for col in range(COLS):
                self.opponent_board_fixed[row].append(self.opponent_board.board[row][col])


    @abstractmethod
    def turn(self):
        pass