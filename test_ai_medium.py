"""
To test the CPU's AI algorithm. Automated games will run where the AI plays against a randomly generated 
player board. No turns will be taken, only the AI will shoot and try to sink the ships on the player board as efficient as possible.
A window will display showing where the AI is shooting. It will look like the AI is playing as the player playing against a
CPU. In other words, the AI's board is on the bottom and the player's board is on top.
"""

from battleship.board import Board
from battleship.AI.AI_MEDIUM import AI_MEDIUM
import pygame as p
from battleship.constants import WIDTH,HEIGHT,BLUE_DARKER, GameState, BoardType, ROWS, COLS
from battleship.game import Game
import numpy as np
import time
from copy import deepcopy

WIN = p.display.set_mode((WIDTH,HEIGHT))    #Window
WIN.fill(BLUE_DARKER)
p.display.set_caption("AI_TEST")
FPS = 60

def init_test(game):
        game.game_state = GameState.MAIN_GAME   # Set to main game
        game.CPU_board = Board(BoardType.Player)
        game.player_board = Board(BoardType.CPU)
        game.CPU = AI_MEDIUM(game.CPU_board, game.player_board)
        game.player = AI_MEDIUM(game.player_board,game.CPU_board)
        for ship in game.player_board.ships:
            ship.display = True
        game.CPU.set_fixed_opponent_board()

def main():
    run = True
    clock = p.time.Clock()
    game = Game(WIN)
    # Switch board and player such that the AI's board is on bottom and player board is on top
    # and such that you can the the player board's ships.
    
    init_test(game)

    # game.CPU.get_opponent_shot_map()

    i = 0
    total_shots_taken = 0
    shots_taken = 0
    while run:
        clock.tick(FPS)  # FPS control
        game.update_display() # Update Screen

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False      

        if i < 100:
            if game.CPU.ship_tiles_hit < 17:
                game.CPU.turn()
                shots_taken+=1
                #time.sleep(0.5)
            else:
                init_test(game)
                total_shots_taken += shots_taken
                shots_taken = 0
                i += 1
        else:
            run = False
        
    p.quit()
    print(f'Average Shots to finish board: {total_shots_taken/100}')


if __name__ == "__main__":
    main()
