"""
Tests for forts ai.

Created on 25.12.2018

@author: Ruslan Dolovanyuk

"""

import pickle

from configparser import ConfigParser

import pygame

import controllers.ai


class Cell:
    """Emulate cell class from project."""

    def __init__(self):
        """Initialize emulate class."""
        self.left = 0
        self.top = 0


class Speech:
    """Emulate speech class."""

    @classmethod
    def speak(cls, phrase):
        """Emulate speak method."""
        print(phrase)


class Board:
    """Emulate board class from project."""

    def __init__(self, config):
        """Initialize emulate class."""
        self.config = config
        self.screen = None
        self.screen_x = self.config.getint('screen', 'size_x')
        self.screen_y = self.config.getint('screen', 'size_y')
        self.rows = self.config.getint('board', 'rows')
        self.cols = self.config.getint('board', 'cols')
        self.size_font = self.config.getint('board', 'size_font')
        self.font_obj = pygame.font.SysFont('arial', self.size_font)
        self.textures = dict.fromkeys(['fort', 'chip'])
        self.cells = []
        for _ in range(self.rows * self.cols):
            self.cells.append(Cell())

    def get_cell(self, _x, _y):
        """Return emulate cell."""
        index = (_y * self.cols) + _x
        return self.cells[index]


def test_create_fleets(_ai):
    """Test creating fleets with ships."""
    _ai.player.create_fleets()
    for fleet in _ai.player.fleets:
        print('Fleet {}:'.format(fleet.num))
        for ship in fleet.ships:
            print('  {};'.format(ship.name))
    print('Всего эскадр: {}'.format(len(_ai.player.fleets)))
    ships = 0
    for fleet in _ai.player.fleets:
        ships += fleet.get_ships_count()
    print('Всего кораблей в эскадрах: {}'.format(ships))
    print('Всего кораблей: {}'.format(len(_ai.player.ships)))


def test_diff2list(_ai):
    """Test diff2list method from controllers."""
    test_vars = [x for x in range(-2, 3)]
    for var in test_vars:
        print(_ai.player.diff2list(var))


if __name__ == '__main__':
    CONFIG = ConfigParser()
    CONFIG.read('settings.ini')
    pygame.init()
    pygame.font.init()
    PHRASES = None
    with open('languages.dat', 'rb') as lang_file:
        PHRASES = pickle.load(lang_file)[CONFIG.get('total', 'language')]
        SPEECH = Speech()
        BOARD = Board(CONFIG)
        AI = controllers.ai.AI(BOARD, SPEECH, PHRASES)
        AI.player.init()

    test_create_fleets(AI)
    test_diff2list(AI)
