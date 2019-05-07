"""
Player module controller.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""

import enum
import logging

from itertools import product

import pygame

from constants import Colors

from controllers.base import Base

from objects.fleets import Fleet


DIR = enum.Enum('Dir', 'left right down up')


class Player(Base):
    """Player class controller."""

    def __init__(self, board, speech, phrases, ai):
        """Initialize player controller."""
        super().__init__(board, speech, phrases, ai)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)
        self.log.info(__name__ + ': ' + 'id controller: ' + str(id(self)))

        self.color = Colors.BLACK
        self.fleet = None
        self.obj = None
        self.light = False
        self.light_cells = []

    def init(self):
        """Initialize ships and other objects for player."""
        super().init()
        self.log.info(__name__ + ': ' + 'def ' + self.init.__name__ + '(): ' + self.init.__doc__)

        for index, fort in enumerate(self.forts):
            fort.x = 0
            fort.y = 3 + index * 5
            fort.show = True
        zone_cells = list(product(range(1, self.board.cols // 2), range(self.board.rows)))
        self.init_coordinates(zone_cells)
        for ship in self.ships:
            ship.show = True
        for mine in self.mines:
            mine.show = True
        for torpedo in self.torpedos:
            torpedo.show = True

    def reset(self):
        """Reset player variable."""
        super().reset()
        self.log.info(__name__ + ': ' + 'def ' + self.reset.__name__ + '(): ' + self.reset.__doc__)

        self.light_cells.clear()

    def draw(self):
        """Draw method player."""
        super().draw()
        if not self._ai.ai_step and self.cell is not None:
            pygame.draw.rect(self.board.board, self.color, (self.cell.left, self.cell.top, self.cell.size, self.cell.size), 2)
        if self.light:
            for cell in self.light_cells:
                pygame.draw.rect(self.board.board, Colors.CHARTREUSE, (cell.left, cell.top, cell.size, cell.size), 2)

    def create_fleets(self):
        """Create fleets player."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_fleets.__name__ + '(): ' + self.create_fleets.__doc__)

        self._ai.set_text(self.phrases['fleet_create_your'])
        self.speech.speak(self.phrases['fleet_create_your'])
        self._ai.create_fleets = True

    def mover(self, _x, _y):  # pylint: disable=W0221
        """Move object on board."""
        result = super().mover(self, self.obj, _x, _y)
        self.log.info(__name__ + ': ' + 'def ' + self.mover.__name__ + '(): ' + self.mover.__doc__)

        if result:
            self.fleet = None
            self.obj = None
            self.light = False
            self.light_cells.clear()
            self.speech.speak(self.phrases['move_true'])
            self._ai.next_step()
        else:
            self.speech.speak(self.phrases['move_false'])

    def select_fleet(self, num):
        """Select fleet by number."""
        fleet = super().select_fleet(num)
        self.log.info(__name__ + ': ' + 'def ' + self.select_fleet.__name__ + '(): ' + self.select_fleet.__doc__)

        if fleet is not None:
            self.light_zone(fleet.ships[0].x, fleet.ships[0].y)
            self.light = True
            self.speech.speak(self.phrases['fleet_select'] + str(fleet.num) + '. ' + fleet.ships[0].name + str(fleet.get_ships_count()))
        else:
            self.speech.speak(self.phrases['fleet_none'])

    def select_obj(self):
        """Select object by current coordinate."""
        self.log.info(__name__ + ': ' + 'def ' + self.select_obj.__name__ + '(): ' + self.select_obj.__doc__)

        self.obj = self.get_obj(self._x, self._y)
        if self.obj is not None:
            if hasattr(self.obj, 'fleet') and (self.obj.fleet != 0):
                self.select_fleet(self.obj.fleet)
                return
            self.light_zone(self.obj.x, self.obj.y)
            self.light = True
            self.speech.speak(self.phrases['select'] + self.obj.name)
        else:
            self.speech.speak(self.phrases['select_none'])

    def light_zone(self, _x, _y):
        """Light zone for moving objects."""
        self.log.info(__name__ + ': ' + 'def ' + self.light_zone.__name__ + '(): ' + self.light_zone.__doc__)

        obj = self.get_obj(_x, _y)
        if obj.__class__.__name__ == 'TorpedoBoat':
            zone = product(range(_x - 2, _x + 3), range(_y - 2, _y + 3))
        else:
            zone = product(range(_x - 1, _x + 2), range(_y - 1, _y + 2))
        for _xy in zone:
            find = False
            if (_xy[0] > (self.board.cols - 1)) or (_xy[1] > (self.board.rows - 1)):
                find = True
            for ship in self.ships:
                if _xy[0] == ship.x and _xy[1] == ship.y:
                    find = True
            for fort in self.forts:
                if _xy[0] == fort.x and _xy[1] == fort.y:
                    find = True
            for mine in self.mines:
                if _xy[0] == mine.x and _xy[1] == mine.y:
                    find = True
            for torpedo in self.torpedos:
                if _xy[0] == torpedo.x and _xy[1] == torpedo.y:
                    find = True
            if not find:
                self.light_cells.append(self.board.get_cell(_xy[0], _xy[1]))

    def move(self, move_dir):
        """Move cursor on board."""
        self.log.info(__name__ + ': ' + 'def ' + self.move.__name__ + '(): ' + self.move.__doc__)

        if self._ai.ai_step:
            return
        if DIR.left == move_dir:
            if self._x > 0:
                self._x -= 1
            else:
                self.speech.speak(self.phrases['border'])
        elif DIR.right == move_dir:
            if (self.board.cols - 1) > self._x:
                self._x += 1
            else:
                self.speech.speak(self.phrases['border'])
        elif DIR.down == move_dir:
            if (self.board.rows - 1) > self._y:
                self._y += 1
            else:
                self.speech.speak(self.phrases['border'])
        elif DIR.up == move_dir:
            if self._y > 0:
                self._y -= 1
            else:
                self.speech.speak(self.phrases['border'])
        self.cell = self.board.get_cell(self._x, self._y)
        self.speak()

    def speak(self):
        """Speak objects on cell."""
        self.log.info(__name__ + ': ' + 'def ' + self.speak.__name__ + '(): ' + self.speak.__doc__)

        self.speech.speak(self.cell.pos)
        find = False
        players = [self, self._ai.player]
        for player in players:
            for fort in player.forts:
                if (self._x == fort.x) and (self._y == fort.y):
                    find = True
                    if fort.show:
                        self.speech.speak(fort.name)
                    else:
                        self.speech.speak(self.phrases['close'])
            for mine in player.mines:
                if (self._x == mine.x) and (self._y == mine.y):
                    find = True
                    if mine.show:
                        self.speech.speak(mine.name)
                    else:
                        self.speech.speak(self.phrases['close'])
            for torpedo in player.torpedos:
                if (self._x == torpedo.x) and (self._y == torpedo.y):
                    find = True
                    if torpedo.show:
                        self.speech.speak(torpedo.name)
                    else:
                        self.speech.speak(self.phrases['close'])
            for ship in player.ships:
                if (self._x == ship.x) and (self._y == ship.y):
                    find = True
                    if ship.show:
                        self.speech.speak(ship.name)
                    else:
                        self.speech.speak(self.phrases['close'])
        if not find:
            self.speech.speak(self.phrases['empty'])

    def select(self, shift=False):
        """Select object on board."""
        self.log.info(__name__ + ': ' + 'def ' + self.select.__name__ + '(): ' + self.select.__doc__)

        if self._ai.create_fleets:
            self.select_obj()
            self.create_fleet(shift)
        else:
            if self.get_obj(self._x, self._y) is None and self.obj is not None:
                self.mover(self._x, self._y)
            else:
                self.select_obj()

    def create_fleet(self, shift):
        """Create fleet from ships."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_fleet.__name__ + '(): ' + self.create_fleet.__doc__)

        if self.obj is not None and (self.obj.__class__.__name__ != 'Mine') and (self.obj.__class__.__name__ != 'Torpedo'):
            if self.fleet is None:
                self.fleet = Fleet(len(self.fleets) + 1)
            else:
                if self.fleet.ships[0].rate != self.obj.rate:
                    self.speech.speak(self.phrases['fleet_never'])
                    return
            self.obj.fleet = self.fleet.num
            self.fleet.add_ship(self.obj)
            self.speech.speak(self.phrases['fleet_add'] % self.fleet.num)
            self.obj = None
            if shift:
                self.fleets.append(self.fleet)
                self.speech.speak(self.phrases['fleet_create'] % self.fleet.num)
                self.fleet = None
                self.obj = None
        else:
            if shift:
                self.fix_coordinate_ships()
                self._ai.player.create_fleets()
                self._ai.next_step()
