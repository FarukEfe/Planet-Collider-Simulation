import pygame as p
from RandomGenerator import rigid_random
from Slider import Slider
import sys

WIDTH = 1000
HEIGHT = 600

# PyGame Setup
p.init()

window = p.display.set_mode((WIDTH,HEIGHT))
p.display.set_caption("Planet Collider")
clock = p.time.Clock()

time_speed = 214 # Define FPS

# GAME SPRITES SETUP
sprites = rigid_random(20,WIDTH,HEIGHT,False)

speed_slider = Slider((WIDTH - 125,50),(100,8), 20, 0, 100)

cursor = p.mouse.get_pos()
if speed_slider.container.collidepoint(cursor):
    speed_slider.change_value(cursor)

# LIFECYCLE
while True:

    window.fill((35,35,35))

    # Display Slider
    speed_slider.render(window)

    # Display sprite groups
    sprites.draw(window)

    p.display.flip()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit(0)
    

    sprites.collision_detect()

    sprites.update_velocities(WIDTH,HEIGHT)
    sprites.update_accelerations()
    sprites.update_positions()

    clock.tick(time_speed)