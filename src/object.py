import pygame
import time

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = None
        self.rect = None

    def draw(self, screen, pos=None):
        if self.image:
            screen.blit(self.image, pos or self.rect.topleft)

class Object(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

class AnimatedObject(GameObject):
    def __init__(self, x, y, images, frame_duration=150, invisible_duration=1500):
        super().__init__(x, y)
        self.images = images
        self.index = 0
        self.forward = True
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.frame_duration = frame_duration  # milliseconds per frame
        self.last_update = pygame.time.get_ticks()

        self.visible = True
        self.invisible_duration = invisible_duration  # milliseconds
        self.last_cycle_time = 0
        self.full_cycle = len(images) * 2 - 2  # forward and back
        self.cycle_counter = 0

    def update(self, current_time):
        if not self.visible:
            if current_time - self.last_cycle_time >= self.invisible_duration:
                self.visible = True
                self.index = 0
                self.forward = True
                self.cycle_counter = 0
                self.image = self.images[self.index]
            else:
                return

        if current_time - self.last_update > self.frame_duration:
            self.last_update = current_time

            # Move forward or backward
            if self.forward:
                self.index += 1
                if self.index == len(self.images):
                    self.index -= 2
                    self.forward = False
            else:
                self.index -= 1
                if self.index < 0:
                    self.index = 1
                    self.forward = True

            self.cycle_counter += 1
            if self.cycle_counter >= self.full_cycle:
                self.visible = False
                self.last_cycle_time = current_time

            self.image = self.images[self.index]

    def draw(self, screen, pos=None):
        if self.visible:
            screen.blit(self.image, pos or self.rect.topleft)

    def is_active(self):
        return self.visible
