"""The main entry point of the connect 4 game"""
import argparse
from random import random

# from flask import Flask
# from flask import request

import interface
from player.bot_player import Connect4BotPlayer
from player.bot_player import TicTacToeBotPlayer
from player.user_player import Connect4Player
from player.user_player import EndGameException
from player.user_player import TicTacToePlayer
from tictactoe import TicTacToe
from connect4 import Connect4
from connect4 import InvalidMoveError

## BEGIN PROGRAM INVOCATION INFORMATION. (FLAGS, ETC.)

def parse_args():
    """Program Description. User Help Manual."""
    parser = argparse.ArgumentParser(
        prog='play.py',
        description='Let\'s Play Connect4!',
    )

    parser.add_argument(
        'gametype', 
        help='"tictactoe" or "connect4". the type of game you want to play',
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

# connect4app = Flask(__name__)

# @connect4app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response

# @connect4app.route("/")
# def get_decision():
#     board = request.args.board
#     piece_type = request.args.piece_type
#     player = Connect4BotPlayer(piece_type)

#     return player.get_next_move(board)

## END BOT SERVER

def get_players_and_turn_order(game_type, bot):
    players = {
        'connect4': (('@', '#'), Connect4Player, Connect4BotPlayer),
        'tictactoe': (('X', 'O'), TicTacToePlayer, TicTacToeBotPlayer),
    }

    pieces, player, bot_player = players[game_type]

    player1 = player(pieces[0])
    player2 = player(pieces[1])
    initial_turn_order = [player1, player2]
    
    # create a bot player if we need to
    # randomize the ordering because it's fun
    if bot:
        player2 = bot_player(pieces[1])
        initial_turn_order = round(random()) and [player1, player2] or [player2, player1]
    
    return initial_turn_order


def main(game_type, bot):
    """Creates the game passed in by the user and manages gameplay."""
    game_class = {
        'connect4': Connect4,
        'tictactoe': TicTacToe,
    }

    # create players
    initial_turn_order = get_players_and_turn_order(game_type, bot)

    # create a game
    game = game_class[game_type].new_game(*initial_turn_order)

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
                next_move = current_player.get_next_move(game)
                # perform the selected action
                game = game.place_piece(*next_move)
            except EndGameException:
                return
            except InvalidMoveError as err:
                interface.display.display_error(err.message)
            else:
                break

    interface.display.display_board(game)

if __name__ == '__main__':
    prog_args = parse_args()

    if prog_args.server:
        connect4app.run()
    else:
        main(
            game_type=prog_args.gametype,
            bot=prog_args.bot
        )
