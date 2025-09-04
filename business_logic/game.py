"""
Game module.

This module implements the core logic and structure of a Battleship game,
including:

- Board representation and ship placement (both automatic and manual).
- Ship validation rules such as adjacency and straight line placement.
- Game state management using a finite state machine pattern.
- States include: not started, setup ships, playing, and finished.
- Interaction with user input/output is abstracted via GameInputOutput
    interface.

Classes:
- Board: manages the game board, ships, and their positions.
- GameState (abstract): base class for game states.
- NotStartState, SetupShipsState, PlayingState, FinishedState: concrete game
    states.
- Game: main game controller, holds the state machine and boards.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import random

from input_output.game_input_output import GameInputOutput


GRID_NUMBERS = [str(i) for i in range(10)]
GRID_LETTERS = [chr(ord("A") + i) for i in range(10)]

# Format: "ship name" : number of decks
SHIPS_INFO = {
    "BB1": 4,
    "CA1": 3,
    "CA2": 3,
    "SS1": 2,
    "SS2": 2,
    "SS3": 2,
    "PB1": 1,
    "PB2": 1,
    "PB3": 1,
    "PB4": 1,
}



class Board:
    """
    A class representing a 10x10 game board for the Battleship game.

    This board handles:
    - Storing and visualizing ship positions.
    - Validating ship placement (manual or automatic).
    - Marking hits and misses.
    - Checking surrounding cells and ensuring no ships touch each other.
    """

    def __init__(self, ships_info: dict):
        self.grid = [["~" for _ in range(10)] for _ in range(10)]
        self.ships = {
            name: {i: [False, False, False] for i in range(1, decks+1)}
                      for name, decks in ships_info.items()
                      }
        self.shots = set()


    @staticmethod
    def get_ship_visual(ship_properties: dict, ship_decks: int) -> str:
        """
        Creates a ship visualization by displaying its decks as a string.
        The following symbols are used:
        - "_" - an unfilled position;
        - "?" - the current deck being input;
        - "X" - a deck whose coordinates have already been entered.

        Parameters:
        ship_properties (dict): A dictionary containing the ship's properties.
        The number of keys determines the ship's length.
        ship_decks (int): The index of the deck currently being entered.

        Returns:
        str: A string representing the ship's current input status.
        For example: 
            "X?_" — the first deck has been entered, the second deck is being
            entered, and the third deck hasn't been entered yet.
        """
        ship_length = len(ship_properties)

        # Create the initial ship template: all positions are unfilled "_"
        ship_visual = ["_"] * ship_length

        # Replace the current deck with "?"
        ship_visual[ship_decks - 1] = "?"

        # Replace all already entered decks with "X"
        if ship_decks != 1:
            for i, _ in enumerate(ship_visual[:ship_decks-1]):
                ship_visual[i] = "X"

        # Convert the list of symbols into a string
        ship_visual = "".join(ship_visual)

        return ship_visual


    @staticmethod
    def get_surrounding_cells(ship: list[str]) -> list[str]:
        """
        Get all the cells surrounding the ship, including diagonals.

        Parameters:
        ship (list[str]): A list of coordinates representing the ship's
        position on the board.

        Returns:
        list[str] - A list of coordinates of the cells around the ship.
        """
        surrounding_cells = []

        # Loop through each deck of the ship
        for coord_cell in ship:
            # Loop through all 3x3 positions around the deck 
            for i in range(-1,2):
                for j in range(-1,2):

                    # Get the row and column index of the current deck
                    coord_row = GRID_LETTERS.index(coord_cell[1])
                    coord_col = GRID_NUMBERS.index(str(coord_cell[0]))

                    new_coord_row = coord_row + i
                    new_coord_col = coord_col + j

                    # Check if the new coordinates are within the field limits
                    if not (
                        0 <= new_coord_row < 10 and 0 <= new_coord_col < 10
                        ):
                        continue

                    # Convert the new coordinates back to our coordinate format
                    new_coord = GRID_NUMBERS[
                        new_coord_col
                        ] + GRID_LETTERS[
                            new_coord_row
                            ]

                    # Add the coordinate if it's not already in the list
                    if new_coord not in surrounding_cells:
                        surrounding_cells.append(new_coord)
        return surrounding_cells


    @staticmethod
    def is_adjacent_coordinates(ship_coords: list[str], new_coord: str) -> bool:
        """
        Checks if the given coordinate is adjacent to the last entered one.

        Parameters:
        ship_coords (list[str]): A list of existing coordinates of the
        ship's decks.
        new_coord (str): The new coordinate to check.

        Returns:
        bool: True if the new coordinate is adjacent to the last entered one,
        False otherwise.
        """
        # If there are no coordinates yet, the first coordinate is always valid
        if not ship_coords:
            return True 
        
        # Get the last coordinate of the ship and the new coordinate
        last_col, last_row = ship_coords[-1]
        new_col, new_row = new_coord

        # Get index positions of columns and rows
        idx_last_col = GRID_NUMBERS.index(last_col)
        idx_last_row = GRID_LETTERS.index(last_row)
        idx_new_col = GRID_NUMBERS.index(new_col)
        idx_new_row = GRID_LETTERS.index(new_row)

        # Check if the cells are adjacent
        if (
            abs(idx_last_col - idx_new_col)
            + abs(idx_last_row - idx_new_row)
            == 1
            ):
            return True
        else:
            return False


    @staticmethod
    def is_ship_in_straight_line(ship: list[str], new_coord: str) -> bool:
        """
        Check if the new coordinate keeps the ship in a straight line.

        Parameters:
        ship_coords (list[str]): A list of already placed coordinates.
        new_coord (str): The new coordinate to check.

        Returns:
        bool: True if all coordinates (existing and new) form a straight line
        (horizontal or vertical). False otherwise.
        """
        # If there are no coordinates yet, the first coordinate is always valid
        if not ship:
            return True

        # Get the sets of column and row coordinates
        col_sets = {c[0] for c in ship} | {new_coord[0]}
        row_sets = {c[1] for c in ship} | {new_coord[1]}
        
        # Check if the ship coordinates form a straight line
        if (
            len(col_sets) == 1 and len(row_sets) != 1
            ) or (
                len(col_sets) != 1 and len(row_sets) == 1
                ):
            return True

        return False
    

    def is_occupied(self, coord: str) -> bool:
        """
        Check if a cell is already occupied by any ship.

        Parameters:
        coord (str): The new coordinate to check.

        Returns:
        bool: True if the coordinate is already occupied by a ship deck,
            False otherwise.
        """
         # Loop through all ships and their decks
        for ship_data in self.ships.values():
            for deck_data in ship_data.values():
                col, row, placed = deck_data
                if placed and coord == f"{col}{row}":
                    return True

        return False


    def can_place_ship(
                    self,
                    coords: list[str],
                    all_surrounding: set[str]
                    ) -> bool:
        """
        Check if a ship can be placed at the given coordinates.
        This function is mainly used during automatic ship placement.

        Parameters:
        coords (list[str]): A list of coordinates where the ship is going
        to be placed.
        all_surrounding (set[str]): A set of all cells that surround existing
        ships.

        Returns:
        bool: True if the ship can be placed, False otherwise.
        """
        for cell in coords:
            # Check that each cell is valid and inside the grid
            if (
                len(cell) != 2
                or cell[0] not in GRID_NUMBERS
                or cell[1] not in GRID_LETTERS
                ):
                return False
        
        # Check that this cell does not touch another ship
        for cell in coords:
            if cell in all_surrounding:
                return False

        return True


    def add_deck_to_ship(self, ship_name: str, deck: int, coords: str) -> None:
        """
        Save the given coordinates for a ship's deck and mark it as placed.

        Parameters:
        ship_name (str): The name of the ship (e.g. "BB1", "SS3").
        deck (int): The index/key of the deck in the ship's dictionary.
        coords (str): The coordinate where the deck is placed (e.g. "3A").
        """
        self.ships[ship_name][deck] = [int(coords[0]), coords[1], True]


    def add_desk_to_grid(self) -> None:
        """
        Update the game field (self.grid) with ship positions.
        """
        # Clear old ship visuals from the grid (reset "O" and "X" to water)
        for r in range(10):
            for c in range(10):
                if self.grid[r][c] in ("O", "X"):
                    self.grid[r][c] = "~"

        # Loop through all ships and their decks
        for ship_type, ship_properties in self.ships.items():
            for ship_decks, desk_properties in ship_properties.items():

                # Skip if there is no deck information available
                if desk_properties[1] == False:
                    continue

                # Convert row (A–J) and column (0–9) to grid indices
                row = GRID_LETTERS.index(desk_properties[1])  
                col = GRID_NUMBERS.index(str(desk_properties[0]))

                # Mark the cell on the grid
                self.grid[row][col] = "O" if desk_properties[2] else "X"  


    def place_ships_automatically(self) -> None:
        """
        Automatically place all ships on the grid.
        """
        occupied_surrounding  = set()

        # Try to place each ship from the list
        for ship, length in SHIPS_INFO.items():
            while True:
                # Choose random orientation and starting point
                orient = random.choice(["horizontal", "vertical"])
                start_coord = (
                    random.choice(GRID_NUMBERS) + random.choice(GRID_LETTERS)
                    )

                # Try to generate full list of coordinates for the ship
                coords = self._make_ship_coords(orient, start_coord, length)

                # Skip if ship doesn't fit or overlaps other ships
                if coords is None:
                    continue
                if not self.can_place_ship(coords, occupied_surrounding):
                    continue

                # Update the list of surrounding cells
                occupied_surrounding |= set(self.get_surrounding_cells(coords))

                # Add each deck to the ship and update the field
                for index, coord in enumerate(coords):
                    self.add_deck_to_ship(
                                        ship_name=ship,
                                        deck=index+1,
                                        coords=coord
                                        )
                # Update the visual grid after placing each ship
                self.add_desk_to_grid()
                break


    def _make_ship_coords(
                        self,
                        orientation: str,
                        coord: str,
                        length: int
                        ) -> list[str] | None:
        """
        Generate a list of coordinates for a ship based on start position
        and orientation.

        This function computes a list of coordinates based on the provided
        starting coordinate, ship length, and orientation.

        Parameters:
        orientation (str): "horizontal" or "vertical" — defines how the ship
        will be placed.
        coord (str): The starting coordinate of the ship (e.g. "3A").
        length (int): The number of cells the ship should occupy.

        Returns: 
        list[str] | None: A list of coordinates if the ship fits inside
        the field. Returns None if the ship would go out of bounds.
        """
        # Get the starting column and row index
        c, r = GRID_NUMBERS.index(coord[0]), GRID_LETTERS.index(coord[1])
        new_ship = []

        # Try horizontal placement
        if orientation == "horizontal":
            # Check if the ship would go outside the right border
            if c + length -1 >= 10:
                return None

            for i in range(length):
                new_ship.append(GRID_NUMBERS[c + i] + GRID_LETTERS[r])
        # Try vertical placement
        else:
            # Check if the ship would go outside the bottom border
            if r + length - 1 >= 10:
                return None

            for i in range(length):
                new_ship.append(GRID_NUMBERS[c] + GRID_LETTERS[r + i])
        return new_ship



class GameState(ABC):
    """
    Abstract base class representing a game state in the finite state machine.

    This class defines the structure for all concrete game states. Each state
    must implement the handle() method, which contains the logic to execute
    when the game is in that state.
    """

    def __init__(self, game: Game):
        self.game = game
        self.io = game.io


    @abstractmethod
    def handle(self) -> None:
        """
        Execute the logic specific to the current game state.
        """
        pass



class NotStartState(GameState):
    """
    This is the first state of the game.

    It shows a message that the game did not start yet.
    It waits for the player to press Enter.
    Then it changes the game to the next state: setting up ships.
    """

    def handle(self) -> None:
        """
        Handle what happens in the start state.
        """
        self.io.show_message("The game hasn't started yet.")
        self.io.wait_to_start()
        self.game.set_state(SetupShipsState(self.game))


class SetupShipsState(GameState):
    """
    This state is for placing ships on the field.

    The player can choose between automatic or manual ship placement.
    Then the opponent’s ships are placed automatically.
    After that, the game moves to the playing state.
    """

    def handle(self) -> None:
        """
        Handle ship placement for both the player and the opponent.
        """
        self.io.show_message("Ship deployment mode.")

        # Ask the player how they want to place their ships
        placement_mode = self.io.ask_ship_placement_mode()

        if placement_mode == "auto":
            # If player chooses automatic placement, do it
            self.game.player_board.place_ships_automatically()
        else:
            # If player chooses manual placement
            all_surrounding = set()
            for ship_name, ship_size in self.game.player_board.ships.items():
                self.place_ships_manually(
                                        ship_name,
                                        ship_size,
                                        all_surrounding
                                        )
        
        self.io.draw_single_field(
                        ships=self.game.player_board.ships,
                        grid=self.game.player_board.grid
                        )

        # Automatically place the opponent's ships
        self.game.opp_board.place_ships_automatically()

        # Show both fields side by side (player's and opponent's)
        self.io.draw_both_fields_side_by_side(
            players_ships=self.game.player_board.ships,
            players_grid=self.game.player_board.grid,
            opponents_ships=self.game.opp_board.ships,
            opponents_grid=self.game.opp_board.grid,
        )

        self.io.wait_to_continue()

        # Move to the playing state (start the game)
        self.game.set_state(PlayingState(self.game))

    
    def place_ships_manually(
            self,
            ship_name: str,
            ship_info: dict,
            all_surrounding: set[str],
            ) -> None:
        """
        Place a ship manually by asking the user to enter coordinates.

        Parameters:
        ship_name (str): The name of the ship to place (e.g. "BB1").
        ship_info (dict): A dictionary with the ship’s deck data.
        all_surrounding (set[str]): A set of coordinates that are next to
        other ships and should be avoided.

        Returns:
        None
        """
        self.io.show_message(
                        f"Placing ship {ship_name} of size {len(ship_info)}."
                        )

        current_ship = []

        # Loop until all decks of the ship have coordinates
        while len(current_ship) < len(ship_info):

            # Get a visual representation of the ship's progress
            visua = self.game.player_board.get_ship_visual(
                                                            ship_info,
                                                            len(current_ship)+1
                                                            )

            # Ask the player to enter the coordinate for the next deck
            coord = self.io.ask_ship_desk(ship_name, visua)

            try:
                # Check 0: Is the cell already occupied by another ship?
                if self.game.player_board.is_occupied(coord):
                    self.io.show_error(
                        "This cell is already occupied by another ship."
                        )
                    continue

                # Check 1: Has this coordinate already been added?
                if coord in current_ship:
                    self.io.show_error(
                        "This desk was already added for this ship"
                        )
                    continue

                # Check 2: Are the coordinates adjacent?
                if (
                    current_ship and not
                    self.game.player_board.is_adjacent_coordinates(
                        current_ship,
                        coord
                        )
                    ):
                    self.io.show_error("Coordinates must be adjacent.")
                    continue

                # Check 3: Are the decks in a straight line?
                if (
                    len(current_ship) >= 2 and not
                    self.game.player_board.is_ship_in_straight_line(
                        current_ship,
                        coord
                        )
                    ):
                    self.io.show_error("Ship must be in a straight line.")
                    continue

                # Check 4: Is the coordinate too close to other ships?
                if coord in all_surrounding:
                    self.io.show_error("Cell too close to another ship.")
                    continue

                # Add the valid coordinate to the current ship's deck list
                current_ship.append(coord)

                # Register the deck position on the player's board
                self.game.player_board.add_deck_to_ship(
                                                    ship_name=ship_name,
                                                    deck=len(current_ship),
                                                    coords=coord
                                                    )

                # Update the grid with the new deck position
                self.game.player_board.add_desk_to_grid()

                # Show the updated board to the player
                self.io.draw_single_field(
                        ships=self.game.player_board.ships,
                        grid=self.game.player_board.grid
                        )

            except Exception as err:
                self.io.show_error(f"Unexpected error: {err}")
                continue

        # After placing the ship, update the set of surrounding cells to overlap
        all_surrounding |= set(
                    self.game.player_board.get_surrounding_cells(current_ship)
                    )



class PlayingState(GameState):
    """
    Represents the state when the game is in progress.
    """

    def handle(self):
        pass
        # self.io.show_message("Playing mode.")



class FinishedState(GameState):
    """
    Represents the state when the game has ended.
    """

    def handle(self):
        pass



class Game:
    """
    The main entry point for the game logic.

    It stores the game states, boards, and delegates actions
    to the current state.
    """

    def __init__(self, io: GameInputOutput):
        self.io = io
        self.state: GameState = NotStartState(self)
        self.player_board = Board(SHIPS_INFO)
        self.opp_board = Board(SHIPS_INFO)
        self._finished = False


    def set_state(self, new_state: GameState) -> None:
        """
        Change the current state of the game.

        Parameters:
        new_state (GameState): The new state to switch to.
        """
        self.state = new_state


    def run_step(self) -> None:
        """
        Run one step of the game by calling the current state's handle method.
        """
        self.state.handle()


    def is_finishing(self) -> bool:
        """
        Check if the game is finished.
        """
        return self._finished
