import pygame as p

class Button():
    def __init__(self,img,x,y):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self,win):
        # Draw button on screen
        win.blit(self.img, (self.rect.x,self.rect.y))
    
    def is_clicked(self):
        # Return variable
        action = False

        # Get mouse position
        pos = p.mouse.get_pos()

        # Check mouse over and clicked conditions   
        if self.rect.collidepoint(pos):
            #p.mouse.set_cursor(p.SYSTEM_CURSOR_HAND)
            if p.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
                p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)
        else:
            p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)

        if not p.mouse.get_pressed()[0]:
            self.clicked = False

        return action
        