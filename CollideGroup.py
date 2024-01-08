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
            # Else, check for merge type
            if type(collision_obj).__name__ == 'Ball':
                collision_obj.r += s.r/2
                collision_obj.m += s.m
                s.kill()
            elif collision_obj.r < s.r:
                s.r += collision_obj.r/2
                s.m += collision_obj.m
                # Change speed value
                '''
                vel_x = collision_obj.velocity[0] + s.velocity[0]
                vel_y = collision_obj.velocity[1] + s.velocity[1]
                s.velocity = [vel_x,vel_y]
                '''
                collision_obj.kill()
            else:
                collision_obj.r += s.r/2
                collision_obj.m += s.m
                # Change speed value
                '''
                vel_x = collision_obj.velocity[0] + s.velocity[0]
                vel_y = collision_obj.velocity[1] + s.velocity[1]
                collision_obj.velocity = [vel_x,vel_y]
                '''
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



        

        
