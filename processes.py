"""
Functions for multiprocessing.

Created on 23.11.2018

@author: Ruslan Dolovanyuk

"""

import io
import logging
import multiprocessing
import multiprocessing.pool

from itertools import repeat

import pygame


def __thread_pic2tex(data):
    """Convert png file object in pygame surface."""
    pic = io.BytesIO(data[1])
    image = pygame.image.load(pic)
    pic.close()
    return (data[0], image)


def __thread_sound(data, volume):
    """Create pygame Sound object."""
    wav = pygame.mixer.Sound(data[1])
    wav.set_volume(volume)
    return (data[0], wav)


def pic2tex(data):
    """Run threads for convert png to pygame surface."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + pic2tex.__name__ + '(): ' + pic2tex.__doc__)

    with multiprocessing.pool.ThreadPool() as pool:
        results = pool.map(__thread_pic2tex, data)
        return {name: tex for name, tex in results}


def sounds(data, volume):
    """Thread for load wav sound in pygame."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + sounds.__name__ + '(): ' + sounds.__doc__)

    with multiprocessing.pool.ThreadPool() as pool:
        results = pool.starmap(__thread_sound, zip(data, repeat(volume)))
        return {name: wav for name, wav in results}
