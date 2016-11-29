import interface.input

from player.player import Player


class EndGameException(Exception):
    pass

class Connect4Player(Player): # pylint: disable=too-few-public-methods

    def get_next_move(self, game):
        while True:
            # get the user action
            column = interface.input.user_input(
                prompt='({0}) Which column will you place your piece? '.format(self)
            )

            # if the user wants out, then out we go
            if column == 'end' or column == 'exit':
                raise EndGameException

            try:
                return int(column)
            except ValueError: # error handle for non-int values and continue the loop
                interface.display.display_error('"{0}" is not a valid column!'.format(column))
