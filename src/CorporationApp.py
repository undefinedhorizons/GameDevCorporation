from CorporationGame import CorporationGame
from utils import get_game
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
from switch_state import switch_state

class CorporationApp(App):
    game = None

    def build(self):
        self.game = CorporationGame()
        self.game.prepare()
        self.load_gui()
        Clock.schedule_interval(self.game.tick, 1.0 / 60.0)
        return self.game

    def load_gui(self):
        build_office = Button(text='office', size_hint=(.2, .2), pos_hint={'x': .01, 'y': .79})
        build_worker = Button(text='worker', size_hint=(.2, .2), pos_hint={'x': .22, 'y': .79})
        money_display = Button(text=str(get_game().money), size_hint=(.2, .2), pos_hint={'x': .79, 'y': .79})

        get_game().money_display = money_display

        build_worker.bind(on_press=switch_state)
        build_office.bind(on_press=switch_state)

        gui = get_game().gui
        gui.add_widget(build_office)
        gui.add_widget(build_worker)
        gui.add_widget(money_display)