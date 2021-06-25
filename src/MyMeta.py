from abc import ABC, abstractmethod, ABCMeta
from utils import GameObject


class MyMeta(ABCMeta, type(GameObject)):
    pass