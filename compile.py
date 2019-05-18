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
               Extension("actions", ["controllers/actions.py"]),
               Extension("ai", ["controllers/ai.py"]),
               Extension("base", ["controllers/base.py"]),
               Extension("behaviors", ["controllers/behaviors.py"]),
               Extension("enemy", ["controllers/enemy.py"]),
               Extension("player", ["controllers/player.py"]),
               Extension("base", ["objects/base.py"]),
               Extension("fleets", ["objects/fleets.py"]),
               Extension("other", ["objects/other.py"]),
               Extension("ships", ["objects/ships.py"]),
               Extension("text", ["objects/text.py"]),
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
