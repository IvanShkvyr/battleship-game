"""
Handles all user interaction in the game.

This module is responsible only for input/output operations
such as printing fields, asking user input, and showing messages.
"""



class GameInputOutput:
    """
    A class responsible for interacting with the player

    This class handles all console input/output operations,
    including drawing fields, asking for input, and showing displaying messages.
    """

    def __init__(self):
        self.grid_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        self.ship_info = {
            0: ("BB", ["BB1"]),
            2: ("CA", ["CA1", "CA2"]),
            4: ("SS", ["SS1", "SS2", "SS3"]),
            6: ("PB", ["PB1", "PB2", "PB3", "PB4"]),
        }


    @staticmethod
    def ship_representation(ship_properties: dict) -> str:
        """
        Create a text representation of a ship on the board.
        Each deck of the ship is shown by a symbol:
            - "X" means the deck is destroyed or has no coodinates.
            - "O" means the deck exists and has set cooedinates.

        Parameters:
        ship_properties (dict) : A dictionary containing information about the
            ship's decks. Each deck's properties include condition.

        Returns:
        str: A string that shows the ship's condition using "X" and "O".
        """
        # Create the ship's representation
        ship = ""

        for ship_decks, deck_properties  in ship_properties.items():

            # Check if the deck is destroyed or undefined
            if deck_properties [2] == False:
                ship += "X"
            else:
                ship += "O"

        return ship


    def show_message(self, message: str) -> None:
        """
        Show a message tothe user
        """
        print(message)


    def draw_single_field(
            self,
            ships: dict,
            grid: list,
            ) -> None:
        """
        Render a single field showing player's ships and their status.

        Parameters:
        ships (dict): A dictionary with all ships and their deck statuses.
        grid (list): A 2D list (10x10) representing the player's field.
        """ 
        # Print the header of the field
        print("\n       Your field")
        print("   0 1 2 3 4 5 6 7 8 9")
        print(" +---------------------+")

        # Go through each row of the grid
        for idx, row in enumerate(grid):
            line = f"{self.grid_letters[idx]}| " + " ".join(row) + " |"
            if idx in self.ship_info:
                ship_name, keys = self.ship_info[idx]

                ship_status = " - ".join(
                    self.ship_representation(ships[k]) for k in keys
                    )
                line += f"  {ship_name} - {ship_status}"

            # Print the full line
            print(line)
        # Print the bottom border of the field
        print(" +---------------------+")


    def draw_both_fields_side_by_side(
            self,
            players_ships: dict,
            players_grid: list,
            opponents_ships: dict,
            opponents_grid: list,
            ) -> None:  
        """
        Render both player's and opponent's fields side by side.

        Parameters:
        players_ships (dict): Player's ships and their deck statuses.
        players_grid (list): 2D list (10x10) showing the player's field.
        opponents_ships (dict): Opponent's ships and their deck statuses.
        opponents_grid (list): 2D list (10x10) showing the opponent's field.
        """
        # Print the header with field labels and column numbers
        print(
            "       Your field                              "
            "                  Opponent's field"
            )
        print(
            "   0 1 2 3 4 5 6 7 8 9                         "
            "                 0 1 2 3 4 5 6 7 8 9"
            )
        print(
            " +---------------------+                       "
            "               +---------------------+"
            )

        # Loop through each row (a to j)
        for i in range(10):
            left_row = (
                f"{self.grid_letters[i]}| " + " ".join(players_grid[i]) + " |"
                )
            right_row = (
                f"{self.grid_letters[i]}| " + " ".join(opponents_grid[i]) + " |"
                )

            # If this row should show ship info (based on ship_info dict)
            if i in self.ship_info:
                ship_name, keys = self.ship_info[i]
                left_ships = " - ".join(
                    self.ship_representation(players_ships[k]) for k in keys
                    )
                right_ships = " - ".join(
                    self.ship_representation(opponents_ships[k]) for k in keys
                    )
                # Print both rows with ship info aligned
                print(
                    f"{left_row}  {ship_name} - "
                    f"{left_ships:<30}{right_row}  "
                    f"{ship_name} - {right_ships}"
                    )
            else:
                # Print both rows without ship info
                print(
                    f"{left_row}                                  "
                    f"   {right_row}"
                    )
        # Print the bottom borders for both fields
        print(
                " +---------------------+ "
                "                                   "
                "  +---------------------+"
                )


    def wait_to_start(self) -> None:
        input("Press Enter to start ...")


    def wait_to_continue(self) -> None:
        input("Press Enter to continue ...")


    def ask_ship_placement_mode(self) -> str:
        """
        Ask the player how they want toplace ships.

        Returns:
        str: "auto" if player selects automatic, "manual" if manual.
        """
        while True:
            # Ask the player to choose placement mode
            answer = input("Select ship deployment mode:\n" \
            "1 - automatic\n" \
            "2 - manual\n" \
            ">").strip()

            # Return corresponding value based on input
            if answer == "1":
                return "auto"
            elif answer == "2":
                return "manual"
            else:
                print("Incorrect choice.Try again.")


    def ask_ship_desk(
            self,
            ship_label: str,
            visual: str
            ) -> str:
        """
        Ask the player to enter the coordinates of a ship's deck.

        Parameters:
        ship_label (str): The name of the ship (e.g. "BB1").
        visual (str): A visual representation of the ship status (e.g. "OXX")

        Returns:
        str: A valid coordinate entered by player (e.g. "3A")
        """
        while True:
            # Ask the player to enter the position for the ship's deck
            player_input = input(
                f"Please put your battleship {ship_label} ({visual}): "
                ).strip().upper()

            # Check if input follows the correct format
            if (
                len(player_input) == 2
                and player_input[0] in "0123456789"
                and player_input[1] in "ABCDEFGHIJ"
                ):
                return player_input

            print("Invalid format. Example: 3A")


    def show_error(self, text: str) -> None:
        """
        Show an error message to the player.
        """
        print(text)
