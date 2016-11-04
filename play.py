from connect4 import Connect4
from connect4 import InvalidMoveError
import interface

def main():
    """Creates the game passed in by the user and manages gameplay."""
    game = Connect4.new_game()

    exit = False
    while not game.winner and not exit:
        game = game.to_next_turn()
        # show the game board
        interface.display(game)

        performed_move = False
        while not performed_move:
            # get the user action
            column = interface.get_input(
                prompt='(Player {0}) Which column will you place your piece? '.format(game.turn_order[0])
            )

            # check to see if the player wants to exit
            if column == 'end' or column == 'exit':
                exit = True
                break

            try:
                # perform the selected action
                game = game.place_piece(int(column))
            except (ValueError, InvalidMoveError) as err:
                interface.display_error(err)
            else:
                performed_move = True

    if game.winner:
        interface.display(game)

if __name__ == '__main__':
    main()