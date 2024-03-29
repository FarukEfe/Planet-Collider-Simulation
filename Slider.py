import pygame as p

class Slider:

    # pos - position of the center of the object
    def __init__(self, pos:tuple, size: tuple, initial_value: int, min:int, max:int):
        self.pos = pos
        self.size = size
        
        # Range
        self.slider_left_pos = self.pos[0] - size[0]//2
        self.slider_right_pos = self.pos[0] + size[0]//2
        self.slider_top_pos = self.pos[1] - size[1]//2
        self.slider_bottom_pos = self.pos[1] + size[1]//2

        # Min - Max
        self.min = min
        self.max = max

        # Initial value pos
        self.initial_val = (self.slider_right_pos - self.slider_left_pos)*initial_value # <- range by multiplier

        # Sprite
        self.container = p.Rect(self.slider_left_pos,self.slider_top_pos,self.size[0],self.size[1])
        self.button_rect = p.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos,8,self.size[1])

    def set_button_pos(self, mouse_pos) -> float:
        self.button_rect.centerx = mouse_pos[0]
    
    def render(self,window):
        p.draw.rect(window, "darkgray", self.container)
        p.draw.rect(window, "blue", self.button_rect)
    
    def get_value(self) -> float:
        length = self.slider_right_pos = self.slider_left_pos
        button_range = self.button_rect.centerx - self.slider_left_pos
        # Get button value expressed as range from min to max, with min as offset
        return (button_range/length)*(self.max - self.min)+self.min
