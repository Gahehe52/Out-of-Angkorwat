import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.font = pygame.font.Font(font_path, 36) if font_path else pygame.font.SysFont("Arial", 36)
        self.options = ["Start Game", "Quit"]
        self.selected = 0
        self.running = True


    def draw(self):
        self.screen.fill((10, 10, 10))
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 300 + i * 50))
            self.screen.blit(text, rect)
        pygame.display.flip()


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
                    return self.options[self.selected].lower().replace(" ", "_")
        return None


    def run(self):
        while self.running:
            action = self.handle_input()
            if action == "start_game":
                return "start"
            elif action == "quit":
                return "quit"
            self.draw()

