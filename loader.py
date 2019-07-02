"""
Functions for loading resources.

Created on 23.11.2018

@author: Ruslan Dolovanyuk

"""

import logging
import pickle

import processes


def textures():
    """Load textures from binary file."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + textures.__name__ + '(): ' + textures.__doc__)

    with open('textures.dat', 'rb') as tex_file:
        pictures = pickle.load(tex_file)
        data = [(name, pic) for name, pic in pictures.items()]
        return processes.pic2tex(data)


def sounds(volume):
    """Load sounds wav data from binary file."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + sounds.__name__ + '(): ' + sounds.__doc__)

    with open('sounds.dat', 'rb') as file_data:
        wavs = pickle.load(file_data)
        data = [(name, wav) for name, wav in wavs.items()]
        return processes.sounds(data, volume)


def music():
    """Load music from binary file."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + music.__name__ + '(): ' + music.__doc__)

    with open('music.dat', 'rb') as file_data:
        return pickle.load(file_data)


def load_cache():
    """Load textures, cells and texts objects from cache file."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + load_cache.__name__ + '(): ' + load_cache.__doc__)

    try:
        cache_file = open('cache.dat', 'rb')
    except IOError as e:
        return None
    else:
        with cache_file:
            data = pickle.load(cache_file)
            return data


def save_cache(sizes, textures, cells, texts):
    """Save textures, cells and texts objects in cache file."""
    log = logging.getLogger()
    log.info(__name__ + ': ' + 'def ' + save_cache.__name__ + '(): ' + save_cache.__doc__)

    data = {'sizes': sizes, 'textures': textures, 'cells': cells, 'texts': texts}
    with open('cache.dat', 'wb') as save_file:
        pickle.dump(data, save_file)
