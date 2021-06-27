from utils import GameObject
from room import Room


class Toilet(GameObject, Room):
    def __init__(self, cell_size=100, position=(0, 0), picture='./toilet.png', **kwargs):
        self.price = 500
        self.pertime = 30
        self.capacity = 2
        self.reliability = 1000
        self.max_reliability = 1000
        self.breakdown = 10
        self.income = 0

        super().__init__(picture, **kwargs)

        self.position = position
        self.size = (2 * cell_size, cell_size)

    def update(self):
        pass

    def repair(self):
        self.reliability = (self.reliability + self.breakdown * 4) % 1000