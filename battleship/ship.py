import pygame as p
from battleship.constants import (
CELL_SIZE,SHIP_EK,SHIP_FN,SIDE_PADDING,MIDDLE_PADDING,TOP_PADDING,
BOARDHEIGHT, ROWS,COLS, BoardType
)

class Ship():
    def __init__(self, size, col, row, board_type):
        self.size = size
        self.col, self.row = col,row
        self.x, self.y = 0,0
        self.indexes = [(0,0) for _ in range(size)]
        self.board_type = board_type
        self.orientation = "v"    
        self.hits = 0
        self.sunk = False
        if board_type == BoardType.CPU:
            self.display = False
        else:
            self.display = True
        self.ship_img = self._get_ship_type()
        self.calc_pos()
        self.calc_indexes()

    def calc_pos(self):
        self.x = SIDE_PADDING + self.col*CELL_SIZE
        if self.board_type == BoardType.CPU:
            self.y = TOP_PADDING + self.row*CELL_SIZE
        else:
            self.y = TOP_PADDING+BOARDHEIGHT+MIDDLE_PADDING + self.row*CELL_SIZE

    def _get_ship_type(self):
        if self.board_type == BoardType.CPU:
            ship = p.transform.scale(SHIP_FN, (CELL_SIZE,CELL_SIZE*self.size))
        else:
            ship = p.transform.scale(SHIP_EK, (CELL_SIZE,CELL_SIZE*self.size))
        return ship
    
    def is_sunk(self):
        return self.sunk
    
    def calc_indexes(self):
        if self.orientation == "v":
            for i in range(self.size):
                self.indexes[i] = (self.row + i,self.col)
        else:
            for i in range(self.size):
                self.indexes[i] = (self.row, self.col + i)

    def draw(self,win):
        if self.orientation == "v":
            win.blit(self.ship_img, (self.x,self.y))
        else:
            win.blit(p.transform.rotate(self.ship_img,90), (self.x, self.y))

    def _in_bounds(self,row,col):
        if self.orientation == "v":
            #Check in bounds
            if col >= 0 and col < COLS:                          
                if row >= 0 and row + self.size <= ROWS :   
                    return True
        if self.orientation == "h":
            # Check in bounds
            if col >= 0 and col + self.size <= COLS: 
                if row >= 0 and row < ROWS:     
                    return True
        return False

    def move(self,row,col):
        if self._in_bounds(row,col):
            # Move left/right
            if col > self.col or col < self.col:        
                self.col = col
            # Move up/down
            if row < self.row or row > self.row:     
                self.row = row
            # Recalculate position
            self.calc_pos()
       
    def hit(self):
        self.hits += 1
        if self.hits == self.size:
            self.display = True
            self.sunk = True
