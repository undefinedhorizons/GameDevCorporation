from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image

class GameObject(Button):
    def __init__(self, picture='air.png', cell_size=100, position=(-1, -1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = picture
        self.background_down = self.background_normal