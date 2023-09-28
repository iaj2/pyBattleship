import pygame as p
from battleship.board import Board
from battleship.constants import (
    BLUE_DARKER, SETUP_GAME_START_IMG,
    WIDTH,HEIGHT, RESTART_IMG, YOU_WIN_IMG, YOU_LOSE_IMG, EASY_BUTTON_IMG,
    MED_BUTTON_IMG, HARD_BUTTON_IMG, BoardType, GameTurn, GameState, AILevel
)
from battleship.player import Player
from battleship.AI.AI_EASY import AI_EASY
from battleship.AI.AI_MEDIUM import AI_MEDIUM
from battleship.AI.AI_HARD import AI_HARD
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
        self.CPU = None
        self.CPU_level = None
        self.player = Player(self.player_board,self.CPU_board)
        self.game_state = GameState.MAIN_MENU
        self.game_just_started = False
        self.turn = GameTurn.Player
        self.winner = None

    # Initialize UI (buttons and such)
    def _init_UI(self):
        # Create easy, medium and hard level buttons
        main_menu_button_y = 330
        easy_level_button_x = (WIDTH//4 - EASY_BUTTON_IMG.get_width()//2)
        easy_level_button_y = (main_menu_button_y - EASY_BUTTON_IMG.get_height()//2)
        self.easy_level_button = Button(EASY_BUTTON_IMG, easy_level_button_x, easy_level_button_y)

        med_level_button_x = ((WIDTH//4)*2 - MED_BUTTON_IMG.get_width()//2)
        med_level_button_y = (main_menu_button_y - MED_BUTTON_IMG.get_height()//2)
        self.med_level_button = Button(MED_BUTTON_IMG, med_level_button_x, med_level_button_y)

        hard_level_button_x = ((WIDTH//4)*3 - HARD_BUTTON_IMG.get_width()//2)
        hard_level_button_y = (main_menu_button_y - HARD_BUTTON_IMG.get_height()//2)
        self.hard_level_button = Button(HARD_BUTTON_IMG, hard_level_button_x, hard_level_button_y)

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
            self._main_menu()
        elif self.game_state == GameState.SETUP:
            self._setup_game()
        elif self.game_state == GameState.MAIN_GAME:
            self._main_game()
        elif self.game_state == GameState.END:
            self._end_game()

    def update_display(self):
        self.win.fill(BLUE_DARKER)
        if self.game_state == GameState.MAIN_MENU:
            self.easy_level_button.draw(self.win)
            self.med_level_button.draw(self.win)
            self.hard_level_button.draw(self.win)
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

    def _main_menu(self):
        # Detect start button to start game
        if self.easy_level_button.is_clicked():
            self.CPU = AI_EASY(self.CPU_board, self.player_board)
            self.game_state = GameState.SETUP
            self.CPU_level = AILevel.EASY
        elif self.med_level_button.is_clicked():
            self.CPU = AI_MEDIUM(self.CPU_board, self.player_board)
            self.game_state = GameState.SETUP
            self.CPU_level = AILevel.MEDIUM
        elif self.hard_level_button.is_clicked():
            self.CPU = AI_HARD(self.CPU_board, self.player_board)
            self.game_state = GameState.SETUP
            self.CPU_level = AILevel.HARD
    
     
    def _setup_game(self):
        # Setup Player Board
        self.player.setup_board()
        # Detect start button to start game
        if self.setup_game_start_button.is_clicked():
            self.game_state = GameState.MAIN_GAME
            if self.CPU_level == AILevel.HARD:
                self.CPU.set_opponent_ships_list()
                self.CPU.set_fixed_opponent_board()                


    def _main_game(self):
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
            self.game_state = GameState.MAIN_MENU
