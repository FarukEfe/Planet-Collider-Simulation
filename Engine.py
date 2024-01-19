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

speed_slider = Slider((WIDTH - 125,50),(100,8), 0.2, 0, 100)

# LIFECYCLE
while True:

    window.fill((35,35,35))

    # Display & Update Slider
    speed_slider.render(window)

    # Display sprite groups
    sprites.draw(window)

    p.display.flip()

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit(0)
    
    # Update Sprites Group
    sprites.collision_detect()

    sprites.update_velocities(WIDTH,HEIGHT)
    sprites.update_accelerations()
    sprites.update_positions()

    cursor = p.mouse.get_pos()
    mouse_pressed = p.mouse.get_pressed()[0]

    if speed_slider.container.collidepoint(cursor) and mouse_pressed:
        speed_val = speed_slider.change_value(cursor)
        time_speed = 214 * speed_val

    clock.tick(time_speed)