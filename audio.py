"""
Sound and music module for games.

Created on 23.11.2018

@author: Ruslan Dolovanyuk

"""

import io
import time

import pygame

import loader


class Sound:
    """Sound class for games."""

    def __init__(self, volume):
        """Initialize sound class."""
        self.__sounds = loader.sounds(volume)

    def get_names(self):
        """Return names all sounds effects."""
        return list(self.__sounds.keys())

    def play(self, name):
        """Play sound by name."""
        self.__sounds[name].play()


class Music:
    """Music class for games."""

    def __init__(self, volume):
        """Initialize music class."""
        self.__music = loader.music()
        pygame.mixer.music.set_volume(volume)

    def get_names(self):
        """Return names all musics in collect."""
        return list(self.__music.keys())

    def play(self, name, loops=0):
        """Play music by name."""
        pygame.mixer.music.load(io.BytesIO(self.__music[name]))
        pygame.mixer.music.play(loops)


def test_sounds(sounds):
    """Test sound system."""
    for name in sounds.get_names():
        sounds.play(name)
        time.sleep(2)


def test_music(music):
    """Test music system."""
    name = music.get_names()[0]
    music.play(name)
    while pygame.mixer.music.get_busy():
        time.sleep(1)


if __name__ == '__main__':
    pygame.mixer.init()
    SOUNDS = Sound(1)
    MUSIC = Music(0.5)
    test_sounds(SOUNDS)
    test_music(MUSIC)
    test_music(MUSIC)
