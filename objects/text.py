"""
Text objects for forts.

Created on 15.12.2018

@author: Ruslan Dolovanyuk

"""

import logging


class Text:
    """Text objects class."""

    def __init__(self, font_obj, text, _x, _y, color):
        """Initialize text class."""
        self.log = logging.getLogger()
        self.log.info('def ' + self.__init__.__name__ + ': ' + self.__init__.__doc__)

        self.font_obj = font_obj
        self.text_surface_obj = self.font_obj.render(text, True, color)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (_x, _y)

    def draw(self, screen):
        """Draw text object on screen."""
        screen.blit(self.text_surface_obj, self.text_rect_obj)
