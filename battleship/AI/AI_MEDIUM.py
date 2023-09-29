import pygame as p
import random
from battleship.AI.AI import AI
from battleship.constants import ROWS, COLS
from battleship.ship import Ship


class AI_MEDIUM(AI):
    def __init__(self,board,opponent_board):
        self.all_spots = [(row, col) for row in range(ROWS) for col in range(COLS)]
        self.adj_spots = []
        super().__init__(board, opponent_board)
    
    def _append_adj_spots(self, row, col):
        """adds possible adjascent spots to adjascent spots list"""
        if (row-1,col) in self.all_spots:
            self.adj_spots.append((row-1, col))
        if (row+1,col) in self.all_spots:
           self.adj_spots.append((row+1, col))
        if (row,col-1) in self.all_spots:
            self.adj_spots.append((row, col-1))
        if (row,col+1) in self.all_spots:
            self.adj_spots.append((row, col+1))


    def _target(self):
        """
        hits squares adjascent to a location where a ship has been hit
        """
        pos = self.adj_spots.pop()

        row,col = pos

        _,ship_got_hit,_ = self.opponent_board.hit_ship(row,col)

        self.all_spots.remove(pos)



        if ship_got_hit:
            # Remove the other adjascent spots
            while self.adj_spots:
                self.adj_spots.pop()
            self.ship_tiles_hit += 1
            self._append_adj_spots(row,col)

    def _hunt(self):
        """
        picks a random location on the board to shoot
        """
        random_spot = random.choice(self.all_spots)
        self.all_spots.remove(random_spot)

        random_row, random_col = random_spot
        _,ship_got_hit,_ = self.opponent_board.hit_ship(random_row, random_col)

        if ship_got_hit:
            self.ship_tiles_hit += 1
            self._append_adj_spots(random_row, random_col)

    def turn(self):
        print(self.all_spots)
        if not self.adj_spots:
            self._hunt()
        else:
            self._target()
        
        return True
    
   
    # def _get_valid_adj_moves(self,row,col):
    #     col_up = col -1  if col -1 >=0 else None
    #     col_down = col + 1 if col + 1 < COLS else None
    #     row_left = row -1  if row -1 >=0 else None
    #     row_right = row + 1 if row + 1 < ROWS else None
    #     if col_up is not None:
    #         if self.opponent_board.board[row][col_up] != -1 or self.opponent_board.board[row][col_up] != 1:
    #             self.valid_adj_moves.append((row,col_up))
    #     if col_down is not None:
    #         if self.opponent_board.board[row][col_down] != -1 or self.opponent_board.board[row][col_down] != 1:
    #             self.valid_adj_moves.append((row,col_down))
    #     if row_left is not None:
    #         if self.opponent_board.board[row_left][col] != -1 or self.opponent_board.board[row_left][col] != 1:
    #             self.valid_adj_moves.append((row_left,col))
    #     if row_right is not None:
    #         if self.opponent_board.board[row_right][col] != -1 or self.opponent_board.board[row_right][col] != 1:
    #             self.valid_adj_moves.append((row_right, col))
       


    # def turn(self):
    #     if not self.valid_adj_moves:
    #             self.mode = 'hunt'
    #     if self.mode == 'hunt':
    #         return self.hunt()
    #     elif self.mode == 'target':
    #         return self.target()

    #     print(self.mode)

    # def hunt(self):
    #     success = True
    #     # Get random move from valid moves list
    #     shot_pos = random.choice(self.valid_moves)
    #     row,col = shot_pos
    #     # Remove valid move from valid moves list
    #     self.valid_moves.remove(shot_pos)
    #     _, hit = self.opponent_board.hit_ship(row,col)
    #     # Check if a ship was hit. If so switch to target mode
    #     if hit:
    #         self.mode = 'target'
    #         self._get_valid_adj_moves(row, col)
    #     return success


    # def target(self):
    #     success = False
    #     # Get random move from valid adj moves list
    #     shot_pos = random.choice(self.valid_adj_moves)
    #     row,col = shot_pos
    #     valid,hit = self.opponent_board.hit_ship(row,col)
    #     self.valid_adj_moves.remove(shot_pos)
    #     if valid:
    #         if hit:
    #             self.valid_adj_moves = []
    #             self._get_valid_adj_moves(row,col)
   
    #         self.valid_moves.remove(shot_pos)
    #         success = True

    #     #print(self.valid_adj_moves)

    #     return success