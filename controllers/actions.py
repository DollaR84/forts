"""
Extended module for behaviors.

Created on 11.03.2019

@author: Ruslan Dolovanyuk

"""

import logging
import time

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

    def __init__(self, player, enemy):
        """Initialise analysis class."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.player = player
        self.enemy = enemy

        self.field = None
        self.p_mines = []
        self.p_torpedos = []
        self.p_ships = []
        self.p_forts = []
        self.p_objects = []
        self.g_forts = []
        self.g_objects = []

        self.actions = []

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

        self.base_analysis(self.p_ships, self.g_forts, self.attack_fort.__name__)

    def attack_object(self):
        """Analysi attack on enemy object."""
        self.log.info(__name__ + ': ' + 'def ' + self.attack_object.__name__ + '(): ' + self.attack_object.__doc__)

        self.base_analysis(self.p_ships, self.g_objects, self.attack_object.__name__)

    def torpedo(self):
        """Analysi torpedo attack on enemy object."""
        self.log.info(__name__ + ': ' + 'def ' + self.torpedo.__name__ + '(): ' + self.torpedo.__doc__)

        self.base_analysis(self.p_torpedos, self.g_objects, self.torpedo.__name__)

    def mine(self):
        """Analysi mine attack on enemy object."""
        self.log.info(__name__ + ': ' + 'def ' + self.mine.__name__ + '(): ' + self.mine.__doc__)

        self.base_analysis(self.p_mines, self.g_objects, self.mine.__name__)

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
            time.sleep(0.1)
        if best is not None:
            self.actions.append(best)

    def get_best_action(self):
        """Return best actions from all actions."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_best_action.__name__ + '(): ' + self.get_best_action.__doc__)

        best = self.actions[0]
        best_rate = best.rate - (best.priority * 100)
        for action in self.actions:
            rate = action.rate - (action.priority * 100)
            if rate > best_rate:
                best = action
                best_rate = rate
        return best
