import pygame
import os

class Prolog:
    def __init__(self, screen, dialogue_list, background_name, on_complete=None):
        self.display_surface = screen
        self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT = 800, 600
        self.internal_surface = pygame.Surface((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))

        self.dialogue = dialogue_list if dialogue_list else ["[Dialogue missing]"]

        # Load background safely
        try:
            background_path = f"assets/backgrounds/{background_name}"
            if not os.path.exists(background_path):
                raise FileNotFoundError(f"Background not found: {background_path}")
            self.background = pygame.image.load(background_path).convert()
            self.background = pygame.transform.scale(self.background, (self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))
        except Exception as e:
            print(f"[Error] Failed to load background: {e}")
            self.background = pygame.Surface((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))
            self.background.fill((0, 0, 0))  # Fallback to black background

        # Load font safely
        try:
            self.font = pygame.font.SysFont("arial", 24)
        except Exception as e:
            print(f"[Error] Failed to load font: {e}")
            self.font = pygame.font.Font(None, 24)

        self.text_color = (255, 255, 255)
        self.box_color = (0, 0, 0, 180)
        self.index = 0
        self.on_complete = on_complete or (lambda: None)
        self.clock = pygame.time.Clock()

    def draw_text_box(self, text):
        try:
            box_rect = pygame.Rect(50, 450, 700, 120)
            
            # Create background box with transparency
            box_surf = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
            box_surf.fill(self.box_color)
            self.internal_surface.blit(box_surf, box_rect.topleft)

            # Render main dialogue text
            text_surface = self.font.render(text, True, self.text_color)
            self.internal_surface.blit(text_surface, (box_rect.left + 20, box_rect.top + 20))

            # Render "Press 'Space' to continue" in smaller font
            prompt_font = pygame.font.SysFont("arial", 18)
            prompt_text = prompt_font.render("Press 'Space' to continue", True, self.text_color)
            prompt_rect = prompt_text.get_rect(bottomright=(box_rect.right - 20, box_rect.bottom - 10))
            self.internal_surface.blit(prompt_text, prompt_rect)
        except Exception as e:
            print(f"[Error] Failed to draw text box: {e}")

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
                        try:
                            self.on_complete()
                        except Exception as e:
                            print(f"[Error] on_complete callback failed: {e}")

            try:
                self.internal_surface.blit(self.background, (0, 0))
                if self.index < len(self.dialogue):
                    self.draw_text_box(self.dialogue[self.index])
                else:
                    self.draw_text_box("[End of dialogue]")

                # Safely scale surface
                try:
                    win_w, win_h = self.display_surface.get_size()
                    scale = min(win_w / self.INTERNAL_WIDTH, win_h / self.INTERNAL_HEIGHT)
                    scaled_w = int(self.INTERNAL_WIDTH * scale)
                    scaled_h = int(self.INTERNAL_HEIGHT * scale)
                    x_offset = (win_w - scaled_w) // 2
                    y_offset = (win_h - scaled_h) // 2
                except Exception as e:
                    print(f"[Error] Failed to get display size or scale surface: {e}")
                    scaled_w, scaled_h = self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT
                    x_offset = y_offset = 0

                scaled_surface = pygame.transform.scale(self.internal_surface, (scaled_w, scaled_h))
                self.display_surface.fill((0, 0, 0))
                self.display_surface.blit(scaled_surface, (x_offset, y_offset))
                pygame.display.flip()
            except Exception as e:
                print(f"[Error] Failed during rendering: {e}")
