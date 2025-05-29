import pygame
import random
import math
import os

class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed=200):
        super().__init__()
        original_image = pygame.image.load("assets/projectiles/fireball.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (12, 12))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.Vector2(speed, 0).rotate(angle)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        if pygame.time.get_ticks() - self.spawn_time > 8000:
            self.kill()

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("assets/projectiles/spear.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.Vector2()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        original_image = pygame.image.load("assets/projectiles/spear.png").convert_alpha()
        angle = -math.degrees(math.atan2(-direction.y, -direction.x)) + 90
        rotated = pygame.transform.rotate(original_image, angle)
        self.image = pygame.transform.scale(rotated, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = direction.normalize() * 400
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 128
        self.load_frames("assets/boss")
        self.direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.frame_rate = 0.15

        self.image = self.frames[self.direction][self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-40, -40)

        self.hp = 100
        self.max_hp = 100
        self.alive = True

        self.projectiles = pygame.sprite.Group()
        self.last_attack_time = 0
        self.attack_interval = 2000  # ms
        self.target_pos = pygame.Vector2(x, y)
        self.move_timer = 0

    def load_frames(self, folder):
        self.frames = {dir: [] for dir in ["down", "up", "left", "right"]}
        for direction in self.frames:
            path = os.path.join(folder, direction)
            for filename in sorted(os.listdir(path)):
                if filename.endswith(".png"):
                    img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                    img = pygame.transform.scale(img, (self.size, self.size))
                    self.frames[direction].append(img)

    def update(self, dt, current_time, player, hp_bar, player_projectiles):
        if not self.alive:
            return

        # Movement logic
        pos = pygame.Vector2(self.rect.center)
        direction = self.target_pos - pos
        if direction.length() > 1:
            direction = direction.normalize()
            self.rect.center += direction * 100 * dt
            self.hitbox.center = self.rect.center

            # Set animation direction
            angle = math.degrees(math.atan2(-direction.y, direction.x)) % 360
            if 45 <= angle < 135:
                self.direction = "up"
            elif 135 <= angle < 225:
                self.direction = "left"
            elif 225 <= angle < 315:
                self.direction = "down"
            else:
                self.direction = "right"

        # Animate
        self.animation_timer += dt
        if self.animation_timer >= self.frame_rate:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
            self.image = self.frames[self.direction][self.current_frame]

        # Choose new position
        self.move_timer += dt
        if self.move_timer > 2:
            self.move_timer = 0
            self.target_pos = pygame.Vector2(
                random.randint(64, 500 - 64),
                random.randint(64, 500 - 64)
            )

        # Shoot projectiles
        if current_time - self.last_attack_time > self.attack_interval:
            self.shoot_projectiles()
            self.last_attack_time = current_time

        self.projectiles.update(dt)

        # Boss projectiles hit player
        for proj in self.projectiles:
            if proj.rect.colliderect(player.hitbox):
                if current_time - player.last_hit_time >= player.invincibility_duration:
                    player.take_damage(5, current_time, hp_bar)
                    proj.kill()

        # Player projectiles hit boss
        for proj in player_projectiles:
            if proj.rect.colliderect(self.hitbox):
                self.hp -= 10
                proj.kill()
                if self.hp <= 0:
                    self.hp = 0
                    self.alive = False

    def shoot_projectiles(self):
        for angle in range(0, 360, 20):
            proj = BossProjectile(self.rect.centerx, self.rect.centery, angle)
            self.projectiles.add(proj)

    def draw(self, screen, camera, debug=False):
        screen.blit(self.image, camera.apply(self))
        for proj in self.projectiles:
            screen.blit(proj.image, camera.apply(proj))
            if debug:
                pygame.draw.rect(screen, (255, 0, 0), camera.apply(proj), 1)
        if debug:
            pygame.draw.rect(screen, (0, 255, 0), camera.apply_rect(self.hitbox), 1)

        # HP bar
        bar_width = 80
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (0, 0, 0), camera.apply_rect(pygame.Rect(bar_x, bar_y, bar_width, bar_height)))
        pygame.draw.rect(screen, (255, 0, 0), camera.apply_rect(pygame.Rect(bar_x, bar_y, int(bar_width * hp_ratio), bar_height)))
