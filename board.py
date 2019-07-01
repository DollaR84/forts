"""
Board for forts.

Created on 12.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

import pygame

from cell import Cell

from constants import Colors
from constants import Letters

import loader

from objects.text import Text


class Board:
    """Board class for forts."""

    def __init__(self, config, screen, sounds):
        """Initialize board class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.config = config
        self.screen = screen
        self.sounds = sounds

        self.screen_x = self.config.getint('screen', 'size_x')
        self.screen_y = self.config.getint('screen', 'size_y')
        self.rows = self.config.getint('board', 'rows')
        self.cols = self.config.getint('board', 'cols')
        self.size_cell = self.config.getint('board', 'size_cell')
        self.size_font = self.config.getint('board', 'size_font')

        self.font_obj = pygame.font.SysFont('arial', self.size_font)

        self.creator()

    def creator(self):
        """Create textures, cells and texts objects or loading from cache."""
        self.log.info(__name__ + ': ' + 'def ' + self.creator.__name__ + '(): ' + self.creator.__doc__)

        self.board = pygame.Surface(self.get_sizes())
        self.calc_offset()

        data = loader.load_cache()
        if data is None:
            self.cells = []
            self.text_obj = []
            self.textures = loader.textures()

            self.create_textures()
            self.convert_textures()
            self.create_cells()
            self.create_texts()
        else:
            self.textures = {}
            for name in list(data['textures'].keys()):
                if name == 'water_6':
                    self.textures[name] = pygame.image.fromstring(data['textures'][name][0], data['textures'][name][1], 'RGB')
                else:
                    self.textures[name] = pygame.image.fromstring(data['textures'][name][0], data['textures'][name][1], 'RGBA')
            self.cells = data['cells']
            self.text_obj = data['texts']

    def finish(self):
        """Save textures, cells and texts objects in cache file."""
        self.log.info(__name__ + ': ' + 'def ' + self.finish.__name__ + '(): ' + self.finish.__doc__)

        textures = {}
        for name in list(self.textures.keys()):
            if name == 'water_6':
                textures[name] = (pygame.image.tostring(self.textures[name], 'RGB'), self.textures[name].get_size())
            else:
                textures[name] = (pygame.image.tostring(self.textures[name], 'RGBA'), self.textures[name].get_size())
        loader.save_cache(self.get_sizes(), textures, self.cells, self.text_obj)

    def get_sizes(self):
        """Return calculated sizes x and y."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_sizes.__name__ + '(): ' + self.get_sizes.__doc__)

        return (self.cols * self.size_cell, self.rows * self.size_cell)

    def calc_offset(self):
        """Calculate position board on screen."""
        self.log.info(__name__ + ': ' + 'def ' + self.calc_offset.__name__ + '(): ' + self.calc_offset.__doc__)

        board_sizes = self.get_sizes()
        board_x = board_sizes[0]
        board_y = board_sizes[1]

        offset_x = (self.screen_x - board_x) // 2
        offset_y = self.size_font * 2 + ((self.screen_y - self.size_font - board_y) // 2)

        self.offset = (offset_x, offset_y)

    def draw(self):
        """Draw method for board."""
        for cell in self.cells:
            cell.draw(self.board)
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(self.board, Colors.WHITE, (col * self.size_cell, row * self.size_cell, self.size_cell, self.size_cell), 1)
        for text_obj in self.text_obj:
            text_obj.draw(self.screen)

    def create_cells(self):
        """Create cells."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_cells.__name__ + '(): ' + self.create_cells.__doc__)

        for row in range(self.rows):
            for col in range(self.cols):
                zone = pygame.Rect(col * self.size_cell, row * self.size_cell, self.size_cell, self.size_cell)
                tex = self.textures['water_6'].subsurface(zone)
                self.cells.append(Cell(col * self.size_cell, row * self.size_cell, self.size_cell, tex))
                self.cells[-1].pos = ''.join((Letters.latin_caps[row], str(col + 1)))

    def create_texts(self):
        """Create texts for rows and columns."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_texts.__name__ + '(): ' + self.create_texts.__doc__)

        for index in range(self.rows):
            _x1 = self.offset[0] // 2
            _x2 = self.screen_x - _x1
            _y = self.offset[1] + (self.size_cell // 2) + index * self.size_cell
            self.text_obj.append(Text(self.font_obj, Letters.latin_caps[index], _x1, _y, Colors.WHITE))
            self.text_obj.append(Text(self.font_obj, Letters.latin_caps[index], _x2, _y, Colors.WHITE))
        for index in range(self.cols):
            _x = self.offset[0] + (self.size_cell // 2) + index * self.size_cell
            _y1 = self.size_font * 2 + ((self.offset[1] - self.size_font * 2) // 2)
            _y2 = self.screen_y - _y1
            self.text_obj.append(Text(self.font_obj, str(index + 1), _x, _y1, Colors.WHITE))
            self.text_obj.append(Text(self.font_obj, str(index + 1), _x, _y2, Colors.WHITE))

    def create_textures(self):
        """Create textures for objects."""
        self.log.info(__name__ + ': ' + 'def ' + self.create_textures.__name__ + '(): ' + self.create_textures.__doc__)

        fort = pygame.Surface((self.size_cell, self.size_cell), pygame.SRCALPHA, 32)
        fort.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        pygame.draw.rect(fort, Colors.SILVER, (0, 0, self.size_cell, self.size_cell))
        pygame.draw.rect(fort, Colors.GRAY, (0, 0, self.size_cell, self.size_cell), 2)
        pygame.draw.rect(fort, Colors.GRAY, (10, 10, self.size_cell - 10, self.size_cell - 10), 1)
        self.textures['fort'] = fort
        chip = pygame.Surface((self.size_cell, self.size_cell), pygame.SRCALPHA, 32)
        chip.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        half = self.size_cell // 2
        pygame.draw.circle(chip, Colors.SILVER, (half, half), half)
        pygame.draw.circle(chip, Colors.GRAY, (half, half), half, 2)
        pygame.draw.circle(chip, Colors.GRAY, (half, half), half - 10, 1)
        self.textures['chip'] = chip

    def convert_textures(self):
        """Convert textures for pygame."""
        self.log.info(__name__ + ': ' + 'def ' + self.convert_textures.__name__ + '(): ' + self.convert_textures.__doc__)

        for name in list(self.textures.keys()):
            if name == 'water_6':
                self.textures[name] = self.textures[name].convert()
            else:
                self.textures[name] = self.textures[name].convert_alpha()

    def get_cell(self, _x, _y):
        """Return cell from x and y coordinate."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_cell.__name__ + '(): ' + self.get_cell.__doc__)

        index = (_y * self.cols) + _x
        return self.cells[index]
