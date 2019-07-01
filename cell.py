"""
Cell on board forts.

Created on 12.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

import pygame


class Cell:
    """Cell class on board for forts."""

    def __init__(self, left, top, size, tex):
        """Initialize cell class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.left = left
        self.top = top
        self.size = size
        self.texture = tex
        self.offset = (self.left, self.top)
        self.pos = ''

    def draw(self, board):
        """Draw method for cell."""
        board.blit(self.texture, self.offset)

    def __getstate__(self):
        """Get information for saving pickle in cache."""
        state = {}
        state['left'] = self.left
        state['top'] = self.top
        state['size'] = self.size
        state['texture'] = (pygame.image.tostring(self.texture, 'RGB'), self.texture.get_size())
        state['pos'] = self.pos
        return state

    def __setstate__(self, state):
        """Set state all information object from cache."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.left = state['left']
        self.top = state['top']
        self.size = state['size']
        self.texture = pygame.image.fromstring(state['texture'][0], state['texture'][1], 'RGB')
        self.offset = (self.left, self.top)
        self.pos = state['pos']
