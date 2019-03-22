"""
Enemy module controller.

Created on 18.12.2018

@author: Ruslan Dolovanyuk

"""

import logging
import random

from itertools import product

from controllers.base import Base
from controllers.behaviors import Behavior

from objects.fleets import Fleet


class Enemy(Base):
    """Enemy class controller."""

    def __init__(self, board, speech, phrases, ai):
        """Initialize enemy controller."""
        super().__init__(board, speech, phrases, ai)
        self.log = logging.getLogger()
        self.log.info('def ' + self.__init__.__name__ + ': ' + self.__init__.__doc__)
        self.log.info('id controller: ' + str(id(self)))

        self.fleet = None
        self.obj = None

        self.behaviors = Behavior(self.board.cols, self.board.rows)

        random.seed()

    def init(self):
        """Initialize ships and other objects for AI."""
        super().init()
        self.log.info('def ' + self.init.__name__ + ': ' + self.init.__doc__)

        for index, fort in enumerate(self.forts):
            fort.x = self.board.cols - 1
            fort.y = 3 + index * 5
            fort.show = True
        zone_cells = list(product(range(self.board.cols // 2 + 1, self.board.cols - 1), range(self.board.rows)))
        self.init_coordinates(zone_cells)

    def create_fleets(self):
        """Create fleets ai enemy."""
        self.log.info('def ' + self.create_fleets.__name__ + ': ' + self.create_fleets.__doc__)

        self._ai.ai_step = True
        self._ai.set_text(self.phrases['fleet_create_ai'])
        self.speech.speak(self.phrases['fleet_create_ai'])
        id_ships = []
        fleets = random.randint(0, 5)
        for index in range(1, fleets + 1):
            fleet = Fleet(index)
            ships = random.randint(2, 3)
            for _ in range(ships):
                if not fleet.ships:
                    fleet.add_ship(random.choice(self.ships))
                    fleet.ships[0].fleet = fleet.num
                    for ship in self.ships:
                        if ship.rate == fleet.ships[0].rate:
                            id_ships.append(id(ship))
                    continue
                ship_id = random.choice(id_ships)
                for ship in self.ships:
                    if ship_id == id(ship):
                        ship.fleet = fleet.num
                        fleet.add_ship(ship)
                        id_ships.remove(ship_id)
                        break
                if not id_ships:
                    break
            self.fleets.append(fleet)
            id_ships.clear()
        self.fix_coordinate_ships()
        self._ai.create_fleets = False

    def select_fleet(self, num):
        """Select fleet by number."""
        self.fleet = super().select_fleet(num)
        self.log.info('def ' + self.select_fleet.__name__ + ': ' + self.select_fleet.__doc__)

    def mover(self, _x, _y):  # pylint: disable=W0221
        """Move object on board."""
        super().mover(self, self.obj, _x, _y)
        self.log.info('def ' + self.mover.__name__ + ': ' + self.mover.__doc__)

        self.fleet = None
        self.obj = None
        self._ai.next_step()

    def step(self):
        """AI step moving."""
        self.log.info('def ' + self.step.__name__ + ': ' + self.step.__doc__)

        if not self._ai.ai_step:
            return
        self.behaviors.step()
        self._ai.next_step()
