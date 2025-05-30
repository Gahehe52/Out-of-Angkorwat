import pygame
from abc import ABC, abstractmethod

class GameCutscene(ABC):
    def __init__(self, surface, on_complete):
        self.display_surface = surface
        self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT = 800, 600
        self.internal_surface = pygame.Surface((self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))
        self.on_complete = on_complete
        self.clock = pygame.time.Clock()

        # Load background
        self.background = pygame.image.load("assets/backgrounds/cutscene_background.png").convert()
        self.background = pygame.transform.scale(self.background, (self.INTERNAL_WIDTH, self.INTERNAL_HEIGHT))

        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 0.1

        self.x = self.INTERNAL_WIDTH // 2 - 48
        self.y = self.start_y()
        self.speed = 100

        self.load_frames()

    @abstractmethod
    def start_y(self):
        """Return the starting Y position of the character."""
        pass

    @abstractmethod
    def update_position(self, dt):
        """Update the Y position per frame."""
        pass

    @abstractmethod
    def exit_condition(self):
        """Return True if cutscene should end."""
        pass

    @abstractmethod
    def frames_path(self):
        """Return the asset path to load the frames from."""
        pass

    def load_frames(self):
        path = self.frames_path()
        i = 0
        while True:
            try:
                img = pygame.image.load(f"{path}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (96, 96))
                self.frames.append(img)
                i += 1
            except FileNotFoundError:
                break
        if not self.frames:
            raise Exception(f"No frames found in {path}")

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.update_position(dt)
            if self.exit_condition():
                running = False
                self.on_complete()
                return

            # Animate
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

            # Draw
            self.internal_surface.blit(self.background, (0, 0))
            self.internal_surface.blit(self.frames[self.current_frame], (self.x, self.y))

            # Scale for display
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
