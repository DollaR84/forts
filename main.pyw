"""
Main module for running forts game.

Created on 24.11.2018

@author: Ruslan Dolovanyuk

"""

import multiprocessing

from game import Game


if __name__ == '__main__':
    multiprocessing.freeze_support()
    game = Game()
    game.mainloop()
