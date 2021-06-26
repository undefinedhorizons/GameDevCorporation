from abc import ABC, abstractmethod, ABCMeta

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty
)
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from utils import GameObject, get_game
from office import Office
from person import Worker
from Cell import Cell
from grass import Grass
from gamefield import GameField
from game import CorporationGame
from switch_state import switch_state
from app import CorporationApp


if __name__ == '__main__':
    CorporationApp().run()
