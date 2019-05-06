"""
Common functions for project.

Created on 06.05.2019

@author: Ruslan Dolovanyuk

"""

from collections import namedtuple

import math


Coordinate = namedtuple('Coordinate', ['x', 'y'])


def diff2list(diff):
    """Convert different to list."""
    result = []
    for _ in range(abs(diff)):
        result.append(int(math.copysign(1.0, diff)))
    return result


def add_coordinates(diff_x, diff_y):
    """Add coordinates for equel lists."""
    if len(diff_x) > len(diff_y):
        main = diff_x
        sub = diff_y
    else:
        main = diff_y
        sub = diff_x
    for _ in range(len(main) - len(sub)):
        sub.append(0)
