"""
Behaviors module for enemy ai.

Created on 06.02.2019

@author: Ruslan Dolovanyuk

"""

from collections import namedtuple

from itertools import product

from controllers.actions import Analysis


class Unit:
    """Aditional unit class."""

    def __init__(self, enemy, obj):
        """Initialize unit class."""
        self.enemy = enemy
        self.obj = obj
        self.fort = bool(obj.__class__.__name__ == 'Fort')


class Behavior:
    """Behaviors class for ai player."""

    def __init__(self, cols, rows):
        """Initialize behavior class."""
        self.cols = cols
        self.rows = rows

        Coordinate = namedtuple('Coordinate', ['x', 'y'])
        self.coordinates = [Coordinate(xy[0], xy[1]) for xy in list(product(range(self.cols), range(self.rows)))]

        self.player = None
        self.gamer = None

        self.analysis = Analysis()

    def set_controllers(self, ai_):
        """Set controllers player and ai."""
        self.player = ai_.player
        self.gamer = ai_.gamer

    def scan(self):
        """Scan battle field and return generated field for behaviors algoritms."""
        field = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for coordinate in self.coordinates:
            player_obj = self.player.get_obj(coordinate.x, coordinate.y)
            gamer_obj = self.gamer.get_obj(coordinate.x, coordinate.y)
            if player_obj is not None:
                field[coordinate.x][coordinate.y] = Unit(True, player_obj)
            elif gamer_obj is not None:
                field[coordinate.x][coordinate.y] = Unit(False, gamer_obj)
        return field

    def generate_objects(self, field, enemy):
        """Generate 2 list: forts and other objects player or ai."""
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
        self.analysis.field = self.scan()
        self.analysis.p_objects, self.analysis.p_forts = self.generate_objects(self.analysis.field, False)
        self.analysis.g_objects, self.analysis.g_forts = self.generate_objects(self.analysis.field, True)
        self.analysis.run()
