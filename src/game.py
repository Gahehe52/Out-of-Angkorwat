import pygame
from player import Player
from camera import Camera
from background import Background
from menu import Menu
from maze import Maze
from hpbar import HPBar
from boss_map import BossMap
from cutscene import Cutscene
from end_cutscene import EndCutscene
from prolog import Prolog  # ✅ NEW IMPORT

class Game:
    def __init__(self):
        self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT = 800, 600
        self.FPS = 60
        self.MENU_MUSIC = "bgm/puzzle-game-bright-casual-video-game-music-249202.mp3"
        self.GAME_MUSIC = "bgm/background_music.mp3"
        self.BOSS_MUSIC = "bgm/boss_music.mp3"
        self.NOISES = "bgm/sfx/crowd-noise.mp3"
        self.FOOTSTEPS = "bgm/sfx/footstep.wav"

    def draw_light_effect(self, surface, player_screen_pos, radius=150):
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

    def run(self):
        pygame.init()
        display_surface = pygame.display.set_mode((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Out of Angkorwat")
        clock = pygame.time.Clock()
        ikon = pygame.image.load("icon.png")
        pygame.display.set_icon(ikon)

        pygame.mixer.music.load(self.MENU_MUSIC)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        while True:
            menu = Menu(display_surface)
            menu_result = menu.run()
            if menu_result == "quit":
                pygame.quit()
                return

            prolog_dialogue = [
                "Suatu hari, di perjalanan wisata sekolah...",
                "Guru: Anak-anak, kita sudah sampai di Angkorwat, silahkan turun...",
                "Guru: Dan ingat, JANGAN MASUK KE BAGIAN KUIL YANG TERBENGKALAI!",
                "Leyberg: *dalam hati* Apaan sih, masa udah bayar wisata ga boleh masuk?",
                "Leyberg: *dalam hati* Lagian emang kenapa sih kalau masuk? Ada Golem?",
                "Leyberg: *dalam hati* Gak mungkin lah! Bodo ah, masuk aja!"
            ]
            pygame.mixer.music.stop()
            # Show prolog first
            pygame.mixer.music.load(self.NOISES)
            pygame.mixer.music.play(-1)
            Prolog(display_surface, prolog_dialogue, "intro_background.png").run()

            def start_game_after_cutscene():
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.GAME_MUSIC)
                pygame.mixer.music.play(-1)

            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.FOOTSTEPS)
            pygame.mixer.music.play(-1)
            Cutscene(display_surface, start_game_after_cutscene).run()

            internal_surface = pygame.Surface((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))

            all_sprites = pygame.sprite.Group()
            background_group = pygame.sprite.Group()

            background = Background("assets/tiles/floor.png", 1600, 1600, 64)
            background_group.add(background)

            player = Player(50, 50)
            all_sprites.add(player)

            hp_bar = HPBar(10, 10)
            collidable_objects = pygame.sprite.Group()
            spikes = pygame.sprite.Group()
            fires = pygame.sprite.Group()
            camera = Camera(self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT)

            tile_size = 64
            wall_img = pygame.image.load("assets/tiles/wall.png").convert_alpha()
            wall_img = pygame.transform.scale(wall_img, (tile_size, tile_size))

            maze = Maze(25, 25, tile_size, wall_img)
            collidable_objects, spikes, fires, exit_rect = maze.create_walls()

            in_boss_fight = False
            boss_map = None
            player_projectiles = pygame.sprite.Group()

            running = True
            while running:
                dt = clock.tick(self.FPS) / 1000
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                if not in_boss_fight:
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
                        self.display_end_text(internal_surface, display_surface, "Game Over!", (255, 0, 0))
                        player.footsteep_sound.stop()
                        break

                    if player.rect.left > exit_rect.right:
                        in_boss_fight = True
                        player.rect.topleft = (50, 50)
                        player.hitbox.topleft = (player.rect.left + 40, player.rect.top + 32)
                        camera = Camera(self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT)
                        boss_map = BossMap()
                        collidable_objects.empty()
                        spikes.empty()
                        fires.empty()
                        all_sprites.empty()
                        all_sprites.add(player)

                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(self.BOSS_MUSIC)
                        pygame.mixer.music.play(-1)
                        continue

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
                    self.draw_light_effect(internal_surface, player_screen_pos, radius=150)
                    hp_bar.draw(internal_surface)
                else:
                    player.update(dt, pygame.sprite.Group())
                    player_projectiles.update(dt)
                    boss_map.update(dt, current_time, player, hp_bar, player_projectiles)
                    camera.update(player)

                    internal_surface.fill((0, 0, 0))
                    boss_map.draw(internal_surface, camera, player)

                    for proj in player_projectiles:
                        internal_surface.blit(proj.image, camera.apply(proj))

                    internal_surface.blit(player.image, camera.apply(player))
                    hp_bar.draw(internal_surface)

                    if player.health <= 0:
                        self.display_end_text(internal_surface, display_surface, "Game Over!", (255, 0, 0))
                        player.footsteep_sound.stop()
                        break

                    if not boss_map.boss.alive:
                        player.footsteep_sound.stop()

                        # Show victory message
                        self.display_end_text(
                            internal_surface,
                            display_surface,
                            "You Win!\nYou've Defeated Goru",
                            (0, 255, 0)
                        )

                        def return_to_menu():
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load(self.MENU_MUSIC)
                            pygame.mixer.music.play(-1)

                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(self.FOOTSTEPS)
                        pygame.mixer.music.play(-1)
                        EndCutscene(display_surface, return_to_menu).run()
                        break


                self.scale_and_blit(display_surface, internal_surface)

    def display_end_text(self, surface, display_surface, text, color):
        font = pygame.font.SysFont(None, 48)
        lines = text.split("\n")
        surface.fill((0, 0, 0))  # Clear the screen

        for i, line in enumerate(lines):
            message = font.render(line, True, color)
            text_rect = message.get_rect(center=(self.INTERNAL_WIDTH // 2, self.INTERNAL_HEIGHT // 2 + i * 50))
            surface.blit(message, text_rect)

        scaled = pygame.transform.scale(surface, display_surface.get_size())
        display_surface.blit(scaled, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2500)

    def scale_and_blit(self, display_surface, internal_surface):
        win_w, win_h = display_surface.get_size()
        scale = min(win_w / self.INTERNAL_WIDTH, win_h / self.INTERNAL_HEIGHT)
        scaled_w = int(self.INTERNAL_WIDTH * scale)
        scaled_h = int(self.INTERNAL_HEIGHT * scale)
        x_offset = (win_w - scaled_w) // 2
        y_offset = (win_h - scaled_h) // 2

        scaled_surface = pygame.transform.scale(internal_surface, (scaled_w, scaled_h))
        display_surface.fill((0, 0, 0))
        display_surface.blit(scaled_surface, (x_offset, y_offset))
        pygame.display.flip()
