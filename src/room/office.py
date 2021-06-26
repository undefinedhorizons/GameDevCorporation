from src.utils import GameObject, get_game
from src.room.room import Room


class Office(GameObject, Room):
    def __init__(self, cell_size=100, position=(0, 0), picture='../res/office.png', **kwargs):
        self.price = 1000
        self.pertime = 50
        self.capacity = 4
        self.reliability = 1000
        self.max_reliability = 1000
        self.breakdown = 15
        self.income = 100

        super().__init__(picture, **kwargs)

        self.position = position
        self.size = (6 * cell_size, cell_size)

    def on_press(self):
        get_game().place(pos=self.position, office=self)

    def update(self):
        if not self.is_broken():
            self.reliability -= self.breakdown

    def is_broken(self):
        return self.reliability < 0

    def repair(self, amount):
        if self.reliability < self.max_reliability:
            self.reliability += amount
