import copy


class InvalidMoveError(Exception):
    def __init__(self, message):
        self.message = message

def has_run_of_at_least_4(list, piece_type):
    longest_run = 0
    current_run = 0
    for piece in list:
        current_run = (piece == piece_type) and (current_run + 1) or 0
        longest_run = max(longest_run, current_run)
    
    return longest_run >= 4

class Connect4():
    @staticmethod
    def copy_board(game):
        return [column[:] for column in game.board]

    @classmethod    
    def new_game(cls):
        board = [
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
        ]

        return cls(
            board=board,
            turn_order=['@', '*']
        )

    def __repr__(self):
        board_repr = '\n'.join(repr(column) for column in self.board)
        return 'board:\n{0}\nturn_order:\n{1}'.format(
            board_repr,
            self.turn_order
        )

    def __str__(self):
        board = [list(row) for row in zip(*Connect4.copy_board(self))] # unpack and convert from tuples to lists
        board.reverse() # reverse the rows so we start from the top first
        board += [['-' for i in range(len(self.board))]] # add a bottom barrier for the pieces for each column
        board += [[str(i + 1) for i in range(len(self.board))]] # numbering for the columns

        board_state = '\n'.join([
            '| {0} |'.format(' | '.join([piece or ' ' for piece in row]))
            for row in board
        ])

        if self.winner:
            winner_title =  '-----------------------------\n'
            winner_title += '-     Player {0} has won!     -\n'.format(self.turn_order[0])
            winner_title += '-----------------------------\n'
        else:
            winner_title = ''
        return '{0}\n{1}\n'.format(winner_title, board_state)

    def __init__(self, board, turn_order):
        self.board = board
        self.turn_order = turn_order

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
            if has_run_of_at_least_4(column, self.turn_order[0])
        ])

    @property
    def row_winner(self):
        board = Connect4.copy_board(self)
        rotated_board = [list(row) for row in zip(*board)]

        return bool([
            row for row in rotated_board
            if has_run_of_at_least_4(row, self.turn_order[0])
        ])

    @property
    def left_diag_winner(self):
        shifted_board = [
            [None for i in range(5 - index)] + column + [None for i in range(index)]
            for index, column in enumerate(self.board)
        ]
        rotated_board = [list(row) for row in zip(*shifted_board)]

        return bool([
            diag for diag in rotated_board
            if has_run_of_at_least_4(diag, self.turn_order[0])
        ])

    @property
    def right_diag_winner(self):
        shifted_board = [
            [None for i in range(index)] + column + [None for i in range(5 - index)]
            for index, column in enumerate(self.board)
        ]
        rotated_board = [list(row) for row in zip(*shifted_board)]

        return bool([
            diag for diag in rotated_board
            if has_run_of_at_least_4(diag, self.turn_order[0])
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
        board[zero_indexed_column][next_available_spot] = self.turn_order[0]

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
