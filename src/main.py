import pygame
from player import Player
from camera import Camera
from background import Background
from menu import Menu
from maze import Maze
from hpbar import HPBar

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

def draw_light_effect(screen, player_screen_pos, radius=150):
    width, height = screen.get_size()
    darkness = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 240))

    light_mask = pygame.Surface((radius * 2, radius * 2), flags=pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        alpha = int(255 * (1 - (r / radius)))
        pygame.draw.circle(light_mask, (0, 0, 0, alpha), (radius, radius), r)

    light_pos = (player_screen_pos[0] - radius, player_screen_pos[1] - radius)
    darkness.blit(light_mask, light_pos, special_flags=pygame.BLEND_RGBA_SUB)

    screen.blit(darkness, (0, 0))

MENU_MUSIC = "bgm/puzzle-game-bright-casual-video-game-music-249202.mp3"
GAME_MUSIC = "bgm/background_music.mp3"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Out of Angkorwat")
    clock = pygame.time.Clock()

    ikon = pygame.image.load("icon.png")
    pygame.display.set_icon(ikon)

    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.play(-1)

    while True:
        menu = Menu(screen)
        menu_result = menu.run()
        if menu_result == "quit":
            pygame.quit()
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.play(-1)

        all_sprites = pygame.sprite.Group()
        background_group = pygame.sprite.Group()

        background = Background("assets/tiles/floor.png", 1600, 1600, 64)
        background_group.add(background)

        player = Player(50, 50)
        all_sprites.add(player)

        hp_bar = HPBar(10, 10)
        collidable_objects = pygame.sprite.Group()

        camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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

            # Update traps
            for spike in spikes:
                spike.update(current_time)
            for fire in fires:
                fire.update(current_time)

            # Trap damage
            for spike in pygame.sprite.spritecollide(player, spikes, False, collided=lambda s1, s2: s1.hitbox.colliderect(s2.rect)):
                if spike.is_active():
                    player.take_damage(10, current_time, hp_bar)

            for fire in pygame.sprite.spritecollide(player, fires, False, collided=lambda s1, s2: s1.hitbox.colliderect(s2.rect)):
                if fire.is_active():
                    player.take_damage(20, current_time, hp_bar)

            # Game Over
            if player.health <= 0:
                game_over_text = pygame.font.SysFont(None, 48).render("Game Over!", True, (255, 0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(MENU_MUSIC)
                pygame.mixer.music.play(-1)
                menu_result = menu.run()
                if menu_result == "quit":
                    pygame.quit()
                    return
                running = False
                continue

            # Check win condition
            if player.rect.left > exit_rect.right:
                win_text = pygame.font.SysFont(None, 48).render("You Escaped!", True, (0, 255, 0))
                screen.blit(win_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(MENU_MUSIC)
                pygame.mixer.music.play(-1)
                menu_result = menu.run()
                if menu_result == "quit":
                    pygame.quit()
                    return
                running = False
                continue


            camera.update(player)

            screen.fill((30, 30, 30))

            for bg in background_group:
                screen.blit(bg.image, camera.apply(bg))
            for wall in collidable_objects:
                screen.blit(wall.image, camera.apply(wall))
            for spike in spikes:
                spike.draw(screen, camera.apply(spike).topleft)
            for fire in fires:
                fire.draw(screen, camera.apply(fire).topleft)

            for sprite in all_sprites:
                screen.blit(sprite.image, camera.apply(sprite))

            player_screen_pos = camera.apply(player).center
            draw_light_effect(screen, player_screen_pos, radius=150)

            hp_bar.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    main()
