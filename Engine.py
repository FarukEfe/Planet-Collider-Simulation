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

# SLIDER SETUP
speed_slider = Slider((WIDTH - 125,75),(100,8), 0.2, 0, 100)

# SLIDER TEXT SETUP
font = p.font.Font('freesansbold.ttf', 12)
text = font.render(f'Speed x {time_speed / 214}', True, (230,230,230), (35,35,35))
textRect = text.get_rect()
textRect.right = WIDTH - 115
textRect.centery = 55

# LIFECYCLE
while True:

    window.fill((35,35,35))

    # Display Text & Slider
    window.blit(text, textRect)
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

    # Update Slider

    cursor = p.mouse.get_pos()
    mouse_pressed = p.mouse.get_pressed()[0]

    if speed_slider.container.collidepoint(cursor) and mouse_pressed:
        speed_val = speed_slider.set_button_pos(cursor)
        time_speed = 214 * speed_slider.get_value()
    
    # Update Text
    text = font.render(f'Speed x {round(time_speed / 21.4)/10}', True, (230,230,230), (35,35,35))

    clock.tick(time_speed)