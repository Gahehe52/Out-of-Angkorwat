import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path="assets/tiles/floor.png", width=1600, height=1200, tile_size=64):
        super().__init__()
        tile_image = pygame.image.load(image_path).convert()
        tile_image = pygame.transform.scale(tile_image, (tile_size, tile_size))


        self.image = pygame.Surface((width, height))
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                self.image.blit(tile_image, (x, y))


        self.rect = self.image.get_rect(topleft=(0, 0))


    def update(self, dt):
        pass  # No dynamic behavior

