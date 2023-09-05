import pygame as p
from battleship.constants import (
SIDE_PADDING,TOP_PADDING,MIDDLE_PADDING,BOARDHEIGHT,ROWS,COLS,SHIP_SIZES,
BLUE_LIGHT,CELL_IMAGE,CELL_SIZE,GREEN,RED, BoardType, Tile)
from battleship.ship import Ship

class Board():
    def __init__(self, board_type):
        self.board = []
        self.ships = []
        self.board_type = board_type
        self.x, self.y = self.get_position()
        self._create()

    def get_position(self):
        x = SIDE_PADDING
        if self.board_type == BoardType.CPU:
            y = TOP_PADDING
        elif self.board_type == BoardType.Player:
            y = TOP_PADDING+BOARDHEIGHT+MIDDLE_PADDING
        return x,y
    

    def _create(self):
        # Create board
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(Tile.OPEN)

        # Add ships to board
        row = 0
        col = 0
        for size in SHIP_SIZES:
            self.ships.append(Ship(size,col,row,self.board_type))     
            col += 1

        for ship in self.ships:
            for row,col in ship.indexes:
                self.board[row][col] = ship


    def draw(self,win):
        # Draw cells
        cell_img = CELL_IMAGE
        for row in range(ROWS):
            for col in range(COLS):
                win.blit(cell_img, (self.x+CELL_SIZE*col, self.y+CELL_SIZE*row))
                p.draw.rect(win,BLUE_LIGHT,(self.x+CELL_SIZE*col, self.y+CELL_SIZE*row, CELL_SIZE, CELL_SIZE), 1)

        # Draw ships
        for ship in self.ships:
            if ship.display:
                ship.draw(win)

        # Draw hit/miss
        miss = p.Surface((CELL_SIZE,CELL_SIZE))
        miss.set_alpha(128)
        miss.fill(GREEN)
        hit = p.Surface((CELL_SIZE,CELL_SIZE))
        hit.set_alpha(128)
        hit.fill(RED)

        for row in range(ROWS):
            for col in range(COLS):
                # Draw miss
                if self.board[row][col] == Tile.MISS:     
                    win.blit(miss,(self.x+CELL_SIZE*col,self.y+CELL_SIZE*row))
                    
                # Draw hit
                elif self.board[row][col] == Tile.HIT:
                    win.blit(hit,(self.x+CELL_SIZE*col,self.y+CELL_SIZE*row))



    def print(self):
        print("**************************")
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != Tile.OPEN:
                    print("X ",end="")
                else:
                    print("0 ",end="")
            print("\n")
        print("**************************")


    def rotate_ship(self,ship):
        success = True
        # Rotate vertical to horizontal
        if ship.orientation == "v":
            if ship.col + ship.size <= COLS:
                for i in range(1,ship.size):
                    if self.board[ship.row][ship.col+i] != Tile.OPEN:
                        success = False
                if success:
                    for i in range(ship.size):
                        self.board[ship.row][ship.col+i] = ship
                    for i in range(1,ship.size):
                        self.board[ship.row+i][ship.col] = Tile.OPEN
                    ship.orientation = "h"
                    ship.calc_indexes()
        # Rotate horizontal to vertical
        else:
            if ship.row + ship.size <= ROWS:
                for i in range(1,ship.size):
                    if self.board[ship.row+i][ship.col] != Tile.OPEN:
                        success = False
                if success:
                    for i in range(ship.size):
                        self.board[ship.row+i][ship.col] = ship
                    for i in range(1,ship.size):
                        self.board[ship.row][ship.col+i] = Tile.OPEN
                    ship.orientation = "v"
                    ship.calc_indexes()

        return success

    def move_ship(self,ship,row,col):
        if ship.orientation == "v":
            #Check in bounds
            if col >= 0 and col < COLS:                          
                if row >= 0 and row + ship.size <= ROWS:   
                    ship.move(row,col)

        if ship.orientation == "h":
            # Check in bounds
            if col >= 0 and col + ship.size <= COLS: 
                if row >= 0 and row < ROWS:     
                    ship.move(row,col)

    def place_ship(self,ship):
        prev_indexes = ship.indexes[:]
        success = True
        ship.calc_indexes()
        # Check valid placement
        for row,col in ship.indexes:
            if self.board[row][col] != ship and self.board[row][col] != Tile.OPEN:
                success = False
                break
        # Reset location if invalid placement
        if not success:
            ship.row = prev_indexes[0][0]
            ship.col = prev_indexes[0][1]
            ship.calc_indexes()
            ship.calc_pos()
        # Erase old location
        for row,col in prev_indexes:
            self.board[row][col] = Tile.OPEN
        # Fill new location
        for row,col in ship.indexes:
            self.board[row][col] = ship

        return success
               
    def hit_ship(self,row,col):
        tile = self.board[row][col]
        success = False
        hit_ship = False
        # Miss
        if self.board[row][col] == Tile.OPEN:
            self.board[row][col] = Tile.MISS
            success = True
        # Hit
        elif self.board[row][col] != Tile.MISS and self.board[row][col] != Tile.HIT:
            ship = self.board[row][col]
            ship.hit()
            self.board[row][col] = Tile.HIT
            success = True
            hit_ship = True
        # Return if the shot was valid (hit a spot not already hit)    
        return success,hit_ship,tile

    def get_ships_list(self):
        return self.ships
            

 
        
        
    

   

    

            
