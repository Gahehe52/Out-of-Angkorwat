import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.font = pygame.font.Font(font_path, 36) if font_path else pygame.font.SysFont("Arial", 36)
        self.options = ["start", "quit"]  # Sesuaikan dengan nama file tombol
        self.selected = 0
        self.running = True

        self.bg_image = pygame.image.load("BrickBG.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        self.button_images = {
            "start": pygame.image.load("start.png").convert_alpha(),
            "quit": pygame.image.load("Quit.png").convert_alpha(),
        }

        self.button_size = (250, 80)
        for key in self.button_images:
            self.button_images[key] = pygame.transform.scale(self.button_images[key], self.button_size)

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        for i, option in enumerate(self.options):
            key = option.lower()
            img = self.button_images[key].copy()

            if i == self.selected:
                overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                overlay.fill((80, 80, 80, 80))
                img.blit(overlay, (0, 0))

            center_x = self.screen.get_width() // 2
            top_y = 250 + i * 120

            rect = img.get_rect(center=(center_x, top_y))
            self.screen.blit(img, rect)

        pygame.display.flip()  # ← Pindah ke sini


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
        return None

    def run(self):
        while self.running:
            action = self.handle_input()
            if action in self.options:
                return action
            self.draw()
