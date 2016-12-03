import copy
from game import InvalidMoveError


def is_all_of_piece(piece1, piece2, piece3, type):
    return piece1 == type and piece2 == type and piece3 == type


class TicTacToe():
    def __init__(self, board, turn_order):
        self.board = board
        self.turn_order = turn_order

    @staticmethod
    def copy_board(game):
        return [column[:] for column in game.board]

    @classmethod
    def new_game(cls, player1, player2):
        board = [[None] * 3 for i in range(3)]

        return cls(
            board=board,
            turn_order=[player1, player2]
        )

    @property
    def winner(self):
        """Checks whether the current turn's player has won"""
        return (
            self.column_winner or
            self.row_winner or
            self.left_diag_winner or
            self.right_diag_winner
        )

    @property
    def column_winner(self):
        return bool([
            column for column in self.board
            if is_all_of_piece(*column, self.turn_order[0].piece_type)
        ])

    @property
    def row_winner(self):
        rotated_board = map(list, zip(*self.board))

        return bool([
            row for row in rotated_board
            if is_all_of_piece(*row, self.turn_order[0].piece_type)
        ])

    @property
    def left_diag_winner(self):
        return is_all_of_piece(
            self.board[0][0], 
            self.board[1][1], 
            self.board[2][2], 
            self.turn_order[0].piece_type
        )

    @property
    def right_diag_winner(self):
        return is_all_of_piece(
            self.board[0][2], 
            self.board[1][1], 
            self.board[2][0], 
            self.turn_order[0].piece_type
        )

    def place_piece(self, column, row):
        column_map = {
            'A': 0,
            'B': 1,
            'C': 2,
        }
        zero_indexed_row = row - 1

        try:
            zero_indexed_column = column_map[column]
        except KeyError:
            raise InvalidMoveError('Sorry, column {0} is not a valid column!'.format(column))

        board = TicTacToe.copy_board(self)

        if board[zero_indexed_row][zero_indexed_column]:
            raise InvalidMoveError('Sorry, Spot {0}{1} is already taken!'.format(column, row))

        board[zero_indexed_row][zero_indexed_column] = self.turn_order[0].piece_type

        return self.__class__(
            board=board,
            turn_order=copy.copy(self.turn_order)
        )

    def to_next_turn(self):
        board = TicTacToe.copy_board(self)
        turn_order = self.turn_order[1:] + self.turn_order[:1]
        return self.__class__(
            board=board,
            turn_order=turn_order,
        )

    def __repr__(self):
        board_repr = '\n'.join(repr(column) for column in self.board)
        return 'board:\n{0}\nturn_order:\n{1}'.format(
            board_repr,
            self.turn_order
        )

    def __str__(self):
        board = [
            ' | A | B | C |',
            '-+---+---+---+',
            '1| {0} | {1} | {2} |'.format(*[x or ' ' for x in self.board[0]]),
            '-+---+---+---+',
            '2| {0} | {1} | {2} |'.format(*[x or ' ' for x in self.board[1]]),
            '-+---+---+---+',
            '3| {0} | {1} | {2} |'.format(*[x or ' ' for x in self.board[2]]),
            '-+---+---+---+',
        ]

        board_state = '\n'.join(board)

        if self.winner:
            winner_title =  '-----------------------------\n'
            winner_title += '-  {0} is the winner!  -\n'.format(self.turn_order[0])
            winner_title += '-----------------------------\n'
        else:
            winner_title = ''
        return '{0}\n{1}\n'.format(winner_title, board_state)
