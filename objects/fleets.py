"""
Fleet object for forts.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""

import logging


class Fleet:
    """Fleet object from ships."""

    def __init__(self, num):
        """Initialize fleet object."""
        self.log = logging.getLogger()
        self.log.info('def ' + self.__init__.__name__ + ': ' + self.__init__.__doc__)

        self.num = num
        self.ships = []

    def add_ship(self, ship):
        """Add link ship to array."""
        self.log.info('def ' + self.add_ship.__name__ + ': ' + self.add_ship.__doc__)

        self.ships.append(ship)

    def get_ships_count(self):
        """Return count ships."""
        self.log.info('def ' + self.get_ships_count.__name__ + ': ' + self.get_ships_count.__doc__)

        return len(self.ships)

    def get_ships_rate(self):
        """Return summ all ships rate."""
        self.log.info('def ' + self.get_ships_rate.__name__ + ': ' + self.get_ships_rate.__doc__)

        result = 0
        for ship in self.ships:
            result += ship.rate
        return result
