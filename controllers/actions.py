"""
Extended module for behaviors.

Created on 11.03.2019

@author: Ruslan Dolovanyuk

"""

from collections import namedtuple

from controllers.base import diff2list


Coordinate = namedtuple('Coordinate', ['x', 'y'])


class Naming:
    """Set global variables."""

    tactics = ('attack_fort', 'attack_object', 'defence', 'torpedo', 'mine')


class Action:
    """Action state in object view."""

    def __init__(self, obj, coord, priority, rate):
        """Initialise action state."""
        self.object = obj
        self.coordinate = coord
        self.priority = priority
        self.rate = rate


class Analysis:
    """Find best tactic for ai game."""

    def __init__(self, player, enemy):
        """Initialise analysis class."""
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
        self.p_mines.clear()
        self.p_torpedos.clear()
        self.p_ships.clear()
        self.actions.clear()

    def run(self):
        """Run analysis tactics."""
        for obj in self.p_objects:
            if obj.__class__.__name__ == 'Mine':
                self.p_mines.append(obj)
            elif obj.__class__.__name__ == 'Torpedo':
                self.p_torpedos.append(obj)
            else:
                self.p_ships.append(obj)

        for name in Naming.tactics:
            getattr(self, name)()

        self.select_best_action()
        self.clear()

    def attack_fort(self):
        """Analysi attack on enemy fort."""
        pass

    def attack_object(self):
        """Analysi attack on enemy object."""
        pass

    def defence(self):
        """Analysi needed defence ai fort."""
        pass

    def torpedo(self):
        """Analysi torpedo attack on enemy object."""
        self.base_analysis(self.p_torpedos, self.g_objects, 3)

    def mine(self):
        """Analysi mine attack on enemy object."""
        self.base_analysis(self.p_mines, self.g_objects, 4)

    def base_analysis(self, player_objects, enemy_objects, prior):
        """Base analysis tactic for battle."""
        best = None
        rate = 0
        for obj in player_objects:
            routes = self.get_routes(obj, enemy_objects)
            for route in routes:
                empty = True
                for coord in route:
                    if self.player.get_object(coord.x, coord.y) is not None or self.enemy.get_object(coord.x, coord.y) is not None:
                        empty = False
                        break
                if empty:
                    temp_rate = 1000 - len(route) * 100
                    if temp_rate > rate:
                        rate = temp_rate
                        best = Action(obj, route[0], prior, rate)
        if best is not None:
            self.actions.append(best)

    def get_routes(self, obj, enemy_list):
        """Return routes from ai object to enemy objects."""
        routes = []
        for enemy in enemy_list:
            route = []
            diff_x = diff2list(enemy.x - 1 - obj.x)
            diff_y = diff2list(enemy.y - 1 - obj.y)
            self.add_coordinates(diff_x, diff_y)
            for index, _ in enumerate(diff_x):
                route.append(Coordinate(diff_x[index], diff_y[index]))
            routes.append(route)
        return routes

    @classmethod
    def add_coordinates(cls, diff_x, diff_y):
        """Add coordinates for equel lists."""
        if len(diff_x) > len(diff_y):
            main = diff_x
            sub = diff_y
        else:
            main = diff_y
            sub = diff_x
        for _ in range(len(main) - len(sub)):
            sub.append(0)

    def select_best_action(self):
        """Select best actions from all actions."""
        pass

    def get_best_action(self):
        """Return best result analysis."""
        pass
