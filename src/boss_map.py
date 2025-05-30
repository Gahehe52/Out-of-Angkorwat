import pygame
import random
from boss import Boss, Spear, PlayerProjectile

class BossMap:
    TILE_SIZE = 64

    def __init__(self, width=640, height=640):
        self.width = width
        self.height = height

        self.background = pygame.image.load("assets/backgrounds/boss_background.png").convert()
        self.background = pygame.transform.scale(self.background, (width, height))

        self.wall_image = pygame.image.load("assets/tiles/wall.png").convert_alpha()
        self.wall_image = pygame.transform.scale(self.wall_image, (self.TILE_SIZE, self.TILE_SIZE))

        self.surface = pygame.Surface((width, height))
        self.walls = self.create_walls()
        self.wall_rects = [pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE) for x, y in self.walls]

        self.boss = Boss(width // 2, height // 2)
        self.spear = None
        self.last_spear_spawn_time = 0
        self.spear_spawn_interval = 10000  # ms

        self.throw_cooldown = 500  # ms
        self.last_throw_time = 0

        # Font for displaying "Press E" text
        self.font = pygame.font.Font(None, 32)
        self.text_color = (255, 255, 255)

    def create_walls(self):
        walls = []
        tiles_x = self.width // self.TILE_SIZE
        tiles_y = self.height // self.TILE_SIZE
        for x in range(tiles_x):
            walls.append((x * self.TILE_SIZE, 0))
            walls.append((x * self.TILE_SIZE, (tiles_y - 1) * self.TILE_SIZE))
        for y in range(1, tiles_y - 1):
            walls.append((0, y * self.TILE_SIZE))
            walls.append(((tiles_x - 1) * self.TILE_SIZE, y * self.TILE_SIZE))
        return walls

    def update(self, dt, current_time, player, hp_bar, player_projectiles):
        self.boss.update(dt, current_time, player, hp_bar, player_projectiles)

        # Clamp boss inside walls
        bx, by = self.boss.rect.center
        min_x = self.TILE_SIZE + self.boss.rect.width // 2
        max_x = self.width - self.TILE_SIZE - self.boss.rect.width // 2
        min_y = self.TILE_SIZE + self.boss.rect.height // 2
        max_y = self.height - self.TILE_SIZE - self.boss.rect.height // 2
        bx = max(min_x, min(bx, max_x))
        by = max(min_y, min(by, max_y))
        self.boss.rect.center = (bx, by)
        self.boss.hitbox.center = self.boss.rect.center

        # Wall collisions
        for wall_rect in self.wall_rects:
            if self.boss.hitbox.colliderect(wall_rect):
                if self.boss.hitbox.right > wall_rect.left and self.boss.hitbox.left < wall_rect.left:
                    self.boss.rect.right = wall_rect.left
                if self.boss.hitbox.left < wall_rect.right and self.boss.hitbox.right > wall_rect.right:
                    self.boss.rect.left = wall_rect.right
                if self.boss.hitbox.bottom > wall_rect.top and self.boss.hitbox.top < wall_rect.top:
                    self.boss.rect.bottom = wall_rect.top
                if self.boss.hitbox.top < wall_rect.bottom and self.boss.hitbox.bottom > wall_rect.bottom:
                    self.boss.rect.top = wall_rect.bottom
                self.boss.hitbox.center = self.boss.rect.center

            if player.hitbox.colliderect(wall_rect):
                if player.hitbox.right > wall_rect.left and player.hitbox.left < wall_rect.left:
                    player.rect.right = wall_rect.left - (player.hitbox.right - player.rect.right)
                if player.hitbox.left < wall_rect.right and player.hitbox.right > wall_rect.right:
                    player.rect.left = wall_rect.right - (player.hitbox.left - player.rect.left)
                if player.hitbox.bottom > wall_rect.top and player.hitbox.top < wall_rect.top:
                    player.rect.bottom = wall_rect.top - (player.hitbox.bottom - player.rect.bottom)
                if player.hitbox.top < wall_rect.bottom and player.hitbox.bottom > wall_rect.bottom:
                    player.rect.top = wall_rect.bottom - (player.hitbox.top - player.rect.top)
                player.hitbox.topleft = (player.rect.left + 40, player.rect.top + 32)

        # Spear pickup
        if self.spear and self.spear.rect.colliderect(player.hitbox) and not player.has_spear:
            player.has_spear = True
            self.spear = None

        # Handle spear throw
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and player.has_spear and current_time - self.last_throw_time > self.throw_cooldown:
            self.throw_spear(player, player_projectiles)
            player.has_spear = False
            self.last_throw_time = current_time

        # Spear spawn
        if not self.spear and not player.has_spear and current_time - self.last_spear_spawn_time > self.spear_spawn_interval:
            self.spawn_spear()
            self.last_spear_spawn_time = current_time

    def throw_spear(self, player, projectile_group):
        direction = pygame.Vector2(0, 0)
        if player.direction == "up":
            direction = pygame.Vector2(0, -1)
        elif player.direction == "down":
            direction = pygame.Vector2(0, 1)
        elif player.direction == "left":
            direction = pygame.Vector2(-1, 0)
        elif player.direction == "right":
            direction = pygame.Vector2(1, 0)

        proj = PlayerProjectile(player.rect.centerx, player.rect.centery, direction)
        projectile_group.add(proj)

    def spawn_spear(self):
        x = random.randint(100, self.width - 100)
        y = random.randint(100, self.height - 100)
        self.spear = Spear(x, y)

    def draw(self, screen, camera, player, debug=False):
        self.surface.blit(self.background, (0, 0))
        for wall_pos in self.walls:
            self.surface.blit(self.wall_image, wall_pos)
        screen.blit(self.surface, (-camera.offset.x, -camera.offset.y))

        self.boss.draw(screen, camera, debug)
        if self.spear:
            self.spear.draw(screen, camera)

        # Draw spear usage text if player has it
        if player.has_spear:
            text_surface = self.font.render('Press "E" to throw spear', True, self.text_color)
            text_rect = text_surface.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() - 20))
            screen.blit(text_surface, text_rect)
