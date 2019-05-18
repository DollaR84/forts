"""
Behaviors module for enemy ai.

Created on 06.02.2019

@author: Ruslan Dolovanyuk

"""

import logging

from itertools import product

import common

from controllers.actions import Analysis


class Unit:
    """Aditional unit class."""

    def __init__(self, enemy, obj):
        """Initialize unit class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.enemy = enemy
        self.obj = obj
        self.fort = bool(obj.__class__.__name__ == 'Fort')


class Behavior:
    """Behaviors class for ai player."""

    def __init__(self, cols, rows):
        """Initialize behavior class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.cols = cols
        self.rows = rows

        self.coordinates = [common.Coordinate(xy[0], xy[1]) for xy in list(product(range(self.cols), range(self.rows)))]

        self.player = None
        self.gamer = None
        self.analysis = None

    def set_controllers(self, ai_):
        """Set controllers player and ai."""
        self.log.info(__name__ + ': ' + 'def ' + self.set_controllers.__name__ + '(): ' + self.set_controllers.__doc__)

        self.player = ai_.player
        self.gamer = ai_.gamer

        self.analysis = Analysis(self.player, self.gamer)

    def scan(self):
        """Scan battle field and return generated field for behaviors algoritms."""
        self.log.info(__name__ + ': ' + 'def ' + self.scan.__name__ + '(): ' + self.scan.__doc__)

        field = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for coordinate in self.coordinates:
            player_obj = self.player.get_obj(coordinate.x, coordinate.y)
            gamer_obj = self.gamer.get_obj(coordinate.x, coordinate.y)
            if player_obj is not None:
                field[coordinate.y][coordinate.x] = Unit(False, player_obj)
            elif gamer_obj is not None:
                field[coordinate.y][coordinate.x] = Unit(True, gamer_obj)
        return field

    def generate_objects(self, field, enemy):
        """Generate 2 list: forts and other objects player or ai."""
        self.log.info(__name__ + ': ' + 'def ' + self.generate_objects.__name__ + '(): ' + self.generate_objects.__doc__)

        forts = []
        objects = []
        for row in field:
            for unit in row:
                if unit is not None and unit.enemy == enemy:
                    if unit.fort:
                        forts.append(unit.obj)
                    else:
                        objects.append(unit.obj)
        return objects, forts

    def step(self):
        """Main algorithm for ai action."""
        self.log.info(__name__ + ': ' + 'def ' + self.step.__name__ + '(): ' + self.step.__doc__)

        self.analysis.field = self.scan()
        self.analysis.p_objects, self.analysis.p_forts = self.generate_objects(self.analysis.field, False)
        self.analysis.g_objects, self.analysis.g_forts = self.generate_objects(self.analysis.field, True)
        action = self.analysis.run()
        self.run_best_action(action)

    def run_best_action(self, action):
        """Run best action for ai."""
        self.log.info(__name__ + ': ' + 'def ' + self.run_best_action.__name__ + '(): ' + self.run_best_action.__doc__)

        self.player.obj = action.object
        _x = action.coordinates[0].x
        _y = action.coordinates[0].y
        if action.coordinates[1] is not None:
            _x += action.coordinates[1].x
            _y += action.coordinates[1].y
        self.player.mover(_x, _y)
