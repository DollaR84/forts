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
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.num = num
        self.ships = []

    def add_ship(self, ship):
        """Add link ship to array."""
        self.log.info(__name__ + ': ' + 'def ' + self.add_ship.__name__ + '(): ' + self.add_ship.__doc__)

        for obj in self.ships:
            if id(obj) == id(ship):
                return
        self.ships.append(ship)

    def del_ship(self, ship):
        """Remove link ship from array."""
        self.log.info(__name__ + ': ' + 'def ' + self.del_ship.__name__ + '(): ' + self.del_ship.__doc__)

        index = -1
        for index, obj in enumerate(self.ships):
            if id(obj) == id(ship):
                break
        if index != -1:
            self.ships.pop(index)

    def get_ships_count(self):
        """Return count ships."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_ships_count.__name__ + '(): ' + self.get_ships_count.__doc__)

        return len(self.ships)

    def get_ships_rate(self):
        """Return summ all ships rate."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_ships_rate.__name__ + '(): ' + self.get_ships_rate.__doc__)

        result = 0
        for ship in self.ships:
            result += ship.rate
        return result
