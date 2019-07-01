"""
Text objects for forts.

Created on 15.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

import pygame


class Text:
    """Text objects class."""

    def __init__(self, font_obj, text, _x, _y, color):
        """Initialize text class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.__x = _x
        self.__y = _y
        self.font_obj = font_obj
        self.text_surface_obj = self.font_obj.render(text, True, color)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.__x, self.__y)

    def draw(self, screen):
        """Draw text object on screen."""
        screen.blit(self.text_surface_obj, self.text_rect_obj)

    def __getstate__(self):
        """Get information for saving pickle in cache."""
        state = {}
        state['x'] = self.__x
        state['y'] = self.__y
        state['texture'] = (pygame.image.tostring(self.text_surface_obj, 'RGBA'), self.text_surface_obj.get_size())
        return state

    def __setstate__(self, state):
        """Set information from cache."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.__x = state['x']
        self.__y = state['y']
        self.font_obj = None
        self.text_surface_obj = pygame.image.fromstring(state['texture'][0], state['texture'][1], 'RGBA')
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.__x, self.__y)
