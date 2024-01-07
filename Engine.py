import pygame as p
from RigidBody import RigidBody, Ball
from CollideGroup import CollideGroup
from RandomGenerator import rigid_random
import sys
from copy import copy

# GAME DISPLAY SETUP

WIDTH = 1000
HEIGHT = 600

p.init()

window = p.display.set_mode((WIDTH,HEIGHT))
p.display.set_caption("Sandbox")
clock = p.time.Clock()

time_speed = 64 # Updates 10 times per second

# GAME SPRITES SETUP


sprites = rigid_random(20,WIDTH,HEIGHT,True)


# LIFECYCLE
on =  True
while on:

    # Display objects
    window.fill((35,35,35))

    # Display sprite groups
    sprites.draw(window)

    p.display.flip()

    # Listen to events
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            sys.exit(0)
    

    # Sprites Collision
    sprites.collision_detect()

    # Update sprite velocity, acceleration, and position if not killed
    sprites.update_velocities(WIDTH,HEIGHT)
    sprites.update_accelerations()
    sprites.update_positions()


    # Set up frames per second
    clock.tick(time_speed)


# TO-DO:
# combine radii for a list of rigid/stationary balls when in collision
# Learn to use Sprite Groups to check multiple-mass collisions