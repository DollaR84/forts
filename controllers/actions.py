"""
Extended module for behaviors.

Created on 11.03.2019

@author: Ruslan Dolovanyuk

"""

import ctypes
import logging

import common

import processes


class Naming:
    """Set global variables."""

    tactics = ('attack_fort', 'attack_object', 'torpedo', 'mine')


class Action:
    """Action state in object view."""
    __slots__ = 'log', 'object', 'coordinates', 'priority', 'rate'

    def __init__(self, obj, coordinates, tactic, rate):
        """Initialise action state."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.object = obj
        self.coordinates = coordinates
        self.priority = Naming.tactics.index(tactic)
        self.rate = rate


class Analysis:
    """Find best tactic for ai game."""

    def __init__(self, player, enemy, cols, rows):
        """Initialise analysis class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.player = player
        self.enemy = enemy
        self.cols = cols
        self.rows = rows

        self.p_mines = []
        self.p_torpedos = []
        self.p_ships = []
        self.p_forts = []
        self.p_objects = []
        self.g_forts = []
        self.g_objects = []

        self.field = None
        self.c_field = None
        self.c_best = StAction()
        self.actions = []

        self.sLib = ctypes.windll.LoadLibrary('ai.dll')

    def clear(self):
        """Clear temporary lists."""
        self.log.info(__name__ + ': ' + 'def ' + self.clear.__name__ + '(): ' + self.clear.__doc__)

        self.p_mines.clear()
        self.p_torpedos.clear()
        self.p_ships.clear()
        self.actions.clear()

    def run(self):
        """Run analysis tactics."""
        self.log.info(__name__ + ': ' + 'def ' + self.run.__name__ + '(): ' + self.run.__doc__)

        for obj in self.p_objects:
            if obj.__class__.__name__ == 'Mine':
                self.p_mines.append(obj)
            elif obj.__class__.__name__ == 'Torpedo':
                self.p_torpedos.append(obj)
            else:
                self.p_ships.append(obj)

        for name in Naming.tactics:
            getattr(self, name)()

        best = self.get_best_action()
        self.clear()
        return best

    def attack_fort(self):
        """Analysi attack on enemy fort."""
        self.log.info(__name__ + ': ' + 'def ' + self.attack_fort.__name__ + '(): ' + self.attack_fort.__doc__)

        #self.base_analysis(self.p_ships, self.g_forts, self.attack_fort.__name__)
        self.base_analysis_dll(self.p_ships, self.g_forts, self.attack_fort.__name__)

    def attack_object(self):
        """Analysi attack on enemy object."""
        self.log.info(__name__ + ': ' + 'def ' + self.attack_object.__name__ + '(): ' + self.attack_object.__doc__)

        #self.base_analysis(self.p_ships, self.g_objects, self.attack_object.__name__)
        self.base_analysis_dll(self.p_ships, self.g_objects, self.attack_object.__name__)

    def torpedo(self):
        """Analysi torpedo attack on enemy object."""
        self.log.info(__name__ + ': ' + 'def ' + self.torpedo.__name__ + '(): ' + self.torpedo.__doc__)

        #self.base_analysis(self.p_torpedos, self.g_objects, self.torpedo.__name__)
        self.base_analysis_dll(self.p_torpedos, self.g_objects, self.torpedo.__name__)

    def mine(self):
        """Analysi mine attack on enemy object."""
        self.log.info(__name__ + ': ' + 'def ' + self.mine.__name__ + '(): ' + self.mine.__doc__)

        #self.base_analysis(self.p_mines, self.g_objects, self.mine.__name__)
        self.base_analysis_dll(self.p_mines, self.g_objects, self.mine.__name__)

    def base_analysis(self, player_objects, enemy_objects, tactic):
        """Base analysis tactic for battle."""
        self.log.info(__name__ + ': ' + 'def ' + self.base_analysis.__name__ + '(): ' + self.base_analysis.__doc__)

        best = None
        rate = 0
        for obj in player_objects:
            routes = processes.get_routes(obj, enemy_objects)
            for route in routes:
                empty = True
                for coord in route:
                    if self.player.get_obj(coord.x, coord.y) is not None or self.enemy.get_obj(coord.x, coord.y) is not None:
                        empty = False
                if empty:
                    temp_rate = 1000 - len(route) * 100
                    if tactic == 'attack_fort':
                        temp_rate += 500
                    step2 = None
                    if (obj.__class__.__name__ == 'TorpedoBoat') and (len(route) > 1):
                        step2 = route[1]
                        temp_rate += 100
                    if temp_rate > rate:
                        rate = temp_rate
                        best = Action(obj, (route[0], step2), tactic, rate)
        if best is not None:
            self.actions.append(best)

    def get_best_action(self):
        """Return best actions from all actions."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_best_action.__name__ + '(): ' + self.get_best_action.__doc__)

        best = None
        if self.actions:
            best = self.actions[0]
            best_rate = best.rate - (best.priority * 100)
            for action in self.actions:
                rate = action.rate - (action.priority * 100)
                if rate > best_rate:
                    best = action
                    best_rate = rate
        return best

    def base_analysis_dll(self, player_objects, enemy_objects, tactic):
        """Base analysis tactic for battle in C DLL."""
        self.log.info(__name__ + ': ' + 'def ' + self.base_analysis_dll.__name__ + '(): ' + self.base_analysis_dll.__doc__)

        player_objects_p = self.py_obj_list2c_u_array(player_objects, False)
        enemy_objects_p = self.py_obj_list2c_u_array(enemy_objects, True)

        c_attack_fort = ctypes.c_bool(True) if (tactic == 'attack_fort') else ctypes.c_bool(False)
        self.sLib.base_analysis.argtypes = [ctypes.POINTER(StUnit), ctypes.c_size_t, ctypes.POINTER(StUnit), ctypes.c_size_t, ctypes.c_bool, ctypes.POINTER(StAction)]
        self.sLib.base_analysis.restype = ctypes.c_bool
        result = self.sLib.base_analysis(player_objects_p, ctypes.c_size_t(len(player_objects)), enemy_objects_p, ctypes.c_size_t(len(enemy_objects)), c_attack_fort, ctypes.pointer(self.c_best))
        if result:
            obj = self.player.get_obj(self.c_best.x, self.c_best.y)
            if obj.__class__.__name__ == 'TorpedoBoat':
                coordinates = (common.Coordinate(self.c_best.cx1, self.c_best.cy1), common.Coordinate(self.c_best.cx2, self.c_best.cy2))
            else:
                coordinates = (common.Coordinate(self.c_best.cx1, self.c_best.cy1), None)
            best = Action(obj, coordinates, tactic, self.c_best.rate)
            self.actions.append(best)

    def py_obj_list2c_u_array(self, py_obj_list, enemy):
        """Convert list objects to array C units for dll."""
        self.log.info(__name__ + ': ' + 'def ' + self.py_obj_list2c_u_array.__name__ + '(): ' + self.py_obj_list2c_u_array.__doc__)

        result = (StUnit * len(py_obj_list))()
        for i in range(len(py_obj_list)):
            result[i] = self.obj2uc(py_obj_list[i], enemy)
        return ctypes.cast(result, ctypes.POINTER(StUnit))

    def obj2uc(self, obj, enemy):
        """Convert object to C unit for dll."""
        self.log.info(__name__ + ': ' + 'def ' + self.obj2uc.__name__ + '(): ' + self.obj2uc.__doc__)

        unit = StUnit()
        unit.x = obj.x
        unit.y = obj.y
        unit.enemy = enemy
        unit.fort = True if obj.__class__.__name__ == 'Fort' else False
        unit.exist = True
        return unit

    def set_field_dll(self):
        """Set field array in dll."""
        self.log.info(__name__ + ': ' + 'def ' + self.set_field_dll.__name__ + '(): ' + self.set_field_dll.__doc__)

        self.c_field = self.pyfield2cfield(self.field)
        self.sLib.set_field.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_bool))]
        self.sLib.set_field.restype = None
        self.sLib.set_field(self.c_field)

    def pyfield2cfield(self, field):
        """Convert python unit class from field to ctypes structure in C field."""
        self.log.info(__name__ + ': ' + 'def ' + self.pyfield2cfield.__name__ + '(): ' + self.pyfield2cfield.__doc__)

        rowType = ctypes.c_bool * self.cols
        resultType = ctypes.POINTER(ctypes.c_bool) * self.rows
        result = resultType()
        for x in range(self.rows):
            row = rowType()
            for y in range(self.cols):
                if field[x][y] is None:
                    row[y] = ctypes.c_bool(False)
                else:
                    row[y] = ctypes.c_bool(True)
            result[x] = ctypes.cast(row, ctypes.POINTER(ctypes.c_bool))
        return ctypes.cast(result, ctypes.POINTER(ctypes.POINTER(ctypes.c_bool)))


class StUnit(ctypes.Structure):
    _fields_ = [
                ('x', ctypes.c_int),
                ('y', ctypes.c_int),
                ('enemy', ctypes.c_bool),
                ('fort', ctypes.c_bool),
                ('exist', ctypes.c_bool)
               ]


class StAction(ctypes.Structure):
    _fields_ = [
                ('x', ctypes.c_int),
                ('y', ctypes.c_int),
                ('cx1', ctypes.c_int),
                ('cy1', ctypes.c_int),
                ('cx2', ctypes.c_int),
                ('cy2', ctypes.c_int),
                ('rate', ctypes.c_int)
               ]
