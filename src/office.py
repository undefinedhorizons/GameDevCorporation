from utils import GameObject, get_game
from Room import Room


class Office(GameObject, Room):
    def __init__(self, cell_size=100, position=(0, 0), picture='../res/office.png', **kwargs):
        self.price = 1000
        self.pertime = 50
        self.capacity = 4
        self.reliability = 1000
        self.breakdown = 15
        self.income = 100

        super().__init__(picture, **kwargs)

        self.position = position
        self.size = (6 * cell_size, cell_size)

    def on_press(self):
        get_game().place(pos=self.position)

    def update(self):
        self.reliability -= self.breakdown

    def repair(self):
        self.reliability = (self.reliability + self.breakdown * 4) % 1000