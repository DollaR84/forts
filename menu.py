"""
Menu module for forts.

Created on 22.09.2019

@author: Ruslan Dolovanyuk

"""

import logging

import pygame

from constants import Colors

from objects.text import Text


class Menu:
    """Menu class for forts."""

    def __init__(self, config, screen, speech, phrases, sounds):
        """Initialize menu class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.config = config
        self.screen = screen
        self.speech = speech
        self.phrases = phrases
        self.sounds = sounds

        self.screen_x = self.config.getint('screen', 'size_x')
        self.screen_y = self.config.getint('screen', 'size_y')
        self.textures = {}

        self.button_x = self.config.getint('menu', 'button_x')
        self.button_y = self.config.getint('menu', 'button_y')
        self.buttons = []

        self.size_font = self.config.getint('menu', 'size_font')
        self.font_obj = pygame.font.SysFont('arial', self.size_font)

        self.__current = 0
        self.creator()

    def creator(self):
        """Create buttons for menu."""
        self.log.info(__name__ + ': ' + 'def ' + self.creator.__name__ + '(): ' + self.creator.__doc__)

        self.calc_offset()
        self.create_textures()
        self.convert_textures()
        self.create_buttons()

    def calc_offset(self):
        """Calculate position menu buttons on screen."""
        self.log.info(__name__ + ': ' + 'def ' + self.calc_offset.__name__ + '(): ' + self.calc_offset.__doc__)

        offset_x = self.screen_x // 2
        offset_y = (self.screen_y // 2) - ((len(self.phrases['menu_buttons']) // 2) * (self.button_y + self.size_font *2))

        self.offset = (offset_x, offset_y)

    def create_textures(self):
        """Create textures for buttons."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_textures.__name__ + '(): ' + self.create_textures.__doc__)

        button = pygame.Surface((self.button_x, self.button_y), pygame.SRCALPHA, 32)
        button.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)
        pygame.draw.rect(button, Colors.DEEPSKYBLUE, (0, 0, self.button_x, self.button_y))
        pygame.draw.rect(button, Colors.BLACK, (0, 0, self.button_x, self.button_y), 2)
        self.textures['button'] = button

    def convert_textures(self):
        """Convert textures for pygame."""
        self.log.info(__name__ + ': ' + 'def ' + self.convert_textures.__name__ + '(): ' + self.convert_textures.__doc__)

        for name in list(self.textures.keys()):
            self.textures[name] = self.textures[name].convert_alpha()

    def create_buttons(self):
        """Create buttons for menu."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_buttons.__name__ + '(): ' + self.create_buttons.__doc__)

        for index, phrase in enumerate(self.phrases['menu_buttons']):
            _x = self.offset[0]
            _y = self.offset[1] + (self.button_y + self.size_font * 2) * index
            text = Text(self.font_obj, phrase, _x, _y, Colors.ORANGE)
            self.buttons.append(Button(_x, _y, self.textures['button'], text))

    def draw(self):
        """Draw method for menu."""
        self.screen.fill(Colors.CHARTREUSE)
        for button in self.buttons:
            button.draw(self.screen)

    def activate(self, flag):
        """Open or close menu."""
        self.log.info(__name__ + ': ' + 'def ' + self.activate.__name__ + '(): ' + self.activate.__doc__)

        if flag:
            self.sounds.play('menu')
            self.speech.speak(self.phrases['menu_caption'], True)
            self.speech.speak(self.phrases['menu_buttons'][self.__current], True)
        else:
            self.sounds.play('close')

    def change_button(self, step):
        """Change current button."""
        self.log.info(__name__ + ': ' + 'def ' + self.change_button.__name__ + '(): ' + self.change_button.__doc__)

        self.__current += step
        if self.__current == -1:
            self.__current = len(self.phrases['menu_buttons']) - 1
        if self.__current == len(self.phrases['menu_buttons']):
            self.__current = 0
        self.sounds.play('down')
        self.speech.speak(self.phrases['menu_buttons'][self.__current], True)

    def set_functions(self, functions):
        """Set functions list for menu buttons."""
        self.log.info(__name__ + ': ' + 'def ' + self.set_functions.__name__ + '(): ' + self.set_functions.__doc__)

        self.functions = functions

    def click(self):
        """Click on button."""
        self.log.info(__name__ + ': ' + 'def ' + self.click.__name__ + '(): ' + self.click.__doc__)

        self.sounds.play('click')
        self.functions[self.__current]()


class Button:
    """Class Button for menu."""

    def __init__(self, x_, y_, texture, text):
        """Initialize button for menu."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.__x = x_
        self.__y = y_
        self.__texture = texture
        self.__text = text

        left = self.__x - (self.__texture.get_width() // 2)
        top = self.__y - (self.__texture.get_height() // 2)
        self.__offset = (left, top)

    def draw(self, screen):
        """Draw method for button on menu screen."""
        screen.blit(self.__texture, self.__offset)
        self.__text.draw(screen)
