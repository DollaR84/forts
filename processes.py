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

import common

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


def get_routes(obj, enemy_list):
    """Return routes from ai object to enemy objects."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + get_routes.__name__ + '(): ' + get_routes.__doc__)

    with multiprocessing.pool.ThreadPool() as pool:
        results = pool.starmap(__thread_route, zip(enemy_list, repeat(obj)))
        return results


def __thread_route(enemy, obj):
    """Calculation route from obj to enemy."""
    route = []
    diff_x = common.diff2list(enemy.x - obj.x)
    diff_y = common.diff2list(enemy.y - obj.y)
    common.add_coordinates(diff_x, diff_y)
    route.append(common.Coordinate(obj.x + diff_x[0], obj.y + diff_y[0]))
    for index in range(1, len(diff_x) - 1):
        route.append(common.Coordinate(route[index - 1].x + diff_x[index], route[index - 1].y + diff_y[index]))
    return route
