from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.scatterlayout import ScatterLayout


class CorporationGame(ScatterLayout):
    pass


class CorporationApp(App):
    def build(self):
        print(1)
        return CorporationGame(do_rotation=False)


if __name__ == '__main__':
    CorporationApp().run()
