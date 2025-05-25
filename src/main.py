import pygame
from player import Player
from camera import Camera
from background import Background
from menu import Menu
from maze import Maze
from hpbar import HPBar

# Constants
INTERNAL_WIDTH, INTERNAL_HEIGHT = 800, 600
FPS = 60

def draw_light_effect(surface, player_screen_pos, radius=150):
    width, height = surface.get_size()
    darkness = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 240))

    light_mask = pygame.Surface((radius * 2, radius * 2), flags=pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        alpha = int(255 * (1 - (r / radius)))
        pygame.draw.circle(light_mask, (0, 0, 0, alpha), (radius, radius), r)

    light_pos = (player_screen_pos[0] - radius, player_screen_pos[1] - radius)
    darkness.blit(light_mask, light_pos, special_flags=pygame.BLEND_RGBA_SUB)

    surface.blit(darkness, (0, 0))

MENU_MUSIC = "bgm/puzzle-game-bright-casual-video-game-music-249202.mp3"
GAME_MUSIC = "bgm/background_music.mp3"

def main():
    pygame.init()
    display_surface = pygame.display.set_mode((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Out of Angkorwat")
    clock = pygame.time.Clock()
    ikon = pygame.image.load("icon.png")
    pygame.display.set_icon(ikon)

    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.play(-1)

    while True:
        menu = Menu(display_surface)
        menu_result = menu.run()
        if menu_result == "quit":
            pygame.quit()
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.play(-1)

        # Setup for fixed FOV surface
        internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))

        all_sprites = pygame.sprite.Group()
        background_group = pygame.sprite.Group()

        background = Background("assets/tiles/floor.png", 1600, 1600, 64)
        background_group.add(background)

        player = Player(50, 50)
        all_sprites.add(player)

        hp_bar = HPBar(10, 10)
        collidable_objects = pygame.sprite.Group()

        camera = Camera(INTERNAL_WIDTH, INTERNAL_HEIGHT)

        tile_size = 64
        wall_img = pygame.image.load("assets/tiles/wall.png").convert_alpha()
        wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))

        maze = Maze(25, 25, tile_size, wall_img)
        collidable_objects, spikes, fires, exit_rect = maze.create_walls()

        running = True
        while running:
            dt = clock.tick(FPS) / 1000
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            player.update(dt, collidable_objects)

            for spike in spikes:
                spike.update(current_time)
            for fire in fires:
                fire.update(current_time)

            for spike in pygame.sprite.spritecollide(player, spikes, False, collided=lambda s1, s2: s1.hitbox.colliderect(s2.rect)):
                if spike.is_active():
                    player.take_damage(10, current_time, hp_bar)

            for fire in pygame.sprite.spritecollide(player, fires, False, collided=lambda s1, s2: s1.hitbox.colliderect(s2.rect)):
                if fire.is_active():
                    player.take_damage(20, current_time, hp_bar)

            if player.health <= 0:
                game_over_text = pygame.font.SysFont(None, 48).render("Game Over!", True, (255, 0, 0))
                internal_surface.blit(game_over_text, (INTERNAL_WIDTH // 2 - 100, INTERNAL_HEIGHT // 2))
                scaled = pygame.transform.scale(internal_surface, display_surface.get_size())
                display_surface.blit(scaled, (0, 0))
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(MENU_MUSIC)
                pygame.mixer.music.play(-1)
                break

            if player.rect.left > exit_rect.right:
                win_text = pygame.font.SysFont(None, 48).render("You Escaped!", True, (0, 255, 0))
                internal_surface.blit(win_text, (INTERNAL_WIDTH // 2 - 100, INTERNAL_HEIGHT // 2))
                scaled = pygame.transform.scale(internal_surface, display_surface.get_size())
                display_surface.blit(scaled, (0, 0))
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(MENU_MUSIC)
                pygame.mixer.music.play(-1)
                break

            camera.update(player)

            internal_surface.fill((30, 30, 30))

            for bg in background_group:
                internal_surface.blit(bg.image, camera.apply(bg))
            for wall in collidable_objects:
                internal_surface.blit(wall.image, camera.apply(wall))
            for spike in spikes:
                spike.draw(internal_surface, camera.apply(spike).topleft)
            for fire in fires:
                fire.draw(internal_surface, camera.apply(fire).topleft)
            for sprite in all_sprites:
                internal_surface.blit(sprite.image, camera.apply(sprite))

            player_screen_pos = camera.apply(player).center
            draw_light_effect(internal_surface, player_screen_pos, radius=150)

            hp_bar.draw(internal_surface)

            # Scale the internal surface to the actual display surface
            # Get window/display size
            win_w, win_h = display_surface.get_size()

            # Calculate scaling factor to preserve aspect ratio
            scale = min(win_w / INTERNAL_WIDTH, win_h / INTERNAL_HEIGHT)

            # Calculate new scaled size
            scaled_w = int(INTERNAL_WIDTH * scale)
            scaled_h = int(INTERNAL_HEIGHT * scale)

            # Center the scaled surface on the screen
            x_offset = (win_w - scaled_w) // 2
            y_offset = (win_h - scaled_h) // 2

            # Scale and blit
            scaled_surface = pygame.transform.scale(internal_surface, (scaled_w, scaled_h))
            display_surface.fill((0, 0, 0))  # Fill background with black to avoid artifacts
            display_surface.blit(scaled_surface, (x_offset, y_offset))
            pygame.display.flip()


if __name__ == "__main__":
    main()
