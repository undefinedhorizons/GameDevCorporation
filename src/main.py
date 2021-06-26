from abc import ABC, abstractmethod, ABCMeta

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty
)
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from utils import GameObject, get_game
from src.room.office import Office
from src.person.worker import Worker
from cell import Cell
from grass import Grass
from gamefield import GameField
from game import CorporationGame
from app import CorporationApp


if __name__ == '__main__':
    CorporationApp().run()
