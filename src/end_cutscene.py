from game_cutscene import GameCutscene

class EndCutscene(GameCutscene):
    def start_y(self):
        return -96  # Start above screen

    def update_position(self, dt):
        self.y += self.speed * dt

    def exit_condition(self):
        return self.y > self.INTERNAL_HEIGHT  # Fully below screen

    def frames_path(self):
        return "assets/player/down"
