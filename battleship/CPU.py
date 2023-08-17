import pygame as p
from battleship.constants import ROWS,COLS
import random

class CPU():
    def __init__(self,board,opponent_board):
        self.board = board
        self.opponent_board = opponent_board
        self.mode = 'hunt'
        self.first_hit_on_ship = False
        self.hit_ship_orientation = None
        self.valid_moves = self._get_valid_moves()
        self.valid_adj_moves = []
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

    def _get_valid_moves(self):
        moves = []
        for row in range(0,ROWS):
            for col in range(0,COLS):
                moves.append((row,col))
        return moves
    
    def _get_valid_adj_moves(self,row,col):
        col_up = col -1  if col -1 >=0 else None
        col_down = col + 1 if col + 1 < COLS else None
        row_left = row -1  if row -1 >=0 else None
        row_right = row + 1 if row + 1 < ROWS else None
        if col_up is not None:
            if self.opponent_board.board[row][col_up] != -1 or self.opponent_board.board[row][col_up] != 1:
                self.valid_adj_moves.append((row,col_up))
        if col_down is not None:
            if self.opponent_board.board[row][col_down] != -1 or self.opponent_board.board[row][col_down] != 1:
                self.valid_adj_moves.append((row,col_down))
        if row_left is not None:
            if self.opponent_board.board[row_left][col] != -1 or self.opponent_board.board[row_left][col] != 1:
                self.valid_adj_moves.append((row_left,col))
        if row_right is not None:
            if self.opponent_board.board[row_right][col] != -1 or self.opponent_board.board[row_right][col] != 1:
                self.valid_adj_moves.append((row_right, col))
        


    def turn(self):
        if not self.valid_adj_moves:
                self.mode = 'hunt'
        if self.mode == 'hunt':
            return self.hunt()
        elif self.mode == 'target':
            return self.target()

        print(self.mode)

    def hunt(self):
        success = True
        # Get random move from valid moves list
        shot_pos = random.choice(self.valid_moves)
        row,col = shot_pos
        # Remove valid move from valid moves list
        self.valid_moves.remove(shot_pos)
        _, hit = self.opponent_board.hit_ship(row,col)
        # Check if a ship was hit. If so switch to target mode
        if hit:
            self.mode = 'target'
            self._get_valid_adj_moves(row, col)
        return success


    def target(self):
        success = False
        # Get random move from valid adj moves list
        shot_pos = random.choice(self.valid_adj_moves)
        row,col = shot_pos
        valid,hit = self.opponent_board.hit_ship(row,col)
        self.valid_adj_moves.remove(shot_pos)
        if valid:
            if hit:
                self.valid_adj_moves = []
                self._get_valid_adj_moves(row,col)
    
            self.valid_moves.remove(shot_pos)
            success = True

        #print(self.valid_adj_moves)

        return success



