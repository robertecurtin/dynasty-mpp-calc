import utils

class Team:
    def __init__(self, owner):
        self.owner = owner
        [self.score, self.mpp] = utils.getStats(owner)
        self.salt = -1
        self.result = 2

    def win(self):
        self.result = .75

    def lose(self):
        self.result = 1.5

    def cry(self):
        self.salt = (self.mpp - self.score) * self.result
