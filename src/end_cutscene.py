import pygame

class EndCutscene:
    def __init__(self, surface, on_complete):
        self.surface = surface
        self.on_complete = on_complete
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load("assets/backgrounds/cutscene_background.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Load downward walking animation frames
        self.frames = []
        i = 0
        while True:
            try:
                img = pygame.image.load(f"assets/player/down/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (96, 96))
                self.frames.append(img)
                i += 1
            except FileNotFoundError:
                break

        if not self.frames:
            raise Exception("No player down animation frames found in assets/player/down")

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 0.1

        self.x = 400 - 48  # center horizontally
        self.y = -96       # start above the screen
        self.speed = 100   # pixels per second

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Move player down
            self.y += self.speed * dt
            if self.y > 600:  # completely off the bottom
                running = False
                self.on_complete()
                return

            # Animate
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

            # Draw
            self.surface.blit(self.background, (0, 0))
            self.surface.blit(self.frames[self.current_frame], (self.x, self.y))
            pygame.display.flip()
