"""helper functions dealing with displaying various things"""

def display_board(game):
    '''display the game on the terminal using the game class's
    own string representation'''
    print(game, flush=True)

def display_error(error):
    '''print out an error'''
    print(error, flush=True)

def display_notice(notice, no_newline=False):
    '''print out a message.
    :param no_newline: boolean if we should print a newline'''
    print(notice, flush=True, end=('' if no_newline else '\n'))
