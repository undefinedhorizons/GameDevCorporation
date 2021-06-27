from game import CorporationGame
from src.gui import RoomButton, WorkerButton
from utils import get_game, ButtonClick
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App


class CorporationApp(App):
    game = None

    def build(self):
        self.play_backgroud_sound()
        self.game = CorporationGame()
        self.game.prepare()
        self.load_gui()
        Clock.schedule_interval(self.game.tick, 1.0 / 60.0)
        return self.game

    def load_gui(self):
        build_office = RoomButton()
        build_worker = WorkerButton()
        money_display = Button(text=str(get_game().money), size_hint=(.2, .2), pos_hint={'x': .79, 'y': .79})

        get_game().money_display = money_display
        gui = get_game().gui
        gui.add_widget(build_office)
        gui.add_widget(build_worker)
        gui.add_widget(money_display)


    def play_backgroud_sound(self):
        pass
        # background_sound = SoundLoader.load('../res/sound/background_sound.wav')
        # if background_sound:
        #     background_sound.play()
        #     background_sound.loop = True