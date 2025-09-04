"""
TODO
"""
from input_output.game_input_output import GameInputOutput
from business_logic.game import Game


def main() -> None:
    io = GameInputOutput()  # input-output layer
    game = Game(io)  # game's logic

    # the main loop
    while not game.is_finishing():
        game.run_step()

    io.show_message("Game over. Thanks for playing!")
 

if "__main__" == __name__:
    main()
