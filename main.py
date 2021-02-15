from kivy.app import App
from kivy.uix.widget import Widget


class CorporationGame(Widget):
    pass


class CorporationApp(App):
    def build(self):
        return CorporationGame()


if __name__ == '__main__':
    CorporationApp().run()