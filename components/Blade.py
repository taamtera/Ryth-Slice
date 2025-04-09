import pygame

class Blade:
    def __init__(self, speed_threshold=10): 
        self.x = 0
        self.y = 0
        self.speed_threshold = speed_threshold
        self.trail = []

    def get_pos(self):
        self.x, self.y = pygame.mouse.get_pos()
        return self
