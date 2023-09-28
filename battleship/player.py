import pygame as p
from battleship.constants import TOTAL_SHIPS,CELL_SIZE,ROWS,COLS, Tile
import random

class Player():
    def __init__(self,board,opponent_board):
        self.board = board
        self.opponent_board = opponent_board
        self.selected_ship = None
        self.drag_ship = False
        self.rotate_ship = False
        self.clicked_mouse = False
    
    def _board_pos(self,board,x,y):
        offset_x, offset_y = board.get_position()
        row = (y-offset_y)//CELL_SIZE
        col = (x-offset_x)//CELL_SIZE
        return row,col
    
    def _mouse_in_range(self,row,col):
        if row >= 0 and row < ROWS:
            if col >= 0 and col < COLS:  
                return True
        return False

    def setup_board(self):
        x,y = p.mouse.get_pos()
        row,col = self._board_pos(self.board,x,y)
        if self._mouse_in_range(row,col):  
            # Start ship drag      
            if p.mouse.get_pressed()[0] and not self.drag_ship:  
                self.selected_ship = self.board.board[row][col]
                if self.selected_ship != Tile.OPEN:
                    self.drag_ship = True
            # Detect Rotate ship
            if p.mouse.get_pressed()[2] and not self.rotate_ship:
                self.selected_ship = self.board.board[row][col]
                self.rotate_ship = True
                if self.selected_ship != Tile.OPEN:
                    self.board.rotate_ship(self.selected_ship)
                    self.selected_ship = None
            # Reset rotation click
            if not p.mouse.get_pressed()[2]:
                self.rotate_ship = False
        # Place ship after ship drag
        if self.selected_ship != Tile.OPEN and self.selected_ship != None:
            # Move ship animation
            self.selected_ship.move(row,col)
            # Place the ship on the board
            if not p.mouse.get_pressed()[0]:
                self.board.place_ship(self.selected_ship)
                self.selected_ship = None
                self.drag_ship = False

    def turn(self):
        success = False
        x,y = p.mouse.get_pos()
        row,col = self._board_pos(self.opponent_board,x,y)
        # Hit opponents board
        if self._mouse_in_range(row,col):
            if p.mouse.get_pressed()[0] and not self.clicked_mouse:
                valid_shot,_,_ = self.opponent_board.hit_ship(row,col)
                if valid_shot:
                    self.clicked_mouse = True
            if self.clicked_mouse and not p.mouse.get_pressed()[0]:
                self.clicked_mouse = False
                success = True
        return success
            

            
