import pygame
import os
import math
from abc import ABC, abstractmethod

class Entity(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_folder, size):
        super().__init__()
        self.frames = {"down": [], "up": [], "left": [], "right": []}
        self.direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_rate = 0.1
        self.size = size

        self.load_frames(sprite_folder)
        self.image = self.frames[self.direction][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-40, -40)

        self.health = 100
        self.max_health = 100
        self.alive = True

    @abstractmethod
    def update(self):
        pass
    
    def load_frames(self, folder):
        for direction in self.frames:
            path = os.path.join(folder, direction)
            for filename in sorted(os.listdir(path)):
                if filename.endswith(".png"):
                    img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                    img = pygame.transform.scale(img, (self.size, self.size))
                    self.frames[direction].append(img)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.frame_rate:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
            self.image = self.frames[self.direction][self.current_frame]

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
