"""
AI module control.

Created on 17.12.2018

@author: Ruslan Dolovanyuk

"""

from itertools import product

from constants import Colors

from controllers.enemy import Enemy

from objects.text import Text


class AI:
    """AI class control."""

    def __init__(self, board, speech, phrases):
        """Initialize AI control."""
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
        self.text_obj = Text(self.font_obj, text, self.offset[0], self.offset[1], Colors.BLUE)

    def draw(self):
        """Draw text surface."""
        if self.text_obj is not None:
            self.text_obj.draw(self.screen)

    def next_step(self):
        """Speak who step next."""
        self.ai_step = not self.ai_step
        if self.ai_step:
            self.set_text(self.phrases['enemy_step'])
            self.speech.speak(self.phrases['enemy_step'])
        else:
            self.set_text(self.phrases['your_step'])
            self.speech.speak(self.phrases['your_step'])

    def get_controllers(self, id_controller):
        """Return player and enemy controllers."""
        first = self.player if id(self.player) == id_controller else self.gamer
        second = self.gamer if id(self.player) == id_controller else self.player
        return {'player': first, 'enemy': second}

    @classmethod
    def swap(cls, controllers, obj, enemy):
        """Return swap controllers, enemy, obj."""
        return {'player': controllers['enemy'], 'enemy': controllers['player']}, enemy, obj

    @classmethod
    def get_enemy(cls, controller, _x, _y):
        """Return enemy object arround coordinate."""
        arround = list(product(range(_x - 1, _x + 2), range(_y - 1, _y + 2)))
        arround.remove((_x, _y))
        for cell in arround:
            enemy_obj = controller.get_obj(cell[0], cell[1])
            if enemy_obj is not None:
                return enemy_obj
        return None

    def check_battle(self, id_controller, obj):
        """Check if running battle and return true, or return false if dont find battle."""
        controllers = self.get_controllers(id_controller)
        if self.get_enemy(controllers['enemy'], obj.x, obj.y) is None:
            return False
        return True

    def battle(self, id_controller, obj):
        """Run battle ships."""
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
        if obj.name != 'mine' and obj.name != 'torpedo':
            controllers['enemy'].forts.remove(enemy)
            self.sounds.play('art_many')
            self.speech.speak(self.phrases['fort_captured'])

    def torpedo_destroy(self, controllers, obj, enemy):
        """Destroy enemy object with torpedo."""
        if enemy.__class__.__name__ == 'Torpedo':
            controllers, obj, enemy = self.swap(controllers, obj, enemy)
        if enemy.__class__.__name__ != 'Mine' and enemy.__class__.__name__ != 'Torpedo':
            self.sounds.play('boom')
            controllers['player'].torpedos.remove(obj)
            controllers['enemy'].ships.remove(enemy)
            self.sounds.play('destroy')
            if enemy.fleet != 0:
                fleet = controllers['enemy'].select_fleet(enemy.fleet)
                if fleet is not None:
                    fleet.remove(enemy)
            self.speech.speak(self.phrases['ship_destroy'].format(enemy.name))

    def mine_destroy(self, controllers, obj, enemy):
        """Destroy enemy object with mine."""
        if enemy.__class__.__name__ == 'Mine':
            controllers, obj, enemy = self.swap(controllers, obj, enemy)
        if enemy.__class__.__name__ != 'Mine' and enemy.__class__.__name__ != 'Torpedo':
            self.sounds.play('boom')
            controllers['player'].mines.remove(obj)
            if enemy.__class__.__name__ == 'Trawler':
                self.speech.speak(self.phrases['mine_destroy'])
            else:
                controllers['enemy'].ships.remove(enemy)
                self.sounds.play('destroy')
                if enemy.fleet != 0:
                    fleet = controllers['enemy'].select_fleet(enemy.fleet)
                    if fleet is not None:
                        fleet.remove(enemy)
                self.speech.speak(self.phrases['ship_destroy'].format(enemy.name))

    def ship_destroy(self, controllers, obj, enemy):
        """Destroy enemy object with ship."""
        rate_obj = obj.rate if obj.fleet == 0 else controllers['player'].select_fleet(obj.fleet).get_ships_rate()
        rate_enemy = enemy.rate if enemy.fleet == 0 else controllers['enemy'].select_fleet(enemy.fleet).get_ships_rate()
        self.sounds.play('art')
        if rate_obj > rate_enemy:
            self.ship_remove(controllers['enemy'], enemy)
        elif rate_obj < rate_enemy:
            self.ship_remove(controllers['player'], obj)
        else:
            count_obj = 1 if obj.fleet == 0 else controllers['player'].select_fleet(obj.fleet).get_ships_count()
            count_enemy = 1 if enemy.fleet == 0 else controllers['enemy'].select_fleet(enemy.fleet).get_ships_count()
            if count_obj > count_enemy:
                self.ship_remove(controllers['enemy'], enemy)
            elif count_obj < count_enemy:
                self.ship_remove(controllers['player'], obj)
            else:
                self.ship_remove(controllers['enemy'], enemy)
                self.ship_remove(controllers['player'], obj)

    def ship_remove(self, controller, ship):
        """Remove ship and fleet if destroy."""
        fleet = None
        if ship.fleet != 0:
            fleet = controller.select_fleet(ship.fleet)
        self.sounds.play('destroy')
        self.speech.speak(self.phrases['ship_destroy'].format(ship.name))
        controller.ships.remove(ship)
        if fleet is not None:
            fleet.ships.remove(ship)
            for f_ship in fleet.ships:
                self.sounds.play('destroy')
                self.speech.speak(self.phrases['ship_destroy'].format(f_ship.name))
                controller.ships.remove(f_ship)
                fleet.ships.remove(f_ship)
            controller.fleets.remove(fleet)
