import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self, target):
        # Center the camera on the target (e.g., player)
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.y = target.rect.centery - self.height // 2

    def apply(self, target):
        return target.rect.move(-self.offset.x, -self.offset.y)
