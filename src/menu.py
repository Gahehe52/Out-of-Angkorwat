import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.internal_resolution = (800, 600)
        self.font = pygame.font.Font(font_path, 36) if font_path else pygame.font.SysFont("Arial", 36)
        self.running = True
        self.state = "main"

        self.main_options = ["start", "options", "quit"]
        self.options_menu = ["volume", "fullscreen", "back"]

        self.bg_image_raw = pygame.image.load("BrickBG.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image_raw, self.internal_resolution)

        self.button_width_ratio = 0.3
        self.button_height_ratio = 0.25
        self.spacing_ratio = 0.04

        self.button_size = (
            int(self.internal_resolution[0] * self.button_width_ratio),
            int(self.internal_resolution[1] * self.button_height_ratio)
        )

        self.button_images = {}
        for key in ["start", "options", "quit", "fullscreen", "back", "volume"]:
            path = f"assets/Menu/{key.capitalize()}.png" if key != "quit" else "assets/Menu/Quit.png"
            self.button_images[key] = pygame.transform.scale(
                pygame.image.load(path).convert_alpha(),
                self.button_size
            )

        self.option_rects = []
        self.checkbox_rects = {}
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

        screen_height = self.internal_resolution[1]
        button_height = self.button_size[1]
        spacing = int(screen_height * self.spacing_ratio)

        total_height = len(options) * button_height + (len(options) - 1) * spacing
        start_y = (screen_height - total_height) // 2

        for i in range(len(options)):
            center_x = self.internal_resolution[0] // 2
            top_y = start_y + i * (button_height + spacing)
            rect = pygame.Rect(0, 0, *self.button_size)
            rect.center = (center_x, top_y + button_height // 2)
            self.option_rects.append(rect)

            option = options[i]
            if option in ["volume", "fullscreen"]:
                checkbox_size = 30
                checkbox_rect = pygame.Rect(
                    rect.right + 10,
                    rect.centery - checkbox_size // 2,
                    checkbox_size,
                    checkbox_size
                )
                self.checkbox_rects[option] = checkbox_rect

    def draw(self):
        scaled_bg = pygame.transform.scale(self.bg_image, self.screen.get_size())
        self.screen.blit(scaled_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        scale_x = self.screen.get_width() / self.internal_resolution[0]
        scale_y = self.screen.get_height() / self.internal_resolution[1]

        for i, option in enumerate(self.get_current_options()):
            img = self.button_images[option].copy()

            # Scale rect for interaction
            display_rect = self.option_rects[i].copy()
            display_rect.x = int(display_rect.x * scale_x)
            display_rect.y = int(display_rect.y * scale_y)
            display_rect.width = int(display_rect.width * scale_x)
            display_rect.height = int(display_rect.height * scale_y)

            if display_rect.collidepoint(mouse_pos):
                hover_index = i
                if self.last_hover_index != i:
                    self.hover_sound.play()
                overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                overlay.fill((80, 80, 80, 80))
                img.blit(overlay, (0, 0))

            self.screen.blit(pygame.transform.scale(img, (display_rect.width, display_rect.height)), (display_rect.x, display_rect.y))

            if option in self.checkbox_rects:
                checked = self.is_muted if option == "volume" else self.is_fullscreen
                checkbox_rect = self.checkbox_rects[option]
                checkbox_rect_display = pygame.Rect(
                    int(checkbox_rect.x * scale_x),
                    int(checkbox_rect.y * scale_y),
                    int(checkbox_rect.width * scale_x),
                    int(checkbox_rect.height * scale_y)
                )
                pygame.draw.rect(self.screen, (200, 200, 200), checkbox_rect_display)
                pygame.draw.rect(self.screen, (0, 0, 0), checkbox_rect_display, 2)
                if checked:
                    check = self.font.render("✓", True, (0, 0, 0))
                    check_rect = check.get_rect(center=checkbox_rect_display.center)
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
                scale_x = self.screen.get_width() / self.internal_resolution[0]
                scale_y = self.screen.get_height() / self.internal_resolution[1]

                for key, rect in self.checkbox_rects.items():
                    scaled_rect = pygame.Rect(
                        int(rect.x * scale_x),
                        int(rect.y * scale_y),
                        int(rect.width * scale_x),
                        int(rect.height * scale_y)
                    )
                    if scaled_rect.collidepoint(pos):
                        if key == "volume":
                            self.toggle_volume()
                        elif key == "fullscreen":
                            self.toggle_fullscreen()
                        return None

                for i, rect in enumerate(self.option_rects):
                    scaled_rect = pygame.Rect(
                        int(rect.x * scale_x),
                        int(rect.y * scale_y),
                        int(rect.width * scale_x),
                        int(rect.height * scale_y)
                    )
                    if scaled_rect.collidepoint(pos):
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
            self.screen = pygame.display.set_mode(self.internal_resolution, pygame.RESIZABLE)
        self.bg_image = pygame.transform.scale(self.bg_image_raw, self.internal_resolution)
        self.create_option_rects()

    def run(self):
        self.create_option_rects()
        while self.running:
            action = self.handle_input()
            if action in self.main_options:
                return action
            self.draw()