import pygame
import random
from collections import namedtuple
Vector2D = namedtuple("Vector2D", ["x", "y"])

slime_images = [
    pygame.image.load("components/images/slime1.png"),
    pygame.image.load("components/images/slime2.png"),
    pygame.image.load("components/images/slime3.png")
]

class Slime:
    def __init__(self, r, vPos, vVel, beat_offset, m_grav, m_spd):
        self.vPos0 = vPos
        self.vVel0 = vVel
        self.vPos = None
        self.beat_offset = beat_offset
        self.r = r
        self.m_spd = m_spd   # Speed multiplier
        self.m_grav = m_grav   # Gravity multiplier
        self.animation_frame = 0  # Track the current animation frame
        self.animation_speed = 0.1  # Speed of animation (adjust as needed)
        self.color = random.randint(0,2)  # Random color for the slime
        self.selected_slime = slime_images[self.color]  # Select the slime image based on the random color
        self.keyframe_count = 4  # Number of keyframes in each image
        self.keyframe_width = self.selected_slime.get_width() // self.keyframe_count
        self.keyframe_height = self.selected_slime.get_height()

    def position(self, t):
        t = (t - self.beat_offset) * self.m_spd
        self.vPos = Vector2D(
            self.vPos0.x + self.vVel0.x * t,
            self.vPos0.y + self.vVel0.y * t + (self.m_grav * t ** 2) / 2
        )

    def draw(self, screen, t):
        self.position(t)
        # Calculate the current frame based on time
        self.animation_frame = (self.animation_frame + self.animation_speed) % self.keyframe_count
        current_frame = int(self.animation_frame)
        # Extract the current keyframe from the sprite sheet
        keyframe_rect = pygame.Rect(
            current_frame * self.keyframe_width, 0, self.keyframe_width, self.keyframe_height
        )
        keyframe_image = self.selected_slime.subsurface(keyframe_rect)
        # Draw the current keyframe
        screen.blit(keyframe_image, (self.vPos.x - self.r, self.vPos.y - self.r))

    
    def check_collision(self, mouse_pos, last_mouse_pos):
        """Fast collision check with accurate hit confirmation"""
        # Calculate mouse movement vector components
        dx = mouse_pos[0] - last_mouse_pos[0]
        dy = mouse_pos[1] - last_mouse_pos[1]
        distance_sq = dx*dx + dy*dy
        
        # If mouse hasn't moved, simple point collision check
        if distance_sq == 0:
            hit = ((mouse_pos[0] - self.vPos.x)**2 + 
                (mouse_pos[1] - self.vPos.y)**2) <= self.r**2
            return hit, 1.0 if hit else 0.0
        
        # Fast sampling check (every 10 pixels)
        steps = min(10, int((distance_sq**0.5) / 10) + 1)
        potential_hit = False
        
        for i in range(steps + 1):
            t = i / steps
            check_x = last_mouse_pos[0] + dx * t
            check_y = last_mouse_pos[1] + dy * t
            
            if ((check_x - self.vPos.x)**2 + 
                (check_y - self.vPos.y)**2) <= self.r**2:
                potential_hit = True
                break
        
        if not potential_hit:
            return False, 0.0
        
        # Accurate line-circle intersection check
        # Vector from line start to circle center
        fx = last_mouse_pos[0] - self.vPos.x
        fy = last_mouse_pos[1] - self.vPos.y
        
        # Quadratic coefficients
        a = dx*dx + dy*dy
        b = 2 * (fx*dx + fy*dy)
        c = fx*fx + fy*fy - self.r*self.r
        
        discriminant = b*b - 4*a*c
        
        if discriminant < 0:
            return False, 0.0
        
        discriminant = discriminant**0.5
        t1 = (-b - discriminant) / (2*a)
        t2 = (-b + discriminant) / (2*a)
        
        # Find valid intersection points (0-1 range)
        hits = []
        if 0 <= t1 <= 1:
            hits.append(t1)
        if 0 <= t2 <= 1:
            hits.append(t2)
        
        if not hits:
            return False, 0.0
        
        # Calculate accuracy (closest point on line to circle center)
        closest_t = max(0, min(1, -b/(2*a) if a != 0 else 0))
        closest_dist_sq = ((last_mouse_pos[0] + dx*closest_t - self.vPos.x)**2 +
                        (last_mouse_pos[1] + dy*closest_t - self.vPos.y)**2)
        
        # Normalized accuracy (1.0 = direct hit, <1.0 = near miss)
        accuracy = max(0, 1 - closest_dist_sq/(self.r*self.r))
        
        return True, accuracy
