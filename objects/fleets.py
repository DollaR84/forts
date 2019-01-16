"""
Fleet object for forts.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""


class Fleet:
    """Fleet object from ships."""

    def __init__(self, num):
        """Initialize fleet object."""
        self.num = num
        self.ships = []

    def add_ship(self, ship):
        """Add link ship to array."""
        self.ships.append(ship)

    def get_ships_count(self):
        """Return count ships."""
        return len(self.ships)

    def get_ships_rate(self):
        """Return summ all ships rate."""
        result = 0
        for ship in self.ships:
            result += ship.rate
        return result
