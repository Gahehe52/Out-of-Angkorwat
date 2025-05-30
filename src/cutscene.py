import pygame

class Cutscene:
    def __init__(self, surface, on_complete):
        self.display_surface = surface
        self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT = 800, 600
        self.internal_surface = pygame.Surface((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))
        self.on_complete = on_complete
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load("assets/backgrounds/cutscene_background.png").convert()
        self.background = pygame.transform.scale(self.background, (self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))

        # Load upward walking animation frames
        self.frames = []
        i = 0
        while True:
            try:
                img = pygame.image.load(f"assets/player/up/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (96, 96))
                self.frames.append(img)
                i += 1
            except:
                break  # Stop when no more frames

        if not self.frames:
            raise Exception("No player up animation frames found in assets/player/up")

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 0.1

        self.x = self.INTERNAL_WIDTH // 2 - 48  # center
        self.y = self.INTERNAL_HEIGHT  # start just below the screen
        self.speed = 100  # pixels per second

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Move player up
            self.y -= self.speed * dt
            if self.y + 96 < 0:  # completely off-screen
                running = False
                self.on_complete()
                return

            # Animate
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

            # Draw to internal surface
            self.internal_surface.blit(self.background, (0, 0))
            self.internal_surface.blit(self.frames[self.current_frame], (self.x, self.y))

            # Scale internal surface to display size
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
