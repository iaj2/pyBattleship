import pygame as p
import random
from battleship.AI.AI import AI
from battleship.constants import ROWS, COLS


class AI_EASY(AI):
    def __init__(self,board,opponent_board):
        self.all_spots = [(row, col) for row in range(ROWS) for col in range(COLS)]

        super().__init__(board, opponent_board)
    

    def turn(self):
        """
        picks a random location on the board to shoot
        """
        random_spot = random.choice(self.all_spots)
        self.all_spots.remove(random_spot)

        random_row, random_col = random_spot
        self.opponent_board.hit_ship(random_row, random_col)

        return True