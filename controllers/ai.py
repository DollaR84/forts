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

    def check_battle(self, id_controller, obj):
        """Check if running battle and return true, or return false if dont find battle."""
        controllers = self.get_controllers(id_controller)
        if self.get_enemy(controllers['enemy'], obj.x, obj.y) is None:
            return False
        return True

    def get_enemy(self, controller, _x, _y):
        """Return enemy object arround coordinate."""
        arround = list(product(range(_x - 1, _x + 2), range(_y - 1, _y + 2)))
        arround.remove((_x, _y))
        for cell in arround:
            enemy_obj = controller.get_obj(cell[0], cell[1])
            if enemy_obj is not None:
                return enemy_obj
        return None

    def get_controllers(self, id_controller):
        """Return player and enemy controllers."""
        first = self.player if id(self.player) == id_controller else self.gamer
        second = self.gamer if id(self.gamer) == id_controller else self.player
        return {'player': first, 'enemy': second}

    def battle(self, id_controller, obj):
        """Run battle ships."""
        controllers = self.get_controllers(id_controller)
        enemy = self.get_enemy(controllers['enemy'], obj.x, obj.y)
