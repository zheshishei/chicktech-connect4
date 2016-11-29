"""The main entry point of the connect 4 game"""
import argparse
from random import random

from flask import Flask
from flask import request

import interface
from player.bot_player import Connect4BotPlayer
from player.user_player import Connect4Player
from player.user_player import EndGameException
from connect4 import Connect4
from connect4 import InvalidMoveError

## BEGIN PROGRAM INVOCATION INFORMATION. (FLAGS, ETC.)

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

    parser.add_argument(
        '--server',
        action='store_const',
        dest='server',
        const=True,
        default=False,
        help='Add this flag to create a pingable server',
    )
    return parser.parse_args()

## END PROGRAM INVOCATION INFORMATION

## BEGIN BOT SERVER

connect4app = Flask(__name__)

@connect4app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@connect4app.route("/")
def get_decision():
    board = request.args.board
    piece_type = request.args.piece_type
    player = Connect4BotPlayer(piece_type)

    return player.get_next_move(board)

## END BOT SERVER

def main(bot):
    """Creates the game passed in by the user and manages gameplay."""
    # create players
    piece1 = '@'
    piece2 = '#'
    player1 = Connect4Player(piece1)
    player2 = Connect4Player(piece2)
    initial_turn_order = [player1, player2]

    # create a bot player if we need to
    # randomize the ordering because it's fun
    if bot:
        player2 = Connect4BotPlayer(piece2)
        initial_turn_order = round(random()) and [player1, player2] or [player2, player1]

    # create a game
    game = Connect4.new_game(*initial_turn_order)

    # start the game
    while not game.winner:
        # go to next turn
        game = game.to_next_turn()
        current_player = game.turn_order[0]

        # show the game board
        interface.display.display_board(game)

        # get the next player's move
        while True:
            try:
                column = current_player.get_next_move(game)
                # perform the selected action
                game = game.place_piece(column)
            except EndGameException:
                return
            except InvalidMoveError as err:
                interface.display.display_error(err)
            else:
                break

    interface.display.display_board(game)

if __name__ == '__main__':
    prog_args = parse_args()

    if prog_args.server:
        connect4app.run()
    else:
        main(
            bot=prog_args.bot
        )
