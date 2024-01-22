from pygame.sprite import Sprite
from pygame.draw import circle
import math as m

class Ball(Sprite):

    def __init__(self,id:int,radius:float,mass:float,color:(int,int,int),x:float,y:float,):
        super().__init__()
        self.id = id
        self.r = radius # in km
        self.m = mass # in kg
        self.rgb = color
        self.x = x
        self.y = y
        self.rect = None
    
    def draw(self, win):
        self.rect = circle(win,color=self.rgb,center=[self.x,self.y],radius=self.r)

class RigidBody(Ball):

    g_constant = 6.67428*10**-2 # Gravitational Constant
    length_multiplier = 3.7795275591*(10**6) # 1mm treated as a kilometer (in pixels)
    
    def __init__(self,acceleration:[float,float],velocity:[float,float],id:int,radius:float,mass:float,color:(int,int,int),x:float,y:float):
        super().__init__(id,radius,mass,color,x,y)
        self.acceleration = acceleration
        self.velocity = velocity

    def gravity_pull(self, body:Ball) -> (float, float):
        # If the ball is itself, return 0
        if self.id == body.id:
            return 0,0
        # Get distance between objects
        distance_x = self.x - body.x
        distance_y = self.y - body.y
        distance = m.sqrt(distance_x**2 + distance_y**2)
        # Find total gravity pull magnitude
        pull = self.g_constant * self.m * body.m / (distance*self.length_multiplier)**2
        # Find angle from horizontal and and split pull into components
        theta = m.atan2(-distance_y, -distance_x)
        pull_x = m.cos(theta) * pull
        pull_y = m.sin(theta) * pull
        # Return both components in a tuple
        return pull_x, pull_y

    def update_acceleration(self, bodies: [Ball]):
        total_pull_x = 0
        total_pull_y = 0

        # Sum up gravity pulls to find total force components
        for body in bodies:
            # Get pull between bodies
            pull_x, pull_y = self.gravity_pull(body)
            total_pull_x += pull_x
            total_pull_y += pull_y

        # Get acceleration from total force
        acc_x, acc_y = total_pull_x/self.m, total_pull_y/self.m
        self.acceleration = [acc_x,acc_y]

    def update_velocity(self, bound_x, bound_y):
        # Rebound from borders (only switch if velocity is also pointing out the boundaries to prevent from double-switch in-between iterations)
        if (self.x <= self.r and self.velocity[0] < 0) or (self.x >= bound_x - self.r and self.velocity[0] > 0):
            self.velocity[0] *= -1
        if (self.y <= self.r and self.velocity[1] < 0) or (self.y >= bound_y - self.r and self.velocity[1] > 0):
            self.velocity[1] *= -1

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
    
    def update_position(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
    
    def mouse_collision(self,cursor) -> bool:
        if self.rect.collidepoint(cursor):
            self.kill()
            return True
        return False
        