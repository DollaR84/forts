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
    log.info('def ' + textures.__name__ + ': ' + textures.__doc__)

    with open('textures.dat', 'rb') as tex_file:
        pictures = pickle.load(tex_file)
        data = [(name, pic) for name, pic in pictures.items()]
        return processes.pic2tex(data)


def sounds(volume):
    """Load sounds wav data from binary file."""
    log = logging.getLogger()
    log.info('def ' + sounds.__name__ + ': ' + sounds.__doc__)

    with open('sounds.dat', 'rb') as file_data:
        wavs = pickle.load(file_data)
        data = [(name, wav) for name, wav in wavs.items()]
        return processes.sounds(data, volume)


def music():
    """Load music from binary file."""
    log = logging.getLogger()
    log.info('def ' + music.__name__ + ': ' + music.__doc__)

    with open('music.dat', 'rb') as file_data:
        return pickle.load(file_data)
