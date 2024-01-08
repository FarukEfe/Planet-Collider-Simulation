import pygame as p
import math as m
from RigidBody import Ball, RigidBody

class CollideGroup(p.sprite.Group):

    def __init__(self,*bodies):
        super().__init__(bodies)
        self.bodies = list(bodies)
    
    def draw(self,win):
        sprites = self.sprites()
        for sprite in sprites:
            sprite.draw(win)

    def update_positions(self):
        updates = self.sprites()
        for update in updates:
            if type(update).__name__ == 'Ball':
                continue
            update.update_position()

    def update_velocities(self,WIDTH,HEIGHT):
        updates = self.sprites()
        for update in updates:
            if type(update).__name__ == 'Ball':
                continue
            update.update_velocity(WIDTH,HEIGHT)
    
    def update_accelerations(self):
        updates = self.sprites()
        for update in updates:
            if type(update).__name__ == 'Ball':
                continue
            update.update_acceleration(updates)
            
    def id_list(self) -> [int]:
        sprites = self.sprites()
        l = []
        for s in sprites:
            l.append(s.id)
        return l
    
    def collision_detect(self):
        sprites = self.sprites()
        for s in sprites:

            collision_obj = p.sprite.spritecollideany(s,self)

            # If the collision object is itself, then ignore
            if collision_obj == None or collision_obj.id == s.id:
                continue
            # If not close enough to merge, ignore
            if not self.should_merge(collision_obj,s):
                continue

            r_new = new_radius(collision_obj,s)
            # Else, check for merge type
            if type(collision_obj).__name__ == 'Ball':
                collision_obj.r = r_new
                collision_obj.m += s.m
                s.kill()
            elif type(s).__name__ == 'Ball':
                s.r = r_new
                s.m += collision_obj.m
                collision_obj.kill()
            elif collision_obj.r < s.r:
                s.r = r_new
                s.m += collision_obj.m
                # Change speed value using perfectly inelastic collision
                s.velocity = p_inelastic_velocity(collision_obj,s)
                collision_obj.kill()
            else:
                collision_obj.r = r_new
                collision_obj.m += s.m
                # Change speed value
                collision_obj.velocity = p_inelastic_velocity(collision_obj,s)
                s.kill()
    
    def should_merge(self,obj1:Ball,obj2:Ball) -> bool:
        # Define bigger/smaller radii
        bigger_radius = obj1.r
        if obj1.r < obj2.r:
            bigger_radius = obj2.r
        # Compute distance
        distance_x = abs(obj1.x - obj2.x)
        distance_y = abs(obj1.y - obj2.y)
        distance = m.sqrt(distance_x**2 + distance_y**2)
        # Return should_merge
        if distance < bigger_radius:
            return True
        return False

# HELPERS
    
# Uses perfectly inelastic collision type to find momentum, then speed
def p_inelastic_velocity(obj1:RigidBody,obj2:RigidBody) -> [float,float]:
    total_mass = obj1.m + obj2.m
    momentum_x = obj1.velocity[0]*obj1.m + obj2.velocity[0]*obj2.m    
    momentum_y = obj1.velocity[1]*obj1.m + obj2.velocity[1]*obj2.m  
    vel_x = momentum_x/total_mass
    vel_y = momentum_y/total_mass
    return [vel_x,vel_y]

# Finds post-collision radius based on total area
def new_radius(obj1:Ball,obj2:Ball) -> float:
    total_area = m.pi*obj1.r**2 + m.pi*obj2.r**2
    return m.sqrt(total_area/m.pi)
