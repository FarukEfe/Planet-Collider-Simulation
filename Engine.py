# Import Modules
import pygame as p
import sys
from datetime import date, datetime, timedelta
import time
# Random Generation
from RandomGenerator import rigid_random
# Game Objects
from Slider import Slider
from RigidBody import RigidBody, Ball
from CursorCollideRect import CursorCollideRect
from CollideGroup import CollideGroup
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

    # Track Game Navigation State
    central_mass = False
    game_on = True

    def __init__(self):
        p.init()
        p.display.set_caption("Planet Collider")

        # Initialized properties
        self.sprites: CollideGroup = None
        self.speed_slider: Slider = None

        self.font = None
        self.text = None
        self.textRect = None

        self.cursor_rect = CursorCollideRect()

    ### MARK: FOR RENDERING PLAYGROUND
    
    # Returns if should ignore MOUSEBUTTONDOWN
    def update_slider(self) -> bool:
        mouse_pressed = p.mouse.get_pressed()[0]

        if not mouse_pressed:
            return False
        
        cursor = p.mouse.get_pos()

        # Move slider if clicked on and return
        if self.speed_slider.container.collidepoint(cursor):
            self.speed_val = self.speed_slider.set_button_pos(cursor)
            self.time_speed = 214 * self.speed_slider.get_value()
            return True
        return False


    def update_click(self):
        mouse_pressed = p.mouse.get_pressed()[0]

        if not mouse_pressed:
            return
        
        cursor = p.mouse.get_pos()
            
        # Implement cooldown
        d1 = datetime.today() - timedelta(seconds=5)
        if self.last_creation != None:
            d1 = self.last_creation
        
        d2 = datetime.now()

        # Change cooldown here...
        if abs((d2-d1).seconds) < 0.5:
            print("Cooldown not yet over")
            return
          
        
        # Kill object if clicked on then return
        clicked_obj = p.sprite.spritecollideany(self.cursor_rect,self.sprites)
        if clicked_obj != None:
            clicked_obj.kill()
            print("Object killed")
            return
        
        # Reset last modification to sprites
        self.last_creation = datetime.now() 
        
        # Otherwise, make new object
        id_list = self.sprites.id_list()
        new_id = 0
        if len(id_list) > 0:
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
    def run_playground(self):

        self.render_frame()

        # Animation Update
        self.update_sprites()
        self.update_text()
        # Slider and Collide Cursor Update
        self.update_cursor_rect()
        ignore_tap = self.update_slider()
        
        # Check for events
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit(0)
            elif event.type == p.MOUSEBUTTONDOWN and not ignore_tap:
                # Click Update
                self.update_click()

        # Next Frame
        self.clock.tick(self.time_speed)

    ### MARK: RENDERING MAIN MENU

    def main_menu(self):
        pass

    ### MARK: NAVIGATION

    # Generate rigidbodies
    def generate(self,gen_n:int,central_mass:bool):
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
    
    # Reset rigidbodies
    def reset_playground(self):
        self.sprites: CollideGroup = None
        self.speed_slider: Slider = None

        self.font = None
        self.text = None
        self.textRect = None

    ### MARK: MAINLOOP
    
    def mainloop(self):
        if self.game_on:
            self.run_playground()
        else:
            self.main_menu()
        
    # Lifecycle
    def start(self):
        while True:
            self.mainloop()

def debug():
    while True:
        time.sleep(1)
        subprocess.run("clear")


if __name__ == "__main__":
    engine = Engine()
    engine.generate(15,False)
    engine.start()

    # Clear terminal to see final log
    t = threading.Thread(target=debug)
    t.start()