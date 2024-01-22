import pygame as p
from RandomGenerator import rigid_random
from Slider import Slider
import sys

WIDTH = 1000
HEIGHT = 600

class Engine:

    window = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    time_speed = 214 # FPS

    def __init__(self, gen_n:int, central_mass:bool):
        p.init()
        p.display.set_caption("Planet Collider")

        # Sprite Setup
        self.sprites = rigid_random(gen_n,WIDTH,HEIGHT,central_mass)

        # Slider Setup
        self.speed_slider = Slider((WIDTH - 125,75),(100,8),0.2,0,100)

        # Slider Text
        self.font = p.font.Font('freesansbold.ttf', 12)
        self.text = self.font.render(f'Speed x {self.time_speed / 214}', True, (230,230,230), (35,35,35))
        self.textRect = self.text.get_rect()
        self.textRect.right = WIDTH - 115
        self.textRect.centery = 55

    def update_text(self):
        cursor = p.mouse.get_pos()
        mouse_pressed = p.mouse.get_pressed()[0]

        if self.speed_slider.container.collidepoint(cursor) and mouse_pressed:
            self.speed_val = self.speed_slider.set_button_pos(cursor)
            self.time_speed = 214 * self.speed_slider.get_value()
    
        # Update Text
        self.text = self.font.render(f'Speed x {round(self.time_speed / 21.4)/10}', True, (230,230,230), (35,35,35))

    def update_sprites(self):
        # Update Sprites Group
        self.sprites.collision_detect()

        self.sprites.update_velocities(WIDTH,HEIGHT)
        self.sprites.update_accelerations()
        self.sprites.update_positions()
    
    def render_frame(self):
        self.window.fill((35,35,35))

        # Display Text & Slider
        self.window.blit(self.text, self.textRect)
        self.speed_slider.render(self.window)

        # Display sprite groups
        self.sprites.draw(self.window)

        p.display.flip()
    
    # Per Frame Tasks
    def run(self):

        self.render_frame()

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit(0)

        self.update_sprites()

        self.update_text()

        self.clock.tick(self.time_speed)
    
    # Lifecycle
    def start(self):
        while True:
            self.run()

if __name__ == "__main__":
    PyGame = Engine(gen_n=15,central_mass=False)
    PyGame.start()