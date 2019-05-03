"""
AI module control.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""

import logging

from itertools import product

from constants import Colors

from controllers.enemy import Enemy

from objects.text import Text


class AI:
    """AI class control."""

    def __init__(self, board, speech, phrases):
        """Initialize AI control."""
        self.log = logging.getLogger()
        self.log.info(__name__ + ': ' + 'def ' + self.__init__.__name__ + '(): ' + self.__init__.__doc__)

        self.speech = speech
        self.phrases = phrases
        self.sounds = board.sounds
        self.screen = board.screen
        self.font_obj = board.font_obj

        self.text_obj = None
        self.offset = (board.screen_x // 2, board.size_font)
        self.gamer = None
        self.player = Enemy(board, speech, phrases, self)
        self.ai_step = False
        self.create_fleets = False

    def set_text(self, text):
        """Set text surface for render."""
        self.log.info(__name__ + ': ' + 'def ' + self.set_text.__name__ + '(): ' + self.set_text.__doc__)

        self.text_obj = Text(self.font_obj, text, self.offset[0], self.offset[1], Colors.BLUE)

    def draw(self):
        """Draw text surface."""
        if self.text_obj is not None:
            self.text_obj.draw(self.screen)

    def next_step(self):
        """Speak who step next."""
        self.log.info(__name__ + ': ' + 'def ' + self.next_step.__name__ + '(): ' + self.next_step.__doc__)

        self.ai_step = not self.ai_step
        if self.ai_step:
            self.set_text(self.phrases['enemy_step'])
            self.speech.speak(self.phrases['enemy_step'])
        else:
            self.set_text(self.phrases['your_step'])
            self.speech.speak(self.phrases['your_step'])

    def get_controllers(self, id_controller):
        """Return player and enemy controllers."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_controllers.__name__ + '(): ' + self.get_controllers.__doc__)

        first = self.player if id(self.player) == id_controller else self.gamer
        second = self.gamer if id(self.player) == id_controller else self.player
        return {'player': first, 'enemy': second}

    def swap(self, controllers, obj, enemy):
        """Return swap controllers, enemy, obj."""
        self.log.info(__name__ + ': ' + 'def ' + self.swap.__name__ + '(): ' + self.swap.__doc__)

        return {'player': controllers['enemy'], 'enemy': controllers['player']}, enemy, obj

    def get_enemy(self, controller, _x, _y):
        """Return enemy object arround coordinate."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_enemy.__name__ + '(): ' + self.get_enemy.__doc__)

        arround = list(product(range(_x - 1, _x + 2), range(_y - 1, _y + 2)))
        arround.remove((_x, _y))
        for cell in arround:
            enemy_obj = controller.get_obj(cell[0], cell[1])
            if enemy_obj is not None:
                return enemy_obj
        return None

    def check_battle(self, id_controller, obj):
        """Check if running battle and return true, or return false if dont find battle."""
        self.log.info(__name__ + ': ' + 'def ' + self.check_battle.__name__ + '(): ' + self.check_battle.__doc__)

        controllers = self.get_controllers(id_controller)
        if self.get_enemy(controllers['enemy'], obj.x, obj.y) is None:
            return False
        return True

    def battle(self, id_controller, obj):
        """Run battle ships."""
        self.log.info(__name__ + ': ' + 'def ' + self.battle.__name__ + '(): ' + self.battle.__doc__)

        controllers = self.get_controllers(id_controller)
        enemy = self.get_enemy(controllers['enemy'], obj.x, obj.y)
        if enemy.__class__.__name__ == 'Fort':
            self.fort_destroy(controllers, obj, enemy)
        elif obj.__class__.__name__ == 'Torpedo' or enemy.__class__.__name__ == 'Torpedo':
            self.torpedo_destroy(controllers, obj, enemy)
        elif obj.__class__.__name__ == 'Mine' or enemy.__class__.__name__ == 'Mine':
            self.mine_destroy(controllers, obj, enemy)
        else:
            self.ship_destroy(controllers, obj, enemy)

    def fort_destroy(self, controllers, obj, enemy):
        """Destroy fort enemy."""
        self.log.info(__name__ + ': ' + 'def ' + self.fort_destroy.__name__ + '(): ' + self.fort_destroy.__doc__)

        if obj.name != 'mine' and obj.name != 'torpedo':
            controllers['enemy'].forts.remove(enemy)
            self.sounds.play('art_many')
            self.speech.speak(self.get_controller_phrase(controllers['enemy']))
            self.speech.speak(self.phrases['fort_captured'])

    def torpedo_destroy(self, p_controllers, p_obj, p_enemy):
        """Destroy enemy object with torpedo."""
        self.log.info(__name__ + ': ' + 'def ' + self.torpedo_destroy.__name__ + '(): ' + self.torpedo_destroy.__doc__)

        if p_enemy.__class__.__name__ == 'Torpedo':
            controllers, obj, enemy = self.swap(p_controllers, p_obj, p_enemy)
        else:
            controllers, obj, enemy = p_controllers, p_obj, p_enemy
        if enemy.__class__.__name__ != 'Mine' and enemy.__class__.__name__ != 'Torpedo':
            self.sounds.play('boom')
            self.speech.speak(self.get_controller_phrase(controllers['player']))
            self.speech.speak(self.phrases['torpedo_destroy'])
            controllers['player'].torpedos.remove(obj)
            self.ship_remove(controllers['enemy'], enemy)

    def mine_destroy(self, p_controllers, p_obj, p_enemy):
        """Destroy enemy object with mine."""
        self.log.info(__name__ + ': ' + 'def ' + self.mine_destroy.__name__ + '(): ' + self.mine_destroy.__doc__)

        if p_enemy.__class__.__name__ == 'Mine':
            controllers, obj, enemy = self.swap(p_controllers, p_obj, p_enemy)
        else:
            controllers, obj, enemy = p_controllers, p_obj, p_enemy
        if enemy.__class__.__name__ != 'Mine' and enemy.__class__.__name__ != 'Torpedo':
            self.sounds.play('boom')
            self.speech.speak(self.get_controller_phrase(controllers['player']))
            self.speech.speak(self.phrases['mine_destroy'])
            controllers['player'].mines.remove(obj)
            if enemy.__class__.__name__ != 'Trawler':
                self.ship_remove(controllers['enemy'], enemy)

    def ship_destroy(self, controllers, obj, enemy):
        """Destroy enemy object with ship."""
        self.log.info(__name__ + ': ' + 'def ' + self.ship_destroy.__name__ + '(): ' + self.ship_destroy.__doc__)

        rate_obj = obj.rate if obj.fleet == 0 else controllers['player'].select_fleet(obj.fleet).get_ships_rate()
        rate_enemy = enemy.rate if enemy.fleet == 0 else controllers['enemy'].select_fleet(enemy.fleet).get_ships_rate()
        self.sounds.play('art')
        if rate_obj > rate_enemy:
            self.ship_remove(controllers['enemy'], enemy, True)
        elif rate_obj < rate_enemy:
            self.ship_remove(controllers['player'], obj, True)
        else:
            count_obj = 1 if obj.fleet == 0 else controllers['player'].select_fleet(obj.fleet).get_ships_count()
            count_enemy = 1 if enemy.fleet == 0 else controllers['enemy'].select_fleet(enemy.fleet).get_ships_count()
            if count_obj > count_enemy:
                self.ship_remove(controllers['enemy'], enemy, True)
            elif count_obj < count_enemy:
                self.ship_remove(controllers['player'], obj, True)
            else:
                self.ship_remove(controllers['enemy'], enemy, True)
                self.ship_remove(controllers['player'], obj, True)

    def ship_remove(self, controller, ship, fleet_remove=False):
        """Remove ship if destroy."""
        self.log.info(__name__ + ': ' + 'def ' + self.ship_remove.__name__ + '(): ' + self.ship_remove.__doc__)

        self.sounds.play('destroy')
        self.speech.speak(self.get_controller_phrase(controller))
        self.speech.speak(self.phrases['ship_destroy'].format(ship.name))
        controller.ships.remove(ship)
        fleet = None
        if ship.fleet != 0:
            fleet = controller.select_fleet(ship.fleet)
        if fleet is not None:
            fleet.ships.remove(ship)
            if fleet_remove:
                self.fleet_remove(controller, fleet)

    def fleet_remove(self, controller, fleet):
        """Remove fleet if destroy."""
        self.log.info(__name__ + ': ' + 'def ' + self.fleet_remove.__name__ + '(): ' + self.fleet_remove.__doc__)

        for f_ship in fleet.ships:
            self.sounds.play('destroy')
            self.speech.speak(self.phrases['ship_destroy'].format(f_ship.name))
            controller.ships.remove(f_ship)
            fleet.ships.remove(f_ship)
        controller.fleets.remove(fleet)

    def get_controller_phrase(self, controller):
        """Return phrase controller for get player or ai."""
        self.log.info(__name__ + ': ' + 'def ' + self.get_controller_phrase.__name__ + '(): ' + self.get_controller_phrase.__doc__)

        phrase = ''
        if id(controller) == id(self.gamer):
            phrase = self.phrases['player_controller']
        else:
            phrase = self.phrases['enemy_controller']
        return phrase
