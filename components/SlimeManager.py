from .Slime import Slime
import random
import pygame
from collections import namedtuple
Vector2D = namedtuple("Vector2D", ["x", "y"])

class SlimeManager:
    def __init__(self, screen):
        self.screen = screen
        self.slimes = []
        self.particles = []
        self.texts = []  # List to store score or miss texts
        self.score = []


    def spawn(self, p, beat_offset, m_grav, m_spd):
        vPos = Vector2D(p[0], p[1])
        vVel = Vector2D(random.randint(-5,5),0)
        self.slimes.append(Slime(50, vPos, vVel, beat_offset, m_grav, m_spd))

    def update(self, t, mouse, last_mouse_pos):
        for s in self.slimes:
            s.draw(self.screen, t)
        for p in self.particles[:]:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["radius"] -= 0.1
            if p["radius"] <= 0:
                self.particles.remove(p)
            else:
                pygame.draw.circle(self.screen, p["color"], (int(p["pos"][0]), int(p["pos"][1])), int(p["radius"]))
        for text in self.texts[:]:
            text["lifetime"] -= 1
            if text["lifetime"] <= 0:
                self.texts.remove(text)
            else:
                font = pygame.font.Font(None, 36)  # Default font with size 36
                rendered_text = font.render(text["text"], True, text["color"])
                self.screen.blit(rendered_text, (text["pos"][0], text["pos"][1]))
                text["pos"][1] -= 1  # Move text upward slightly
        self.check_collision(t ,mouse, last_mouse_pos)

    def check_collision(self, t, mouse, last_mouse_pos):
        for s in self.slimes[:]:
            colide, accuracy  = s.check_collision(mouse, last_mouse_pos)
            if (t > s.beat_offset and s.vPos.y > self.screen.get_height()) or colide:
                score, timing, offset = self.explode(s, t)
                new_score = score, timing, offset, accuracy
                print(new_score)
                self.score.append(new_score)

    def explode(self, s, t):
        self.slimes.remove(s)
        color = [(0, 255, 0),(255, 105, 180),(173, 216, 230)][s.color]  # Color based on slime color
        # Generate particles for the explosion
        particles = []
        for _ in range(20):  # Number of particles
            particle = {
                "pos": [s.vPos.x, s.vPos.y],
                "vel": [random.uniform(-2, 2), random.uniform(-2, 2)],
                "radius": random.randint(2, 5),
                "color": color,
                "lifetime": random.randint(40, 60)
            } 
            particles.append(particle)
        self.particles.extend(particles)
        timing_diff = abs(t - s.beat_offset)
        if timing_diff < 0.1:
            text, score, color = "Perfect", 300, (255, 215, 0)  # Gold for perfect
        elif timing_diff < 0.5:
            text, score, color = "Good", 100,(0, 255, 0)  # Green for good
        elif timing_diff < 0.9:
            text, score, color = "Ok", 50, (0, 0, 255)  # Blue for okay
        else:
            text, score, color = "Miss", 0, (255, 0, 0)
        self.add_text(text, color, (s.vPos.x, s.vPos.y))  # Add score text
        pygame.mixer.Sound("components/sounds/explode.mp3").play()
        return score, t - s.beat_offset, s.beat_offset

    def add_text(self, text, color, pos):
        self.texts.append({
            "text": text,
            "color": color,
            "pos": [pos[0], pos[1]],
            "lifetime": 60  # Text will last for 60 frames
        })


