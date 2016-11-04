import argparse

from connect4 import Connect4
from connect4 import InvalidMoveError
import interface

class EndGameException(Exception):
    pass

def parse_args():
    """Program Description. User Help Manual."""
    parser = argparse.ArgumentParser(
        prog='game',
        description='Let\'s Play Connect4!',
    )

    parser.add_argument(
        '--bot', 
        action='store_const',
        dest='bot', 
        const=True, 
        default=False,
        help='Add this flag to play against a bot',
    )
    
    return parser.parse_args()


def get_user_move(player_name):
    while True:
        # get the user action
        column = interface.get_input(
            prompt='({0}) Which column will you place your piece? '.format(player_name)
        )

        # if the user wants out, then out we go
        if column == 'end' or column == 'exit':
            raise EndGameException

        try:
            return int(column)
        except ValueError:
            interface.display_error('"{0}" is not a valid column!'.format(column))


def main(bot):
    """Creates the game passed in by the user and manages gameplay."""
    game = Connect4.new_game()

    exit = False
    while not game.winner and not exit:
        # go to next turn
        game = game.to_next_turn()

        # show the game board
        interface.display(game)
        while True:
            try:
                column = get_user_move('Player {0}'.format(game.turn_order[0]))
                # perform the selected action
                game = game.place_piece(column)
            except EndGameException:
                return
            except InvalidMoveError as err:
                interface.display_error(err)
            else:
                break

    if game.winner:
        interface.display(game)

if __name__ == '__main__':
    args = parse_args()
    main(
        bot=args.bot
    )