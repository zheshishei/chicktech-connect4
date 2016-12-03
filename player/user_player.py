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
                return (int(column),)
            except ValueError: # error handle for non-int values and continue the loop
                interface.display.display_error('"{0}" is not a valid column!'.format(column))

class TicTacToePlayer(Player):

    def get_next_move(self, game):
        while True:
            # get the user action
            space = interface.input.user_input(
                prompt='({0}) What space do you want to move to next (e.g. A1)? '.format(self)
            )
            # if the user wants out, then out we go
            if space == 'end' or space == 'exit':
                raise EndGameException

            if len(space) != 2:
                interface.display.display_error('"{0}" is not a move!'.format(space))
                continue
                
            column = space[0].upper()
            row = space[1]

            if column not in ('A', 'B', 'C'):
                interface.display.display_error('"{0}" is not a valid column!'.format(column))
                continue

            try:
                row = int(row)
                if not 0 < row < 4:
                    raise ValueError

                return column, row
            except ValueError: # error handle for non-int values and continue the loop
                interface.display.display_error('"{0}" is not a valid row!'.format(row))
