"""
Base module objects for forts.

Created on 18.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

from constants import Colors

from objects.text import Text


class Base:
    """Base objects class."""

    def __init__(self, name, tex, symbol):
        """Initialize base class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.__x = 0
        self.__y = 0

        self.name = name
        self.texture = tex
        self.__symbol = symbol
        self.__text = None
        self.show = False

    def draw(self, board):
        """Draw object on board surface."""
        cell = board.get_cell(self.x, self.y)
        board.board.blit(self.texture, (cell.left, cell.top))
        if self.show:
            if self.__text is None:
                self.__text = Text(board.font_obj, self.__symbol, cell.left + (cell.size // 2), cell.top + (cell.size // 2), Colors.BLUE)
            self.__text.draw(board.board)

    @property
    def x(self):  # pylint: disable=C0103
        """Return x number cell coordinate."""
        return self.__x

    @x.setter
    def x(self, value):  # pylint: disable=C0103
        """Set x num cell coordinate."""
        self.__x = value
        self.__text = None

    @property
    def y(self):  # pylint: disable=C0103
        """Return y number cell coordinate."""
        return self.__y

    @y.setter
    def y(self, value):  # pylint: disable=C0103
        """Set y num cell coordinate."""
        self.__y = value
        self.__text = None

    def __eq__(self, other):
        """Comparasion two object id."""
        if id(self) == id(other):
            return True
        return False
