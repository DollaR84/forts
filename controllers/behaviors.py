"""
Behaviors module for enemy ai.

Created on 06.02.2019

@author: Ruslan Dolovanyuk

"""

import random

from collections import namedtuple

from itertools import product


class Unit:
    """Aditional unit class."""

    def __init__(self, enemy, obj):
        """Initialize unit class."""
        self.enemy = enemy
        self.obj = obj


class Behavior:
    """Behaviors class for ai player."""

    def __init__(self, cols, rows):
        """Initialize behavior class."""
        Coordinate = namedtuple('Coordinate', ['x', 'y'])
        self.coordinates = [Coordinate(xy[0], xy[1]) for xy in list(product(range(cols), range(rows)))]

        self.player = None
        self.gamer = None

        random.seed()

    def set_controllers(self, ai_):
        """Set controllers player and ai."""
        self.player = ai_.player
        self.gamer = ai_.gamer

    def scan(self):
        """Scan battle field and generate field for behaviors algoritms."""
        for coordinate in self.coordinates:
            player_obj = self.player.get_obj(coordinate.x, coordinate.y)
            gamer_obj = self.gamer.get_obj(coordinate.x, coordinate.y)
            if player_obj is not None:
                self.field[coordinate.x][coordinate.y] = Unit(True, player_obj)
            elif gamer_obj is not None:
                self.field[coordinate.x][coordinate.y] = Unit(False, gamer_obj)
            else:
                self.field[coordinate.x][coordinate.y] = None
