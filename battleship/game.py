import pygame as p
from battleship.board import Board
from battleship.constants import (
    BLUE_DARKER, SETUP_GAME_START_IMG,
    WIDTH,HEIGHT, RESTART_IMG, YOU_WIN_IMG, YOU_LOSE_IMG,
    BoardType, GameTurn, GameState
)
from battleship.player import Player
from battleship.CPU import CPU
from battleship.button import Button

class Game():
    def __init__(self, win):
        self.win = win
        self._init()
        self._init_UI()

    # Initialize new game
    def _init(self):
        self.CPU_board = Board(BoardType.CPU)
        self.player_board = Board(BoardType.Player)
        self.CPU = CPU(self.CPU_board,self.player_board)
        self.player = Player(self.player_board,self.CPU_board)
        self.game_state = GameState.SETUP
        self.game_just_started = False
        self.turn = GameTurn.Player
        self.winner = None

    # Initialize UI (buttons and such)
    def _init_UI(self):
        # Create the in-game start button in between the middle of the screen
        setup_game_start_button_x = (WIDTH - SETUP_GAME_START_IMG.get_width())//2
        setup_game_start_button_y = (HEIGHT - SETUP_GAME_START_IMG.get_height())//2
        self.setup_game_start_button = Button(SETUP_GAME_START_IMG,setup_game_start_button_x,setup_game_start_button_y)

        # Create end game restart button
        restart_button_x = (WIDTH - RESTART_IMG.get_width())//2
        restart_button_y = (HEIGHT - RESTART_IMG.get_height())//2 - 40
        self.restart_button = Button(RESTART_IMG,restart_button_x,restart_button_y)


    def state_manager(self):
        if self.game_state == GameState.MAIN_MENU:
            # TODO: Implement Main Menu
            pass
        elif self.game_state == GameState.SETUP:
            self._setup_game()
        elif self.game_state == GameState.MAIN_GAME:
            self._main_game()
        elif self.game_state == GameState.END:
            self._end_game()

    def update_display(self):
        self.win.fill(BLUE_DARKER)
        if self.game_state == GameState.SETUP or self.game_state == GameState.MAIN_GAME:
            # Draw boards
            self.CPU_board.draw(self.win)
            self.player_board.draw(self.win)
        if self.game_state == GameState.SETUP:   
            # Draw in-game start button
            self.setup_game_start_button.draw(self.win)
        if self.game_state == GameState.END:
            # Display restart button
            self.restart_button.draw(self.win)
            # Display winner
            winner_banner_x = 0
            winner_banner_y = 20
            if self.winner == GameTurn.Player:
                self.win.blit(YOU_WIN_IMG, (winner_banner_x,winner_banner_y))
            else:
                self.win.blit(YOU_LOSE_IMG, (winner_banner_x,winner_banner_y))

        p.display.update()
        
    def _setup_game(self):
        # Setup Player Board
        self.player.setup_board()
        # Detect start button to start game
        if self.setup_game_start_button.is_clicked():
            self.game_state = GameState.MAIN_GAME


    def _main_game(self):
        if not self.game_just_started:
            self.CPU.set_opponent_ships_list()
            self.CPU.set_fixed_opponent_board()
            self.game_just_started = True

        if self.turn == GameTurn.Player:
            if self.player.turn():
                self._change_turn()
            # Check for win
            if self._check_win(self.CPU):
               self.winner = GameTurn.Player
               self.game_state = GameState.END
        else:
            if self.CPU.turn():
                self._change_turn()
            # Check for win
            if self._check_win(self.player):
               self.winner = GameTurn.CPU
               self.game_state = GameState.END

    def _change_turn(self):
        if self.turn == GameTurn.Player:
            self.turn = GameTurn.CPU
        else:
            self.turn = GameTurn.Player

    def _check_win(self,opponent):
        # Check for win
        for ship in opponent.board.ships:
            if not ship.sunk:
                return False
        return True
    
    def _end_game(self):
        # Detect if restart button is clicked to restart game
        if self.restart_button.is_clicked():
            # Init a new game
            self._init()
            # Change game state to setup
            self.game_state = GameState.SETUP
