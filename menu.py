import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.font = pygame.font.Font(font_path, 36) if font_path else pygame.font.SysFont("Arial", 36)
        self.running = True
        self.state = "main"

        self.main_options = ["start", "options", "quit"]
        self.options_menu = ["volume", "fullscreen", "back"]

        self.bg_image = pygame.image.load("BrickBG.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        screen_width, screen_height = self.screen.get_size()
        self.button_width_ratio = 0.3
        self.button_height_ratio = 0.25
        self.spacing_ratio = 0.04

        self.button_size = (
            int(screen_width * self.button_width_ratio),
            int(screen_height * self.button_height_ratio)
        )

        self.button_images = {
            "start": pygame.image.load("assets/Menu/start.png").convert_alpha(),
            "options": pygame.image.load("assets/Menu/options.png").convert_alpha(),
            "quit": pygame.image.load("assets/Menu/Quit.png").convert_alpha(),
            "fullscreen": pygame.image.load("assets/Menu/FullScreen.png").convert_alpha(),
            "back": pygame.image.load("assets/Menu/Back.png").convert_alpha(),
            "volume": pygame.image.load("assets/Menu/Volume.png").convert_alpha(),
        }


        for key in self.button_images:
            path = f"assets/Menu/{key.capitalize()}.png" if key != "quit" else "assets/Menu/Quit.png"
            self.button_images[key] = pygame.transform.scale(
                pygame.image.load(path).convert_alpha(),
                self.button_size
            )


        self.option_rects = []
        self.checkbox_rects = {}  # Simpan posisi checkbox
        self.last_hover_index = None

        self.hover_sound = pygame.mixer.Sound("bgm/sfx/ButtonClick.mp3")

        self.is_muted = False
        self.is_fullscreen = False

    def get_current_options(self):
        return self.main_options if self.state == "main" else self.options_menu

    def create_option_rects(self):
        self.option_rects = []
        self.checkbox_rects.clear()
        options = self.get_current_options()

        screen_height = self.screen.get_height()
        button_height = self.button_size[1]
        spacing = int(screen_height * self.spacing_ratio)

        total_height = len(options) * button_height + (len(options) - 1) * spacing
        start_y = (screen_height - total_height) // 2

        for i in range(len(options)):
            center_x = self.screen.get_width() // 2
            top_y = start_y + i * (button_height + spacing)
            rect = pygame.Rect(0, 0, *self.button_size)
            rect.center = (center_x, top_y + button_height // 2)
            self.option_rects.append(rect)

            # Tentukan rect checkbox (hanya untuk volume dan fullscreen)
            option = options[i]
            if option in ["volume", "fullscreen"]:
                checkbox_size = 30
                checkbox_rect = pygame.Rect(
                    rect.right + 10,  # Geser ke kanan dari tombol
                    rect.centery - checkbox_size // 2,
                    checkbox_size,
                    checkbox_size
                )
                self.checkbox_rects[option] = checkbox_rect

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        options = self.get_current_options()
        for i, option in enumerate(options):
            key = option.lower()

            # Tombol utama
            if key in self.button_images:
                img = self.button_images[key].copy()
            else:
                img = pygame.Surface(self.button_size)
                img.fill((50, 150, 50))
                text_surf = self.font.render(option.upper(), True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=(self.button_size[0]//2, self.button_size[1]//2))
                img.blit(text_surf, text_rect)

            if self.option_rects[i].collidepoint(mouse_pos):
                hover_index = i
                if self.last_hover_index != i:
                    self.hover_sound.play()
                overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                overlay.fill((80, 80, 80, 80))
                img.blit(overlay, (0, 0))

            self.screen.blit(img, self.option_rects[i])

            # Gambar checkbox jika perlu
            if option in self.checkbox_rects:
                checked = (self.is_muted if option == "volume" else self.is_fullscreen)
                checkbox_rect = self.checkbox_rects[option]
                pygame.draw.rect(self.screen, (200, 200, 200), checkbox_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), checkbox_rect, 2)
                if checked:
                    check = self.font.render("✓", True, (0, 0, 0))
                    check_rect = check.get_rect(center=checkbox_rect.center)
                    self.screen.blit(check, check_rect)

        self.last_hover_index = hover_index
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                # Prioritaskan klik checkbox
                for key, rect in self.checkbox_rects.items():
                    if rect.collidepoint(pos):
                        if key == "volume":
                            self.toggle_volume()
                        elif key == "fullscreen":
                            self.toggle_fullscreen()
                        return None

                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        selected_option = self.get_current_options()[i]

                        if self.state == "main":
                            if selected_option == "options":
                                self.state = "options"
                                self.create_option_rects()
                                return None
                            else:
                                return selected_option

                        elif self.state == "options":
                            if selected_option == "volume":
                                self.toggle_volume()
                            elif selected_option == "fullscreen":
                                self.toggle_fullscreen()
                            elif selected_option == "back":
                                self.state = "main"
                                self.create_option_rects()
        return None

    def toggle_volume(self):
        self.is_muted = not self.is_muted
        pygame.mixer.music.set_volume(0.0 if self.is_muted else 1.0)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 600))
        self.bg_image = pygame.transform.scale(pygame.image.load("BrickBG.png").convert(), self.screen.get_size())

        screen_width, screen_height = self.screen.get_size()
        self.button_size = (
            int(screen_width * self.button_width_ratio),
            int(screen_height * self.button_height_ratio)
        )

        for key in self.button_images:
            self.button_images[key] = pygame.transform.scale(
                pygame.image.load(f"assets/Menu/{key}.png").convert_alpha(),
                self.button_size
            )

        self.create_option_rects()

    def run(self):
        self.create_option_rects()
        while self.running:
            action = self.handle_input()
            if action in self.main_options:
                return action
            self.draw()
