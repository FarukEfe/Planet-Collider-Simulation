# Import Modules
import pygame as p
import sys
from datetime import date, datetime
import time
# Random Generation
from RandomGenerator import rigid_random
# Game Objects
from Slider import Slider
from RigidBody import RigidBody, Ball
from CursorCollideRect import CursorCollideRect

# For Debugging System
import threading
import subprocess

WIDTH = 1000
HEIGHT = 600

class Engine:

    window = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    time_speed = 214 # FPS

    # Track last object creation
    last_creation: date = None

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

        # Cursor Rect
        self.cursor_rect = CursorCollideRect()


    def update_click(self):
        mouse_pressed = p.mouse.get_pressed()[0]

        if not mouse_pressed:
            return
        
        cursor = p.mouse.get_pos()

        # Move slider if clicked on and return
        if self.speed_slider.container.collidepoint(cursor):
            self.speed_val = self.speed_slider.set_button_pos(cursor)
            self.time_speed = 214 * self.speed_slider.get_value()
            print("Slider modified")
            return
        
        # Kill object if clicked on then return
        clicked_obj = p.sprite.spritecollideany(self.cursor_rect,self.sprites)
        if clicked_obj != None:
            clicked_obj.kill()
            print("Object killed")
            return
            
        # Implement cooldown
        d1 = datetime.now()#datetime.strftime(datetime.now(),"%H:%M:%S")
        if self.last_creation != None:
            d1 = self.last_creation#datetime.strftime(self.last_creation,"%H:%M:%S")
        
        d2 = datetime.now()#datetime.strftime(datetime.now(),"%H:%M:%S")

        if abs((d2-d1).seconds) < 1:
            print("Cooldown not yet over")
            return
        
        # Make new object
        id_list = self.sprites.id_list()
        new_id = max(id_list) + 1
        new = RigidBody(
            [0,0],
            [0,0],
            new_id,
            15,
            15*10**14,
            (250,135,135),
            cursor[0],
            cursor[1]
            )
        self.sprites.add(new)   
        self.last_creation = datetime.now()         
    
    def update_text(self):
        self.text = self.font.render(f'Speed x {round(self.time_speed / 21.4)/10}', True, (230,230,230), (35,35,35))

    def update_sprites(self):
        # Update Sprites Group
        self.sprites.collision_detect()

        self.sprites.update_velocities(WIDTH,HEIGHT)
        self.sprites.update_accelerations()
        self.sprites.update_positions()
    
    def update_cursor_rect(self):
        cursor_pos = p.mouse.get_pos()
        self.cursor_rect.update_location(cursor_pos)
    
    def render_frame(self):
        self.window.fill((35,35,35))

        # Draw Cursor Box
        self.cursor_rect.draw(self.window)

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

        # Animation Update
        self.update_sprites()
        self.update_text()
        # Cursor Update
        self.update_cursor_rect()
        self.update_click()

        self.clock.tick(self.time_speed)
    
    # Lifecycle
    def start(self):
        while True:
            self.run()

def debug():
    while True:
        time.sleep(1)
        subprocess.run("clear")


if __name__ == "__main__":
    PyGame = Engine(gen_n=15,central_mass=False)
    PyGame.start()

    # Clear terminal to see final log
    t = threading.Thread(target=debug)
    t.start()