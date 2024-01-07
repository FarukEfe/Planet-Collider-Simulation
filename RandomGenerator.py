from RigidBody import Ball, RigidBody
from CollideGroup import CollideGroup
from random import randint

def rigid_random(n:int, max_x:int,max_y:int,central_mass:bool) -> CollideGroup:

    # Initiate CollideGroup
    group = CollideGroup()
    if central_mass:
        h = Ball(0,35,1.8*10**17,(250,250,130),max_x/2, max_y/2)
        group.add(h)
    # Generate n random rigidbodies
    for i in range(n):
        # Random generated radius
        gen_r = randint(8,12)

        # Random generated mass
        gen_m = 1
        if central_mass:
            gen_m = randint(5000,10000)
        else:
            gen_m = randint(10**13,9*10**14)

        # Random generated position
        gen_x = randint(gen_r,max_x-gen_r)
        gen_y = randint(gen_r,max_y-gen_r)

        generated = RigidBody(
            acceleration=[0,0],
            velocity=[0,0],
            id=i+1,
            radius=gen_r,
            mass=gen_m,
            color=(250,135,135),
            x=gen_x,
            y=gen_y
        )
        group.add(generated)
    # Return final group
    return group