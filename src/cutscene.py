import pygame

class Cutscene:
    def __init__(self, surface, on_complete):
        self.surface = surface
        self.on_complete = on_complete
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load("assets/backgrounds/cutscene_background.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Load upward walking animation frames
        self.frames = []
        for i in range(len(pygame.image.get_extended().__class__.__name__)):  # safe dummy count
            try:
                img = pygame.image.load(f"assets/player/up/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (96, 96))
                self.frames.append(img)
            except:
                break  # Stop when no more frames

        if not self.frames:
            raise Exception("No player up animation frames found in assets/player/up")

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 0.1

        self.x = 400 - 48  # center
        self.y = 600  # start below screen
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

            # Draw
            self.surface.blit(self.background, (0, 0))
            self.surface.blit(self.frames[self.current_frame], (self.x, self.y))
            pygame.display.flip()
