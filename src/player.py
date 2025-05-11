import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_frames("assets/player")
        self.direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_rate = 0.1
        self.image = self.frames[self.direction][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))


        # Define a smaller collision rect (hitbox)
        self.hitbox = pygame.Rect(self.rect.left + 40, self.rect.top + 32, 16, 32)  # tweak these values
        self.speed = 200


    def load_frames(self, folder):
        self.frames = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        for direction in self.frames:
            path = os.path.join(folder, direction)
            for filename in sorted(os.listdir(path)):
                if filename.endswith(".png"):
                    img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                    img = pygame.transform.scale(img, (96, 96))
                    self.frames[direction].append(img)

    def update(self, dt, *args):
        collisions = args[0] if args else None
        keys = pygame.key.get_pressed()
        dx = dy = 0


        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed * dt
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed * dt
            self.direction = "right"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed * dt
            self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed * dt
            self.direction = "down"


        # Move and check collision
        self.rect.x += dx
        self.hitbox.x += dx
        if collisions:
            for sprite in collisions:
                if self.hitbox.colliderect(sprite.rect):
                    self.rect.x -= dx
                    self.hitbox.x -= dx


        self.rect.y += dy
        self.hitbox.y += dy
        if collisions:
            for sprite in collisions:
                if self.hitbox.colliderect(sprite.rect):
                    self.rect.y -= dy
                    self.hitbox.y -= dy


        if dx != 0 or dy != 0:
            self.animate(dt)
        else:
            self.current_frame = 0
            self.image = self.frames[self.direction][self.current_frame]



    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.frame_rate:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
            self.image = self.frames[self.direction][self.current_frame]

