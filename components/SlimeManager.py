import random
from .Slime import Slime
from collections import namedtuple
Vector2D = namedtuple("Vector2D", ["x", "y"])

class SlimeManager:
    def __init__(self):
        self.slimes = []

    def spawn(self, p, beat_offset, m_grav, m_spd):
        vPos = Vector2D(p[0], p[1])
        vVel = Vector2D(random.randint(-5,5),0)
        radius = random.randint(30, 40)
        self.slimes.append(Slime(radius, vPos, vVel, beat_offset, m_grav, m_spd))

    def draw(self, screen, t):
        for s in self.slimes:
            s.draw(screen, t)

    # def check_collision(self, mouse):
    #     for s in self.slimes[:]:
    #         if s.check_collision(mouse):
    #             self.slimes.remove(s)