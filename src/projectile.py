import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, angle=0, speed=200, size=(12, 12), ttl=8000, rotate_image=False):
        super().__init__()
        original_image = pygame.image.load(image_path).convert_alpha()

        if rotate_image:
            original_image = pygame.transform.rotate(original_image, angle)

        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect(center=(x, y))

        self.vel = pygame.Vector2(speed, 0).rotate(angle)
        self.spawn_time = pygame.time.get_ticks()
        self.ttl = ttl  # time to live in milliseconds

    def update(self, dt):
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        if pygame.time.get_ticks() - self.spawn_time > self.ttl:
            self.kill()