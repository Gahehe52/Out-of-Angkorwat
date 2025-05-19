import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.font = pygame.font.Font(font_path, 36) if font_path else pygame.font.SysFont("Arial", 36)
        self.options = ["start", "quit"]
        self.running = True

        self.bg_image = pygame.image.load("BrickBG.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        self.button_images = {
            "start": pygame.image.load("assets/Menu/start.png").convert_alpha(),
            "quit": pygame.image.load("assets/Menu/Quit.png").convert_alpha(),
        }

        self.button_size = (250, 80)
        for key in self.button_images:
            self.button_images[key] = pygame.transform.scale(self.button_images[key], self.button_size)

        self.option_rects = []
        self.last_hover_index = None  # Untuk mendeteksi perubahan hover

        # === Load hover sound ===
        self.hover_sound = pygame.mixer.Sound("bgm/sfx/ButtonClick.mp3")  # Ganti path jika perlu

    def create_option_rects(self):
        self.option_rects = []
        for i in range(len(self.options)):
            center_x = self.screen.get_width() // 2
            top_y = 250 + i * 120
            rect = pygame.Rect(0, 0, *self.button_size)
            rect.center = (center_x, top_y)
            self.option_rects.append(rect)

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hover_index = None

        for i, option in enumerate(self.options):
            key = option.lower()
            img = self.button_images[key].copy()

            if self.option_rects[i].collidepoint(mouse_pos):
                hover_index = i
                # Hanya mainkan suara jika hover berpindah
                if self.last_hover_index != i:
                    self.hover_sound.play()
                overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                overlay.fill((80, 80, 80, 80))
                img.blit(overlay, (0, 0))

            self.screen.blit(img, self.option_rects[i])

        self.last_hover_index = hover_index
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            return self.options[i]
        return None

    def run(self):
        self.create_option_rects()
        while self.running:
            action = self.handle_input()
            if action in self.options:
                return action
            self.draw()
