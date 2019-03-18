"""
Base definition for controllers.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""

import math
import random

from itertools import product

from objects.other import Fort
from objects.other import Mine
from objects.other import Torpedo
from objects.ships import Battleship
from objects.ships import Cruiser
from objects.ships import Destroyer
from objects.ships import GuardBoat
from objects.ships import Submarine
from objects.ships import TorpedoBoat
from objects.ships import Trawler


class Base:
    """Base class for controllers."""

    def __init__(self, board, speech, phrases, ai):
        """Initialize base controller."""
        self.board = board
        self.speech = speech
        self.phrases = phrases
        self._ai = ai

        self._x = 0
        self._y = 0
        self.cell = self.board.get_cell(self._x, self._y)

        self.fleets = []
        self.ships = []
        self.mines = []
        self.torpedos = []
        self.forts = []

        random.seed()

    def reset(self):
        """Reset local variable."""
        self._x = 0
        self._y = 0
        self.cell = self.board.get_cell(self._x, self._y)
        self.fleets.clear()
        self.ships.clear()
        self.mines.clear()
        self.torpedos.clear()
        self.forts.clear()

    def init(self):
        """Initialize total for all controllers."""
        self.reset()
        for _ in range(2):
            self.forts.append(Fort(self.phrases['fort'], self.board.textures['fort'], self.phrases['fort_symbol']))
            self.ships.append(Battleship(self.phrases['battleship'], self.board.textures['chip'], self.phrases['battleship_symbol']))
            self.ships.append(Submarine(self.phrases['submarine'], self.board.textures['chip'], self.phrases['submarine_symbol']))
        for _ in range(4):
            self.mines.append(Mine(self.phrases['mine'], self.board.textures['chip'], self.phrases['mine_symbol']))
        for _ in range(5):
            self.ships.append(Cruiser(self.phrases['cruiser'], self.board.textures['chip'], self.phrases['cruiser_symbol']))
        for _ in range(6):
            self.torpedos.append(Torpedo(self.phrases['torpedo'], self.board.textures['chip'], self.phrases['torpedo_symbol']))
            self.ships.append(Destroyer(self.phrases['destroyer'], self.board.textures['chip'], self.phrases['destroyer_symbol']))
            self.ships.append(GuardBoat(self.phrases['guardboat'], self.board.textures['chip'], self.phrases['guardboat_symbol']))
            self.ships.append(TorpedoBoat(self.phrases['torpedoboat'], self.board.textures['chip'], self.phrases['torpedoboat_symbol']))
            self.ships.append(Trawler(self.phrases['trawler'], self.board.textures['chip'], self.phrases['trawler_symbol']))

    def init_coordinates(self, zone_cells):
        """Initialize coordinate in objects."""
        for ship in self.ships:
            cell = random.choice(zone_cells)
            ship.x = cell[0]
            ship.y = cell[1]
            zone_cells.remove(cell)
        for mine in self.mines:
            cell = random.choice(zone_cells)
            mine.x = cell[0]
            mine.y = cell[1]
            zone_cells.remove(cell)
        for torpedo in self.torpedos:
            cell = random.choice(zone_cells)
            torpedo.x = cell[0]
            torpedo.y = cell[1]
            zone_cells.remove(cell)

    def fix_coordinate_ships(self):
        """Fix coordinate ships in fleets."""
        for fleet in self.fleets:
            main = fleet.ships[0]
            for index in range(1, len(fleet.ships)):
                arround = self.get_empty_arround_cell(main.x, main.y)
                if arround:
                    fleet.ships[index].x = arround[0][0]
                    fleet.ships[index].y = arround[0][1]

    def draw(self):
        """Total draw all objects."""
        for fort in self.forts:
            fort.draw(self.board)
        for torpedo in self.torpedos:
            torpedo.draw(self.board)
        for mine in self.mines:
            mine.draw(self.board)
        for ship in self.ships:
            ship.draw(self.board)

    def get_empty_arround_cell(self, _x, _y):
        """Return list coordinate empty cells arround incoming cell."""
        result = list(product(range(_x - 1, _x + 2), range(_y - 1, _y + 2)))
        for cell in result:
            if (cell[0] == 0) or (cell[0] == self.board.cols - 1) or (cell[0] == self.board.cols // 2):
                result.remove(cell)
                continue
            if (_x != cell[0]) and (_y != cell[1]):
                result.remove(cell)
                continue
            for ship in self.ships:
                if (cell[0] == ship.x) and (cell[1] == ship.y):
                    result.remove(cell)
                    break
        return result

    def select_fleet(self, num):
        """Select fleet of number."""
        for fleet in self.fleets:
            if num == fleet.num:
                return fleet
        return None

    def move_obj(self, obj, _x, _y):
        """Move object on input coordinate."""
        diff_x = _x - obj.x
        diff_y = _y - obj.y
        result = False
        if obj.__class__.__name__ == 'Fort':
            result = False
        elif (obj.__class__.__name__ == 'TorpedoBoat') and ((abs(diff_x) > 2) or (abs(diff_y) > 2)):
            result = False
        elif (abs(diff_x) > 1) or (abs(diff_y) > 1):
            result = False
        else:
            diff_x = diff2list(diff_x)
            diff_y = diff2list(diff_y)
            for index in range(2):
                obj._x += diff_x[index]
                obj._y += diff_y[index]
                if self._ai.check_battle(id(self), obj):
                    self._ai.battle(id(self), obj)
                    break
            result = True
        return result

    def move_fleet(self, fleet, _x, _y):
        """Move fleet on board."""
        result = True
        for ship in fleet.ships:
            result = self.move_obj(ship, _x, _y)
            if not result:
                break
        return result

    def mover(self, obj, _x, _y):
        """Move object or fleet on board."""
        result = False
        if (obj.__class__.__name__ == 'Mine') or (obj.__class__.__name__ == 'Torpedo') or (obj.fleet == 0):
            result = self.move_obj(obj, _x, _y)
        else:
            result = self.move_fleet(self.select_fleet(obj.fleet), _x, _y)
        return result

    def if_exists_forts(self):
        """Return status exists forts."""
        return bool(self.forts)

    def get_ship(self, _x, _y):
        """Return ship on incoming coordinate."""
        for ship in self.ships:
            if (_x == ship.x) and (_y == ship.y):
                return ship
        return None

    def get_obj(self, _x, _y):
        """Return object on incoming coordinate."""
        for fort in self.forts:
            if (_x == fort.x) and (_y == fort.y):
                return fort
        for mine in self.mines:
            if (_x == mine.x) and (_y == mine.y):
                return mine
        for torpedo in self.torpedos:
            if (_x == torpedo.x) and (_y == torpedo.y):
                return torpedo
        return self.get_ship(_x, _y)


def diff2list(diff):
    """Convert different to list."""
    result = []
    for _ in range(abs(diff)):
        result.append(int(math.copysign(1.0, diff)))
    return result
