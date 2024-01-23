import pygame as p
from pygame.draw import rect

class CursorCollideRect(p.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 20
        self.rect = None
    
    def draw(self, window):
        self.rect = rect(window,(35,35,35),p.Rect(self.x,self.y,5,5))
    
    def update_location(self, cursor_pos):
        self.x = cursor_pos[0]
        self.y = cursor_pos[1]