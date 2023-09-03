import pygame as p
from battleship.constants import ROWS,COLS
import random

class CPU():
    def __init__(self,board,opponent_board):
        self.board = board
        self.opponent_board = opponent_board
        self.prob_map = self.generate_prob_map()
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

    def turn(self):
        pass

    def generate_prob_map(self):
        

    



