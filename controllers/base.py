"""
Base definition for controllers.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""

import logging
import random

from itertools import product

import common

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
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

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
        self.log.info(__name__ + ': ' + 'def ' + self.reset.__name__ + '(): ' + self.reset.__doc__)

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
        self.log.info(__name__ + ': ' + 'def ' + self.init.__name__ + '(): ' + self.init.__doc__)

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
        self.log.info(__name__ + ': ' + 'def ' + self.init_coordinates.__name__ + '(): ' + self.init_coordinates.__doc__)

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
        self.log.info(__name__ + ': ' + 'def ' + self.fix_coordinate_ships.__name__ + '(): ' + self.fix_coordinate_ships.__doc__)

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
        self.log.info(__name__ + ': ' + 'def ' + self.get_empty_arround_cell.__name__ + '(): ' + self.get_empty_arround_cell.__doc__)

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
        self.log.info(__name__ + ': ' + 'def ' + self.select_fleet.__name__ + '(): ' + self.select_fleet.__doc__)

        for fleet in self.fleets:
            if num == fleet.num:
                return fleet
        return None

    def move_obj(self, controller, obj, _x, _y):
        """Move object on input coordinate."""
        self.log.info(__name__ + ': ' + 'def ' + self.move_obj.__name__ + '(): ' + self.move_obj.__doc__)

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
            diff_x = common.diff2list(diff_x)
            diff_y = common.diff2list(diff_y)
            if len(diff_x) < 2:
                for _ in range(len(diff_x), 2):
                    diff_x.append(0)
            if len(diff_y) < 2:
                for _ in range(len(diff_y), 2):
                    diff_y.append(0)
            for index in range(2):
                obj.x += diff_x[index]
                obj.y += diff_y[index]
                self.speech.speak(self.board.get_cell(obj.x, obj.y).pos)
                if self._ai.check_battle(id(controller), obj):
                    self._ai.battle(id(controller), obj)
                    break
            result = True
        return result

    def move_fleet(self, controller, fleet, _x, _y):
        """Move fleet on board."""
        self.log.info(__name__ + ': ' + 'def ' + self.move_fleet.__name__ + '(): ' + self.move_fleet.__doc__)

        result = True
        for ship in fleet.ships:
            result = self.move_obj(controller, ship, _x, _y)
            if not result:
                break
        return result

    def mover(self, controller, obj, _x, _y):
        """Move object or fleet on board."""
        self.log.info(__name__ + ': ' + 'def ' + self.mover.__name__ + '(): ' + self.mover.__doc__)

        result = False
        if (obj.__class__.__name__ == 'Mine') or (obj.__class__.__name__ == 'Torpedo') or (obj.fleet == 0):
            result = self.move_obj(controller, obj, _x, _y)
        else:
            fleet = self.select_fleet(obj.fleet)
            if fleet is None:
                obj.fleet = 0
                result = self.move_obj(controller, obj, _x, _y)
            else:
                result = self.move_fleet(controller, fleet, _x, _y)
        return result

    def if_exists_forts(self):
        """Return status exists forts."""
        return bool(self.forts)

    def get_ship(self, _x, _y):
        """Return ship on incoming coordinate."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_ship.__name__ + '(): ' + self.get_ship.__doc__)

        for ship in self.ships:
            if (_x == ship.x) and (_y == ship.y):
                return ship
        return None

    def get_obj(self, _x, _y):
        """Return object on incoming coordinate."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_obj.__name__ + '(): ' + self.get_obj.__doc__)

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
