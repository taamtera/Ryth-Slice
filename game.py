import pygame
from components import SlimeManager
from components import Blade
from components import Map

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 9.8
SPEED = 10
SPAWN_AHEAD = 10

class GameManager:
    pygame.init()
    pygame.display.set_caption("slimeFalling")

 
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ticks = 0
        self.current_beat = 0
        self.Blade = Blade()
        self.SlimeManager = SlimeManager()
        self.Map = Map(self.SlimeManager, GRAVITY, SPEED, SPAWN_AHEAD)
        
        maps = self.Map.loadMaps();
        self.Map.selectMap(maps[0])


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = self.clock.tick(FPS)
            self.ticks += dt
            self.current_beat = self.Map.tick(self.ticks)
            print(f"Current Beat: {self.current_beat}")
            # print([s.vPos for s in self.SlimeManager.slimes])
            self.draw()
        pygame.quit()
            
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.SlimeManager.draw(self.screen, self.current_beat)
        pygame.display.flip()

GameManager().run()


