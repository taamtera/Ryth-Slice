import pygame
from components import SlimeManager
from components import Blade
from components import Map
from components import DataTracking

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 9.8
SPEED = 10
SPAWN_AHEAD = 10

class GameManager:
    pygame.init()
    pygame.display.set_caption("Ryth-Slice")

 
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ticks = 0
        self.current_beat = 0
        self.Blade = Blade()
        self.SlimeManager = SlimeManager(self.screen)
        self.DataTracking = DataTracking(self.SlimeManager)
        self.Map = Map(self.SlimeManager, GRAVITY, SPEED, SPAWN_AHEAD)
        maps = self.Map.loadMaps();
        self.Map.selectMap(maps[0])
        self.last_mouse_pos = pygame.mouse.get_pos()


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = self.clock.tick(FPS)
            self.ticks += dt
            self.current_beat = self.Map.tick(self.ticks)
            if self.Map.last_beat and self.current_beat >= self.Map.last_beat:
                self.running = False
            # print(f"Current Beat: {self.current_beat}")
            # print([s.vPos for s in self.SlimeManager.slimes])
            self.draw()
        self.DataTracking.newRecord(self.Map.map["name"], self.SlimeManager.score)
        self.Map.stopMusic()
        self.DataTracking.display_visualizations(self.screen)
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
            

        pygame.quit()
            
    def draw(self):
        # self.screen.fill((0, 0, 0))
        
        # blue bg image  /components/images/bg.png
        bg_image = pygame.transform.scale(pygame.image.load("components/images/bg.png"), (WIDTH, HEIGHT))
        self.screen.blit(bg_image, (0, 0))
        self.SlimeManager.update(self.current_beat, pygame.mouse.get_pos(), self.last_mouse_pos)
        self.last_mouse_pos = pygame.mouse.get_pos()
        pygame.display.flip()

GameManager().run()


