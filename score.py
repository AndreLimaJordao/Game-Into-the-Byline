class Score:
    def __init__(self, highscore):
        self.highscore = highscore
        self.num_flashs_trigger = 0
        self.num_monster_trigger = 0
        self.num_items_trigger = 0

    def set_highscore(self, value):
        self.highscore -= value
        if value == 50:
            self.num_monster_trigger += 1
        elif value == 100:
            self.num_flashs_trigger += 1
        elif value == 200:
            self.num_items_trigger += 1

    def get_highscore(self):
        return self.highscore

    def reset_highscore(self):
        self.highscore = 0

    def get_num_flashs_trigger(self):
        return self.num_flashs_trigger

    def get_num_monster_trigger(self):
        return self.num_monster_trigger

    def get_num_items_trigger(self):
        return self.num_items_trigger
