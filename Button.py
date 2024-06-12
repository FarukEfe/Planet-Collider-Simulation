from pygame import *

class ButtonTefxt(sprite.Sprite):

    def __init__(self,left,top,width,height,text,call:callable):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.call = call
        self.collide_rect = None

    def draw(self, window):
        # Create a surface for the button
        button_surface = Surface((self.width,self.height))
        button_surface.fill((240,240,240))
        # Create an inner surface for better looking buttons
        inner_surface = Surface((self.width*0.9,self.height*0.9))
        inner_surface.fill((140,140,140))
        # Here put the inner design for each button
        f = font.Font(None, 24)
        text = f.render(self.text, True, (35,35,35))
        text_rect = text.get_rect(center=(inner_surface.get_width()/2,inner_surface.get_height()/2))
        inner_surface.blit(text,text_rect)
        button_surface.blit(inner_surface,(5,4))
        # Render button
        window.blit(button_surface,(self.left,self.top))
        self.collide_rect = Rect(self.left,self.top,self.width,self.height)
    
    def clicked(self,pos) -> bool:
        return self.collide_rect.collidepoint(pos)
    
    def action(self):
        self.call()