import pygame
import random
import math
import os
from projectile import Projectile
from entity import Entity

class BossProjectile(Projectile):
    def __init__(self, x, y, angle, speed=200):
        super().__init__(
            x, y,
            image_path="assets/projectiles/fireball.png",
            angle=angle,
            speed=speed,
            size=(12, 12),
            ttl=8000,
            rotate_image=False
        )

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("assets/projectiles/spear.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.Vector2()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

class PlayerProjectile(Projectile):
    def __init__(self, x, y, direction):
        angle = -math.degrees(math.atan2(-direction.y, -direction.x)) + 90
        super().__init__(
            x, y,
            image_path="assets/projectiles/spear.png",
            angle=angle,
            speed=400,
            size=(32, 32),
            ttl=5000,
            rotate_image=True
        )
        self.vel = direction.normalize() * 400

class Boss(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/boss", 128)
        self.hitbox = self.rect.inflate(-40, -40)

        self.projectiles = pygame.sprite.Group()
        self.last_attack_time = 0
        self.attack_interval = 2000

        self.target_pos = pygame.Vector2(x, y)
        self.move_timer = 0
        self.frame_rate = 0.15

    def update(self, dt, current_time, player, hp_bar, player_projectiles):
        if not self.alive:
            return

        # Move
        pos = pygame.Vector2(self.rect.center)
        direction = self.target_pos - pos
        if direction.length() > 1:
            direction = direction.normalize()
            self.rect.center += direction * 100 * dt
            self.hitbox.center = self.rect.center

            angle = math.degrees(math.atan2(-direction.y, direction.x)) % 360
            if 45 <= angle < 135:
                self.direction = "up"
            elif 135 <= angle < 225:
                self.direction = "left"
            elif 225 <= angle < 315:
                self.direction = "down"
            else:
                self.direction = "right"

        self.animate(dt)

        # Pick new target
        self.move_timer += dt
        if self.move_timer > 2:
            self.move_timer = 0
            self.target_pos = pygame.Vector2(random.randint(64, 500 - 64), random.randint(64, 500 - 64))

        # Attack
        if current_time - self.last_attack_time > self.attack_interval:
            self.shoot_projectiles()
            self.last_attack_time = current_time

        self.projectiles.update(dt)

        # Check hit player
        for proj in self.projectiles:
            if proj.rect.colliderect(player.hitbox):
                if current_time - player.last_hit_time >= player.invincibility_duration:
                    player.take_damage(5, current_time, hp_bar)
                    proj.kill()

        # Check hit by player
        for proj in player_projectiles:
            if proj.rect.colliderect(self.hitbox):
                self.take_damage(10)
                proj.kill()

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

        bar_width = 80
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15
        hp_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), camera.apply_rect(pygame.Rect(bar_x, bar_y, bar_width, bar_height)))
        pygame.draw.rect(screen, (255, 0, 0), camera.apply_rect(pygame.Rect(bar_x, bar_y, int(bar_width * hp_ratio), bar_height)))
