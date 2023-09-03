"""
To test the CPU's AI algorithm. Automated games will run where the AI plays against a randomly generated 
player board. No turns will be taken, only the AI will shoot and try to sink the ships on the player board as efficient as possible.
A window will display showing where the AI is shooting. It will look like the AI is playing as the player playing against a
CPU. In other words, the AI's board is on the bottom and the player's board is on top.
"""

from battleship.board import Board
from battleship.CPU import CPU
import pygame as p
from battleship.constants import WIDTH,HEIGHT,BLUE_DARKER, GameState, BoardType, ROWS, COLS
from battleship.game import Game

WIN = p.display.set_mode((WIDTH,HEIGHT))    #Window
WIN.fill(BLUE_DARKER)
p.display.set_caption("AI_TEST")
FPS = 60

def main():
    run = True
    clock = p.time.Clock()
    game = Game(WIN)
    # Switch board and player such that the AI's board is on bottom and player board is on top
    # and such that you can the the player board's ships.
    game.game_state = GameState.MAIN_GAME   # Set to main game
    game.CPU_board = Board(BoardType.Player)
    game.player_board = Board(BoardType.CPU)
    game.CPU = CPU(game.CPU_board, game.player_board)
    game.player = CPU(game.player_board,game.CPU_board)
    for ship in game.player_board.ships:
        ship.display = True

    row = 0
    col = 0
    while run:
        clock.tick(FPS)  # FPS control
        game.update_display() # Update Screen

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False        
      

    p.quit()


if __name__ == "__main__":
    main()
