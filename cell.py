"""
Cell on board forts.

Created on 12.12.2018

@author: Ruslan Dolovanyuk

"""


class Cell:
    """Cell class on board for forts."""

    def __init__(self, left, top, size, tex):
        """Initialize cell class."""
        self.left = left
        self.top = top
        self.size = size
        self.texture = tex
        self.offset = (self.left, self.top)
        self.pos = ''

    def draw(self, board):
        """Draw method for cell."""
        board.blit(self.texture, self.offset)
