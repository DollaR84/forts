"""
Ship objects for forts.

Created on 14.12.2018

@author: Ruslan Dolovanyuk

"""

from objects.base import Base


class Ship(Base):
    """Base ship class."""

    rate = property(lambda self: self.__rate)

    def __init__(self, name, tex, symbol, rate):
        """Initialize base ship class."""
        super().__init__(name, tex, symbol)
        self.__rate = rate
        self.fleet = 0


class Battleship(Ship):
    """Battleship class."""

    def __init__(self, name, tex, symbol):
        """Initialize battleship class."""
        super().__init__(name, tex, symbol, 7)


class Cruiser(Ship):
    """Cruiser class."""

    def __init__(self, name, tex, symbol):
        """Initialize cruiser class."""
        super().__init__(name, tex, symbol, 6)


class Destroyer(Ship):
    """Destroyer boat class."""

    def __init__(self, name, tex, symbol):
        """Initialize destroyer class."""
        super().__init__(name, tex, symbol, 5)


class GuardBoat(Ship):
    """Guard boat class."""

    def __init__(self, name, tex, symbol):
        """Initialize guard boat class."""
        super().__init__(name, tex, symbol, 4)


class TorpedoBoat(Ship):
    """Torpedo boat class."""

    def __init__(self, name, tex, symbol):
        """Initialize torpedo boat class."""
        super().__init__(name, tex, symbol, 3)


class Trawler(Ship):
    """Trawler class."""

    def __init__(self, name, tex, symbol):
        """Initialize trawler class."""
        super().__init__(name, tex, symbol, 2)


class Submarine(Ship):
    """Submarine class."""

    def __init__(self, name, tex, symbol):
        """Initialize submarine class."""
        super().__init__(name, tex, symbol, 1)
