import copy


class InvalidMoveError(Exception):
    '''Exception for an invalid move'''
    def __init__(self, message):
        self.message = message
        super().__init__()

def has_run_of_at_least_4(list_with_run, piece_type):
    '''checks whether list_with_run has a run of at least 4 of piece_type'''
    longest_run = 0
    current_run = 0
    for piece in list_with_run:
        current_run = (piece == piece_type) and (current_run + 1) or 0
        longest_run = max(longest_run, current_run)

    return longest_run >= 4

class Connect4():
    def __init__(self, board, turn_order):
        self.board = board
        self.turn_order = turn_order

    @staticmethod
    def copy_board(game):
        return [column[:] for column in game.board]

    @classmethod
    def new_game(cls, player1, player2):
        board = [[None] * 6 for i in range(7)]

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
            if has_run_of_at_least_4(column, self.turn_order[0].piece_type)
        ])

    @property
    def row_winner(self):
        board = Connect4.copy_board(self)
        rotated_board = map(list, zip(*board))

        return bool([
            row for row in rotated_board
            if has_run_of_at_least_4(row, self.turn_order[0].piece_type)
        ])

    @property
    def left_diag_winner(self):
        shifted_board = [
            ([None] * (5 - index)) + column + ([None] * index)
            for index, column in enumerate(self.board)
        ]
        rotated_board = map(list, zip(*shifted_board))

        return bool([
            diag for diag in rotated_board
            if has_run_of_at_least_4(diag, self.turn_order[0].piece_type)
        ])

    @property
    def right_diag_winner(self):
        shifted_board = [
            ([None] * index) + column + ([None] * (5 - index))
            for index, column in enumerate(self.board)
        ]
        rotated_board = map(list, zip(*shifted_board))

        return bool([
            diag for diag in rotated_board
            if has_run_of_at_least_4(diag, self.turn_order[0].piece_type)
        ])

    def place_piece(self, column):
        zero_indexed_column = column - 1
        try:
            next_available_spot = self.board[zero_indexed_column].index(None)
        except IndexError:
            raise InvalidMoveError('Sorry, column {0} is not a valid column!'.format(column))
        except ValueError:
            raise InvalidMoveError('Sorry, column {0} has no more room!'.format(column))

        board = Connect4.copy_board(self)
        board[zero_indexed_column][next_available_spot] = self.turn_order[0].piece_type

        return self.__class__(
            board=board,
            turn_order=copy.copy(self.turn_order)
        )

    def to_next_turn(self):
        board = Connect4.copy_board(self)
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
        num_cols = len(self.board)
        board = [list(row) for row in zip(*Connect4.copy_board(self))] # rotate and convert from tuples to lists
        board.reverse()
        board += [['-' for i in range(num_cols)]] # add a bottom barrier for the pieces for each column
        board += [[str(i + 1) for i in range(num_cols)]] # numbering for the columns

        board_state = '\n'.join([
            '| {0} |'.format(' | '.join([piece or ' ' for piece in row]))
            for row in board
        ])

        if self.winner:
            winner_title =  '-----------------------------\n'
            winner_title += '-  {0} is the winner!  -\n'.format(self.turn_order[0])
            winner_title += '-----------------------------\n'
        else:
            winner_title = ''
        return '{0}\n{1}\n'.format(winner_title, board_state)
