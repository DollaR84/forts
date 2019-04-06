"""
Ship objects for forts.

Created on 14.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

from objects.base import Base


class Ship(Base):
    """Base ship class."""

    rate = property(lambda self: self.__rate)

    def __init__(self, name, tex, symbol, rate):
        """Initialize base ship class."""
        super().__init__(name, tex, symbol)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.__rate = rate
        self.fleet = 0


class Battleship(Ship):
    """Battleship class."""

    def __init__(self, name, tex, symbol):
        """Initialize battleship class."""
        super().__init__(name, tex, symbol, 7)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class Cruiser(Ship):
    """Cruiser class."""

    def __init__(self, name, tex, symbol):
        """Initialize cruiser class."""
        super().__init__(name, tex, symbol, 6)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class Destroyer(Ship):
    """Destroyer boat class."""

    def __init__(self, name, tex, symbol):
        """Initialize destroyer class."""
        super().__init__(name, tex, symbol, 5)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class GuardBoat(Ship):
    """Guard boat class."""

    def __init__(self, name, tex, symbol):
        """Initialize guard boat class."""
        super().__init__(name, tex, symbol, 4)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class TorpedoBoat(Ship):
    """Torpedo boat class."""

    def __init__(self, name, tex, symbol):
        """Initialize torpedo boat class."""
        super().__init__(name, tex, symbol, 3)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class Trawler(Ship):
    """Trawler class."""

    def __init__(self, name, tex, symbol):
        """Initialize trawler class."""
        super().__init__(name, tex, symbol, 2)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class Submarine(Ship):
    """Submarine class."""

    def __init__(self, name, tex, symbol):
        """Initialize submarine class."""
        super().__init__(name, tex, symbol, 1)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)
