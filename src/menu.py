import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.internal_resolution = (800, 600)
        self.internal_surface = pygame.Surface(self.internal_resolution)
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

    def get_internal_mouse_pos(self, mouse_pos):
        screen_w, screen_h = self.screen.get_size()
        internal_w, internal_h = self.internal_resolution
        scale = min(screen_w / internal_w, screen_h / internal_h)
        scaled_w, scaled_h = internal_w * scale, internal_h * scale
        x_offset = (screen_w - scaled_w) / 2
        y_offset = (screen_h - scaled_h) / 2

        x = (mouse_pos[0] - x_offset) / scale
        y = (mouse_pos[1] - y_offset) / scale
        return int(x), int(y)

    def draw(self):
        # Draw background
        self.internal_surface.blit(self.bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        internal_mouse_pos = self.get_internal_mouse_pos(mouse_pos)
        hover_index = None

        for i, option in enumerate(self.get_current_options()):
            img = self.button_images[option].copy()
            rect = self.option_rects[i]

            if rect.collidepoint(internal_mouse_pos):
                hover_index = i
                if self.last_hover_index != i:
                    self.hover_sound.play()
                overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                overlay.fill((80, 80, 80, 80))
                img.blit(overlay, (0, 0))

            self.internal_surface.blit(img, rect.topleft)

            if option in self.checkbox_rects:
                checked = self.is_muted if option == "volume" else self.is_fullscreen
                checkbox_rect = self.checkbox_rects[option]
                pygame.draw.rect(self.internal_surface, (200, 200, 200), checkbox_rect)
                pygame.draw.rect(self.internal_surface, (0, 0, 0), checkbox_rect, 2)
                if checked:
                    check = self.font.render("✓", True, (0, 0, 0))
                    check_rect = check.get_rect(center=checkbox_rect.center)
                    self.internal_surface.blit(check, check_rect)

        self.last_hover_index = hover_index

        # Scale to screen with aspect ratio preserved
        screen_w, screen_h = self.screen.get_size()
        internal_w, internal_h = self.internal_resolution
        scale = min(screen_w / internal_w, screen_h / internal_h)
        scaled_w, scaled_h = int(internal_w * scale), int(internal_h * scale)

        scaled_surface = pygame.transform.smoothscale(self.internal_surface, (scaled_w, scaled_h))
        x_offset = (screen_w - scaled_w) // 2
        y_offset = (screen_h - scaled_h) // 2

        self.screen.fill((0, 0, 0))  # black bars
        self.screen.blit(scaled_surface, (x_offset, y_offset))
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                internal_pos = self.get_internal_mouse_pos(event.pos)

                for key, rect in self.checkbox_rects.items():
                    if rect.collidepoint(internal_pos):
                        if key == "volume":
                            self.toggle_volume()
                        elif key == "fullscreen":
                            self.toggle_fullscreen()
                        return None

                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(internal_pos):
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
