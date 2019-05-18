"""
Compile module in python library pid.

Created on 18.05.2019

@author: Ruslan Dolovanyuk

example running:
    python compile.py build_ext --inplace

"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
               Extension("controllers.actions", ["controllers/actions.py"]),
               Extension("controllers.ai", ["controllers/ai.py"]),
               Extension("controllers.base", ["controllers/base.py"]),
               Extension("controllers.behaviors", ["controllers/behaviors.py"]),
               Extension("controllers.enemy", ["controllers/enemy.py"]),
               Extension("controllers.player", ["controllers/player.py"]),
               Extension("objects.base", ["objects/base.py"]),
               Extension("objects.fleets", ["objects/fleets.py"]),
               Extension("objects.other", ["objects/other.py"]),
               Extension("objects.ships", ["objects/ships.py"]),
               Extension("objects.text", ["objects/text.py"]),
               Extension("audio", ["audio.py"]),
               Extension("board", ["board.py"]),
               Extension("cell", ["cell.py"]),
               Extension("common", ["common.py"]),
               Extension("constants", ["constants.py"]),
               Extension("game", ["game.py"]),
               Extension("loader", ["loader.py"]),
               Extension("processes", ["processes.py"]),
               Extension("speech", ["speech.py"]),
               Extension("Tolk", ["Tolk.py"]),
               Extension("utils", ["utils.py"])
              ]

setup(
      name='main',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
)
