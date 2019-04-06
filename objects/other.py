"""
Other objects for forts.

Created on 14.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

from objects.base import Base


class Fort(Base):
    """Fort object class."""

    def __init__(self, name, tex, symbol):
        """Initialise fort object."""
        super().__init__(name, tex, symbol)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class Mine(Base):
    """Mine object class."""

    def __init__(self, name, tex, symbol):
        """Initialise mine object."""
        super().__init__(name, tex, symbol)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)


class Torpedo(Base):
    """Torpedo object class."""

    def __init__(self, name, tex, symbol):
        """Initialise torpedo object."""
        super().__init__(name, tex, symbol)
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)
