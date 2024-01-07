import pygame as p
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

            if type(collision_obj).__name__ == 'Ball' or collision_obj.r > s.r:
                collision_obj.r += s.r/2
                collision_obj.m += s.m
                s.kill()
            else:
                s.r += collision_obj.r/2
                s.m += collision_obj.m
                collision_obj.kill()

        
