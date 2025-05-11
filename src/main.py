import pygame
from player import Player
from camera import Camera
from background import Background
from menu import Menu
from maze import Maze

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

def draw_light_effect(screen, player_screen_pos, radius=150):
    width, height = screen.get_size()
    darkness = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 248))  # Fully dark to start

    # Create gradient light mask
    light_mask = pygame.Surface((radius * 2, radius * 2), flags=pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        alpha = int(255 * (1 - (r / radius)))  # transparent center to opaque edge
        pygame.draw.circle(light_mask, (0, 0, 0, alpha), (radius, radius), r)

    # Blit light mask onto the darkness at player's screen position
    light_pos = (player_screen_pos[0] - radius, player_screen_pos[1] - radius)
    darkness.blit(light_mask, light_pos, special_flags=pygame.BLEND_RGBA_SUB)

    screen.blit(darkness, (0, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Out of Angkorwat")
    clock = pygame.time.Clock()


    ikon = pygame.image.load("icon.png")
    pygame.display.set_icon(ikon)


    pygame.mixer.music.load("bgm/background_music.mp3")
    pygame.mixer.music.play(-1)


    # Show the menu
    menu = Menu(screen)
    menu_result = menu.run()
    if menu_result == "quit":
        pygame.quit()
        return


    # Game begins here
    all_sprites = pygame.sprite.Group()
    background_group = pygame.sprite.Group()


    background = Background("assets/tiles/floor.png", 1600, 1600, 64)
    background_group.add(background)


    player = Player(200, 200)
    all_sprites.add(player)
    # Collision Objects
    collidable_objects = pygame.sprite.Group()




    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    tile_size = 64
    wall_img = pygame.image.load("assets/tiles/wall.png").convert_alpha()
    wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))
    


    maze = Maze(25, 25, tile_size, wall_img)
    collidable_objects = maze.create_walls()




    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        player.update(dt, collidable_objects)
        camera.update(player)


        screen.fill((30, 30, 30))

        for bg in background_group:
            screen.blit(bg.image, camera.apply(bg))
        for wall in collidable_objects:
            screen.blit(wall.image, camera.apply(wall))


        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        player_screen_pos = camera.apply(player).center
        draw_light_effect(screen, player_screen_pos, radius=150)


        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
