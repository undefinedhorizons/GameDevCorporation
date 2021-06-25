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
from Grass import Grass
from GameField import GameField
from CorporationGame import CorporationGame
from switch_state import switch_state
from CorporationApp import CorporationApp


if __name__ == '__main__':
    CorporationApp().run()
