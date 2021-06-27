from utils import GameObject

class Grass(GameObject):
    def __init__(self, picture='ground.png', cell_size=100, **kwargs):
        super().__init__(picture, **kwargs)
        self.size = (cell_size, cell_size)