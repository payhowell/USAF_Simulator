class GameState:
    def __init__(self):
        self.slot = 1
        self.chapter = 0
        self.player_name = ""
        self.backstory = ""
        self.stats = {}
        self.rank = "Airman"
        self.level = 1
        self.xp = 0
        self.inventory = []
        self.mental_state = 100  # hidden
        self.morality_score = 0  # visible
        self.flags = {}  # story triggers

    def reset(self):
        self.__init__()

# Global instance
game_state = GameState()
