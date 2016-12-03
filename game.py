class InvalidMoveError(Exception):
    '''Exception for an invalid move'''
    def __init__(self, message):
        self.message = message
        super().__init__()
