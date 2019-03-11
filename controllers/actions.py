"""
Extended module for behaviors.

Created on 11.03.2019

@author: Ruslan Dolovanyuk

"""


class Naming:
    """Set global variables."""

    tactics = ('attack_fort', 'attack_object', 'defence', 'mine', 'torpedo')


class Action:
    """Action state in object view."""

    def __init__(self, obj, x, y, priority, rate):
        """Initialise action state."""
        self.object = obj
        self.x = x
        self.y = y
        self.priority = priority
        self.rate = rate


class Analysis:
    """Find best tactic for ai game."""

    def __init__(self):
        """Initialise analysis class."""
        self.field = None
        self.p_mines = None
        self.p_torpedos = None
        self.p_ships = None
        self.p_forts = None
        self.p_objects = None
        self.g_forts = None
        self.g_objects = None

        self.actions = []
        self.best = None

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
        """Analysis attack on enemy fort."""
        pass

    def attack_object(self):
        """Analysis attack on enemy object."""
        pass

    def defence(self):
        """Analysis needed defence ai fort."""
        pass

    def mine(self):
        """Analysis mine attack on enemy object."""
        pass

    def torpedo(self):
        """Analysis torpedo attack on enemy object."""
        pass

    def select_best_action(self):
        """Select best actions from all actions."""
        pass

    def get_best_action(self):
        """Return best result analysis."""
        pass
