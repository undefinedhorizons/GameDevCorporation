from kivy.core.audio import SoundLoader
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App


def get_game():
    return App.get_running_app().game


class GameObject(Button):
    def __init__(self, picture='air.png', cell_size=100, position=(-1, -1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = picture
        self.background_down = self.background_normal


class ButtonClick(Button):
    def on_press(self):
        sound = SoundLoader.load('button.wav')
        if sound:
            sound.play()
