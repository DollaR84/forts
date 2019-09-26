"""
Main game module for forts.

Created on 24.11.2018

@author: Ruslan Dolovanyuk

"""

import logging
import os
import pickle
import sys

from configparser import ConfigParser

import pygame

from audio import Music
from audio import Sound

from board import Board

from constants import Colors

from controllers.ai import AI
from controllers.player import DIR
from controllers.player import Player

from menu import Menu

from speech import Speech

from utils import Logger


class Game:
    """Main running class for game."""

    def __init__(self):
        """Initialize running class."""
        self.config = ConfigParser()
        self.config.read('settings.ini')

        if self.config.getboolean('total', 'debug'):
            if getattr(sys, 'frozen', False):
                self.logger = Logger(os.path.join(os.path.dirname(sys.executable), self.__class__.__name__))
            else:
                self.logger = Logger(os.path.join(os.getcwd(), self.__class__.__name__))
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.size_x = self.config.getint('screen', 'size_x')
        self.size_y = self.config.getint('screen', 'size_y')

        with open('languages.dat', 'rb') as lang_file:
            self.phrases = pickle.load(lang_file)[self.config.get('total', 'language')]

        self.speech = Speech(self.config)
        self.speech.speak(self.phrases['start'], True)

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption(self.phrases['title'])

        self.music = Music(self.config.getfloat('audio', 'music_volume'))
        self.sounds = Sound(self.config.getfloat('audio', 'sound_volume'))

        self.menu = Menu(self.config, self.screen, self.speech, self.phrases, self.sounds)
        self.menu_flag = True
        menu_functions = [self.new_game, self.rules, self.help, self.exit]
        self.menu.set_functions(menu_functions)

        self.board = Board(self.config, self.screen, self.sounds)
        self._ai = AI(self.board, self.speech, self.phrases)
        self.player = Player(self.board, self.speech, self.phrases, self._ai)
        self._ai.gamer = self.player
        self._ai.player.behaviors.set_controllers(self._ai)
        self.running = True
        self.game_over = True
        self.win = False

        self.handle_numbers = {'K_' + str(num): num for num in range(1, 10)}
        self.handle_numbers.update({'K_KP' + str(num): num for num in range(1, 10)})

        self.font_obj = pygame.font.SysFont('arial', 50)
        self.clock = pygame.time.Clock()

        self.music_play()
        self.menu.activate(self.menu_flag)

    def mainloop(self):
        """Run main loop game."""
        self.log.info(__name__ + ': ' + 'def ' + self.mainloop.__name__ + '(): ' + self.mainloop.__doc__)

        while self.running:
            self.handle_events()
            if self._ai.ai_step:
                self._ai.player.step()
            if self.menu_flag:
                self.menu.draw()
            else:
                self.draw()
            if not self.game_over:
                self.check_win()

            self.clock.tick(15)
            pygame.display.flip()

        self.speech.speak(self.phrases['finish'], True)
        self.speech.finish()
        self.board.finish()
        if self.config.getboolean('total', 'debug'):
            self.logger.finish()
        pygame.quit()

    def exit(self):
        """Exit from game in menu."""
        self.log.info(__name__ + ': ' + 'def ' + self.exit.__name__ + '(): ' + self.exit.__doc__)

        self.menu_flag = not self.menu_flag
        self.menu.activate(self.menu_flag)
        self.running = False

    def handle_events(self):
        """Check all game events."""
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.running = False
            elif pygame.KEYDOWN == event.type:
                self.handle_events_keydown(event)

    def handle_events_keydown(self, event):
        """Check keydown events."""
        self.handle_events_keydown_functional(event)
        self.handle_events_keydown_arrows(event)
        if pygame.K_ESCAPE == event.key:
            if not self.game_over:
                self.menu_flag = not self.menu_flag
                self.menu.activate(self.menu_flag)
        elif pygame.K_SPACE == event.key and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                self.player.select(True)
        elif pygame.K_SPACE == event.key:
            if self.menu_flag:
                self.menu.click()
            elif not self.game_over and not self._ai.ai_step:
                self.player.select()
        elif pygame.K_RETURN == event.key:
            if self.menu_flag:
                self.menu.click()
        elif pygame.K_c == event.key:
            if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                self.speech.speak(self.player.cell.pos, True)
        elif pygame.K_p == event.key:
            if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                phrase = self.phrases['your_info'] % self.player.info()
                self.speech.speak(phrase, True)
        elif pygame.K_e == event.key:
            if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                phrase = self.phrases['enemy_info'] % self._ai.player.info()
                self.speech.speak(phrase, True)
        for key, num in self.handle_numbers.items():
            if getattr(pygame, key) == event.key:
                if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                    self.player.select_fleet(num)

    def handle_events_keydown_functional(self, event):
        """Check functional keys."""
        if pygame.K_F1 == event.key:
            self.help()
        elif pygame.K_F2 == event.key:
            self.turn_music()
        elif pygame.K_F5 == event.key:
            self.new_game()
        elif pygame.K_F9 == event.key:
            self.change_language()

    def handle_events_keydown_arrows(self, event):
        """Check arrows keys."""
        if pygame.K_LEFT == event.key:
            if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                self.player.move(DIR.left)
        elif pygame.K_RIGHT == event.key:
            if not self.menu_flag and not self.game_over and not self._ai.ai_step:
                self.player.move(DIR.right)
        elif pygame.K_UP == event.key:
            if self.menu_flag:
                self.menu.change_button(-1)
            elif not self.game_over and not self._ai.ai_step:
                self.player.move(DIR.up)
        elif pygame.K_DOWN == event.key:
            if self.menu_flag:
                self.menu.change_button(1)
            elif not self.game_over and not self._ai.ai_step:
                self.player.move(DIR.down)

    def draw(self):
        """Main draw function."""
        self.screen.fill(Colors.GRAY)
        self.board.draw()
        if not self.game_over:
            self.player.draw()
            self._ai.player.draw()
            self._ai.draw()
            self.screen.blit(self.board.board, self.board.offset)
        else:
            if self.win:
                text_surface_obj = self.font_obj.render(self.phrases['win'], True, Colors.GREEN)
            else:
                text_surface_obj = self.font_obj.render(self.phrases['game_over'], True, Colors.RED)
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (self.size_x // 2, self.size_y // 2)
            self.screen.blit(text_surface_obj, text_rect_obj)

    def music_play(self):
        """Run music play."""
        self.log.info(__name__ + ': ' + 'def ' + self.music_play.__name__ + '(): ' + self.music_play.__doc__)

        if self.config.getboolean('audio', 'music'):
            name = self.music.get_names()[0]
            self.music.play(name, -1)

    def check_win(self):
        """Check win game."""
        if not self._ai.player.if_exists_forts():
            self.game_over = True
            self.win = True
            self.speech.speak(self.phrases['win'], True)
        elif not self.player.if_exists_forts():
            self.game_over = True
            self.win = False
            self.speech.speak(self.phrases['game_over'], True)

    def new_game(self):
        """Start new game."""
        self.log.info(__name__ + ': ' + 'def ' + self.new_game.__name__ + '(): ' + self.new_game.__doc__)

        self.menu_flag = not self.menu_flag
        self.menu.activate(self.menu_flag)
        self.speech.speak(self.phrases['new_game'], True)
        self.game_over = False
        self.win = False
        self._ai.player.init()
        self.player.init()
        self.player.create_fleets()
        #self._ai.ai_step = True # if remove create_fleets
        #self._ai.next_step() # if remove create_fleets
        self.player.speak()

    def help(self):
        """Speak help for keys control game."""
        self.log.info(__name__ + ': ' + 'def ' + self.help.__name__ + '(): ' + self.help.__doc__)

        language = self.config.get('total', 'language')
        with open('help.dat', 'rb') as help_file:
            data = pickle.load(help_file)
            for line in [line for line in data[language] if line != '\n']:
                self.speech.speak(line, False)

    def rules(self):
        """Speak help for rules game."""
        self.log.info(__name__ + ': ' + 'def ' + self.rules.__name__ + '(): ' + self.rules.__doc__)

        with open('help.dat', 'rb') as help_file:
            data = pickle.load(help_file)
            for line in [line for line in data['rules'] if line != '\n']:
                self.speech.speak(line, False)

    def turn_music(self):
        """On or off music in game."""
        self.log.info(__name__ + ': ' + 'def ' + self.turn_music.__name__ + '(): ' + self.turn_music.__doc__)

        if self.config.getboolean('audio', 'music'):
            self.config.set('audio', 'music', 'false')
            pygame.mixer.music.stop()
            self.speech.speak(self.phrases['music_off'], True)
        else:
            self.config.set('audio', 'music', 'true')
            self.music_play()
            self.speech.speak(self.phrases['music_on'], True)
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

    def change_language(self):
        """Change language for phrases."""
        self.log.info(__name__ + ': ' + 'def ' + self.change_language.__name__ + '(): ' + self.change_language.__doc__)

        if self.config.get('total', 'language') == 'ru':
            self.config.set('total', 'language', 'en')
            with open('languages.dat', 'rb') as lang_file:
                self.phrases = pickle.load(lang_file)['en']
        else:
            self.config.set('total', 'language', 'ru')
            with open('languages.dat', 'rb') as lang_file:
                self.phrases = pickle.load(lang_file)['ru']
        self.player.phrases = self.phrases
        self.speech.speak(self.phrases['language'], True)
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)
