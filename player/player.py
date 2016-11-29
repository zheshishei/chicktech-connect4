class Player():
    def __init__(self, piece_type):
        self.piece_type = piece_type

    def get_next_move(self, game):
        raise NotImplementedError('Player doesn\'t have a decision maker!')

    def __str__(self):
        return 'Player {0}'.format(self.piece_type)