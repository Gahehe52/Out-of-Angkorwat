import pygame

class Prolog:
    def __init__(self, screen, dialogue_list, background_name, on_complete=None):
        self.display_surface = screen
        self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT = 800, 600
        self.internal_surface = pygame.Surface((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))

        self.dialogue = dialogue_list
        self.background = pygame.image.load(f"assets/backgrounds/{background_name}").convert()
        self.background = pygame.transform.scale(self.background, (self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))
        self.font = pygame.font.SysFont("arial", 24)
        self.text_color = (255, 255, 255)
        self.box_color = (0, 0, 0, 180)
        self.index = 0
        self.on_complete = on_complete or (lambda: None)
        self.clock = pygame.time.Clock()

    def draw_text_box(self, text):
        box_rect = pygame.Rect(50, 450, 700, 120)
        text_surface = self.font.render(text, True, self.text_color)

        # Background for text
        box_surf = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        box_surf.fill(self.box_color)

        self.internal_surface.blit(box_surf, box_rect.topleft)
        self.internal_surface.blit(text_surface, (box_rect.left + 20, box_rect.top + 40))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.index += 1
                    if self.index >= len(self.dialogue):
                        running = False
                        self.on_complete()

            self.internal_surface.blit(self.background, (0, 0))
            if self.index < len(self.dialogue):
                self.draw_text_box(self.dialogue[self.index])

            # Scale internal surface to fit screen while keeping aspect ratio
            win_w, win_h = self.display_surface.get_size()
            scale = min(win_w / self.INTERNAL_WIDTH, win_h / self.INTERNAL_HEIGHT)
            scaled_w = int(self.INTERNAL_WIDTH * scale)
            scaled_h = int(self.INTERNAL_HEIGHT * scale)
            x_offset = (win_w - scaled_w) // 2
            y_offset = (win_h - scaled_h) // 2

            scaled_surface = pygame.transform.scale(self.internal_surface, (scaled_w, scaled_h))
            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(scaled_surface, (x_offset, y_offset))
            pygame.display.flip()
