import pygame as p
from battleship.constants import WIDTH,HEIGHT,BLUE_DARKER
from battleship.game import Game

WIN = p.display.set_mode((WIDTH,HEIGHT))    #Window
WIN.fill(BLUE_DARKER)
p.display.set_caption("Battleship")
FPS = 60

def main():
    run = True
    clock = p.time.Clock()
    game = Game(WIN)
    while run:
        clock.tick(FPS)  # FPS control
        game.update_display() # Update Screen

        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
      
        game.state_manager()
        

    p.quit()


if __name__ == "__main__":
    main()
