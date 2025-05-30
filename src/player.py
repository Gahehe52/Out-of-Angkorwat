import pygame
from entity import Entity
from boss import PlayerProjectile

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/player", 96)
        self.__speed = 200
        self.hitbox = pygame.Rect(self.rect.left + 40, self.rect.top + 32, 16, 32)

        self.footsteep_sound = pygame.mixer.Sound("bgm/sfx/footstep.wav")
        self.footsteep_sound.set_volume(0.5)
        self.footsteep_playing = False

        self.invincible = False
        self.last_hit_time = 0
        self.invincible_timer = 0
        self.invincibility_duration = 1000

        self.has_spear = False
        self.throw_cooldown = 0

    def update(self, dt, *args):
        collisions = args[0] if args else None
        keys = pygame.key.get_pressed()
        dx = dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.__speed * dt
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.__speed * dt
            self.direction = "right"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.__speed * dt
            self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.__speed * dt
            self.direction = "down"

        # Move and collision
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
            if not self.footsteep_playing:
                self.footsteep_sound.play(-1)
                self.footsteep_playing = True
        else:
            self.current_frame = 0
            self.image = self.frames[self.direction][self.current_frame]
            if self.footsteep_playing:
                self.footsteep_sound.stop()
                self.footsteep_playing = False

        # Invincibility flicker
        now = pygame.time.get_ticks()
        if self.invincible:
            if now - self.invincible_timer >= self.invincibility_duration:
                self.invincible = False
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0 if (now // 100) % 2 == 0 else 255)
        else:
            self.image.set_alpha(255)

        self.throw_cooldown = max(0, self.throw_cooldown - dt)

    def take_damage(self, damage_amount, current_time, hp_bar):
        if current_time - self.last_hit_time >= self.invincibility_duration:
            super().take_damage(damage_amount)
            hp_bar.reduce(damage_amount)
            self.last_hit_time = current_time
            self.invincible = True
            self.invincible_timer = current_time

            if self.health <= 0:
                print("Game Over!")

    def throw_spear(self, projectile_group):
        if self.throw_cooldown > 0 or not self.has_spear:
            return
        dir_map = {
            "up": pygame.Vector2(0, -1),
            "down": pygame.Vector2(0, 1),
            "left": pygame.Vector2(-1, 0),
            "right": pygame.Vector2(1, 0)
        }
        direction = dir_map[self.direction]
        proj = PlayerProjectile(self.rect.centerx, self.rect.centery, direction)
        projectile_group.add(proj)
        self.has_spear = False
        self.throw_cooldown = 1  # 1 second cooldown
