class Player:
    def __init__(self):
        self.score = 0
        self.lives = 3

    def __str__(self):
        return f'You have earned {self.score} point(s)!'

    def getScore(self):
        return self.score

    def getLives(self):
        return self.lives

    def increaseScore(self):
        self.score = self.score + 1

    def decreaseLife(self):
        self.lives = self.lives - 1
