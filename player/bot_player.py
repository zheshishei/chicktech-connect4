import time
from random import random

import interface.display
from player.player import Player


class Connect4BotPlayer(Player):
    def get_next_move(self, game):
        '''called to get the next move for a given game board'''
        interface.display.display_notice(
            '({0}) Bot is making a choice...'.format(self),
            no_newline=True,
        )
        time.sleep(.5 + round(1.5 * random(), 1))

        decided_move = self._decide_move(game)
        interface.display.display_notice('{0}'.format(decided_move))
        time.sleep(.5)

        return decided_move

    def _decide_move(self, game):
        return 1
