from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.scatterlayout import ScatterLayout


class CorporationGame(Widget):
    pass


class CorporationApp(App):
    def build(self):
        return Button(text='hello world')


if __name__ == '__main__':
    CorporationApp().run()
