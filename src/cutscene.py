from game_cutscene import GameCutscene

class Cutscene(GameCutscene):
    def start_y(self):
        return self.INTERNAL_HEIGHT  # Start below screen

    def update_position(self, dt):
        self.y -= self.speed * dt

    def exit_condition(self):
        return self.y + 96 < 0  # Fully above screen

    def frames_path(self):
        return "assets/player/up"
