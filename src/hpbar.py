import pygame

class HPBar:
    def __init__(self, x, y, width=200, height=20, max_hp=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.border_radius = 10
        self.font = pygame.font.SysFont(None, 24)

    def reduce(self, amount):
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def get_color(self):
        ratio = self.current_hp / self.max_hp
        if ratio > 0.6: return (0, 200, 0)      # Hijau
        elif ratio > 0.3: return (255, 215, 0)  # Kuning
        else: return (200, 0, 0)               # Merah

    def draw(self, surface):
        fill_width = (self.current_hp / self.max_hp) * self.width
        pygame.draw.rect(surface, (0, 0, 0), (self.x-2, self.y-2, self.width+4, self.height+4), border_radius=self.border_radius+2)
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), border_radius=self.border_radius)
        pygame.draw.rect(surface, self.get_color(), (self.x, self.y, fill_width, self.height), border_radius=self.border_radius)

        text = self.font.render(f"HP: {int(self.current_hp)} / {self.max_hp}", True, (255, 255, 255))
        surface.blit(text, (self.x, self.y + self.height + 5))