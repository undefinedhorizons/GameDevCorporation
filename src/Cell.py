from utils import GameObject, get_game


class Cell(GameObject):
    def __init__(self, position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.contains_office = False

    def on_press(self):
        print(self.position)
        get_game().place(self.position)
