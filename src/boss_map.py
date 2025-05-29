import pygame
from boss import Boss

class BossMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((50, 0, 50))  # Purple background

        self.boss = Boss(width // 2, height // 2)

    def update(self, dt, current_time, player, hp_bar):
        self.boss.update(dt, current_time, player, hp_bar)

    def draw(self, screen, camera):
        screen.blit(self.surface, (0, 0))
        self.boss.draw(screen, camera)
