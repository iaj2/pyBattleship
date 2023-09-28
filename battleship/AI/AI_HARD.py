import pygame as p
import numpy as np
from battleship.AI.AI import AI
from battleship.constants import ROWS,COLS, SHIP_SIZES, Tile, ShotMapCode
from battleship.ship import Ship
import random
import time


class AI_HARD(AI):
    def __init__(self,board,opponent_board):
        super().__init__(board, opponent_board)
        self.prob_map = None
        self.adj_hit_probs_map = {}
        self.ship_tiles_hit = 0

    def set_opponent_ships_list(self):
        """
        Stores a list of the oppenents ships. AI will not use this information to target the ships but rather
        to know if they have been sunk
        """
        self.opponent_ships = self.opponent_board.get_ships_list()

    def _get_endpoints(self, ship, row , col):
        """
        get a list of endpoints a ship could have on a sepecific position on the board.
        """
        endpoints = []
        if (row + 1) - ship.size > 0:
            endpoints.append(((row-ship.size+1, col), (row, col)))
        if row + ship.size <= ROWS:
            endpoints.append(((row, col), (row+ship.size-1, col)))
        if (col + 1) - ship.size > 0:
            endpoints.append(((row, col-ship.size+1), (row, col)))
        if col + ship.size <= COLS:
            endpoints.append(((row, col), (row, col+ship.size-1)))

        return endpoints
    
    def _remove_hit_probabilites(self, prob_map):
        """
        removes any added probability on a probability map from positions where a hit has been made
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.opponent_shot_map[row,col] == ShotMapCode.HIT.value:
                    prob_map[row,col] = 0

    def _add_adj_hits_to_map(self,ship, row, col):
        """
        after a ship was hit, add indexes of adjascent squares to the adjescent hit probabilites map.
        """
        if ship not in self.adj_hit_probs_map:
            self.adj_hit_probs_map[ship] = []

        if row + 1 < ROWS and self.opponent_shot_map[row+1,col] == ShotMapCode.EMPTY_SPACE.value:
            self.adj_hit_probs_map[ship].append((row+1,col))
        if row - 1 >= 0 and self.opponent_shot_map[row-1,col] == ShotMapCode.EMPTY_SPACE.value:
            self.adj_hit_probs_map[ship].append((row-1,col))
        if col + 1 < COLS and self.opponent_shot_map[row,col+1] == ShotMapCode.EMPTY_SPACE.value:
            self.adj_hit_probs_map[ship].append((row, col+1))
        if col - 1 >= 0 and self.opponent_shot_map[row,col-1] == ShotMapCode.EMPTY_SPACE.value:
            self.adj_hit_probs_map[ship].append((row, col-1))

    def _add_orientaion_probability(self, prob_map):
        """
        adds extra probability to adjascent squares of horizontally/vertically scored hits
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.opponent_shot_map[row,col] != ShotMapCode.HIT.value:
                    continue
                ship = self.opponent_board_fixed[row][col]
                if isinstance(ship, Ship) and not ship.is_sunk():
                    if row -1 >= 0 and row + 1 < ROWS:
                        if self.opponent_shot_map[row+1,col] == ShotMapCode.HIT.value and\
                            self.opponent_shot_map[row-1,col] == ShotMapCode.EMPTY_SPACE.value:
                                prob_map[row-1, col] += 50
                        if self.opponent_shot_map[row-1,col] == ShotMapCode.HIT.value and \
                            self.opponent_shot_map[row+1,col] == ShotMapCode.EMPTY_SPACE.value:
                                prob_map[row+1, col] += 50
                    if col -1 >= 0 and col + 1 < COLS:
                        if self.opponent_shot_map[row,col+1] == ShotMapCode.HIT.value and\
                            self.opponent_shot_map[row,col-1] == ShotMapCode.EMPTY_SPACE.value:
                                prob_map[row, col-1] += 50
                        if self.opponent_shot_map[row,col-1] == ShotMapCode.HIT.value and \
                            self.opponent_shot_map[row,col+1] == ShotMapCode.EMPTY_SPACE.value:
                                prob_map[row, col+1] += 50
                    


    def add_adj_hit_probs(self,prob_map):
        """
        adds extra weight to the probability map if to adjascent squares of hit spots
        """
        if not self.adj_hit_probs_map:
            return

        for _, adj_pos_list in self.adj_hit_probs_map.items():
            for position in adj_pos_list:
                row,col = position
                if self.opponent_shot_map[row, col] == ShotMapCode.EMPTY_SPACE.value:
                    prob_map[row,col] += 50


    def generate_prob_map(self):
        prob_map = np.zeros((6, 10))

        for ship in self.opponent_ships:
            if not ship.is_sunk():
                for row in range(ROWS):
                    for col in range(COLS):
                        
                      if self.opponent_shot_map[row,col] != ShotMapCode.MISS.value:
                            endpoints = self._get_endpoints(ship, row, col)

                            # add one to end point cuz of numpy slicing
                            for (start_row, start_col), (end_row, end_col) in endpoints:
                                if np.all(self.opponent_shot_map[start_row:end_row+1, start_col:end_col+1] != ShotMapCode.MISS.value):
                                    prob_map[start_row:end_row+1, start_col:end_col+1] += 1 


        self._remove_hit_probabilites(prob_map)
        self.add_adj_hit_probs(prob_map)
        self._add_orientaion_probability(prob_map)

        self.prob_map = prob_map
        

    def shoot_ship(self):
        """shoots opponent ship"""
        # Find the indices of the maximum value
        max_indices = np.argmax(self.prob_map)
        max_row, max_col = np.unravel_index(max_indices, self.prob_map.shape)

        # Shoot the ship
        _, ship_got_hit, ship =  self.opponent_board.hit_ship(max_row,max_col)
        
        if ship_got_hit:
            self.opponent_shot_map[max_row, max_col] = ShotMapCode.HIT.value
            self.ship_tiles_hit += 1
            if ship.is_sunk():
                del self.adj_hit_probs_map[ship]
            else:
                self._add_adj_hits_to_map(ship, max_row, max_col)

        else:
            self.opponent_shot_map[max_row, max_col] = ShotMapCode.MISS.value

    def turn(self):
        """what the ai does on each turn"""
        self.generate_prob_map()
        self.shoot_ship()

        return True