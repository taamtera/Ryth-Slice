import pygame
from collections import namedtuple
Vector2D = namedtuple("Vector2D", ["x", "y"])

class Slime:
    def __init__(self, r, vPos, vVel, beat_offset, m_grav, m_spd):
        self.vPos0 = vPos
        self.vVel0 = vVel
        self.vPos = None
        self.beat_offset = beat_offset
        self.r = r
        self.m_spd = m_spd   # Speed multiplier
        self.m_grav = m_grav   # Gravity multiplier

    def position(self, t):
        t = (t - self.beat_offset) * self.m_spd
        self.vPos = Vector2D(
            self.vPos0.x + self.vVel0.x * t,
            self.vPos0.y + self.vVel0.y * t + (self.m_grav * t ** 2) / 2
        )

    def draw(self, screen, t):
        self.position(t)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.vPos.x), int(self.vPos.y)), self.r)

    # def check_collision(self, mouse):
    #     return (self.x - mouse[0]) ** 2 + (self.y - mouse[1]) ** 2 < (self.r*1.2) ** 2
