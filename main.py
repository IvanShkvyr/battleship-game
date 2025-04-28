"""я бы начинал не изнутри, а снаружи
написать логику ввода и валидации координат пользователем, и возвращения ответа
от компьютера. пока можешь не париться насчет классов и того, как всё это организовать

відображення поля
   0 1 2 3 4 5 6 7 8 9
 +---------------------+ 
a| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
b| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
c| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
d| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
e| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
f| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
g| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
h| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
i| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
j| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
 +---------------------+
~ - пусте місце
Х – підбитий корабель
О – палуба корабля
* - місце промаху/де не може бути корабельͱ +




"""
import random


RED = "\033[91m"
RESET = "\033[0m"

# Format: "ship name" : number of decks
ships_info = {
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

# Generate battleships_player_1
battleships_player_1 = {}
for ship_name, decks in ships_info.items():
    battleships_player_1[ship_name] = {i: [False, False, False] for i in range(1, decks + 1)}

# Generate battleships_player_2
battleships_player_2 = {}
for ship_name, decks in ships_info.items():
    battleships_player_2[ship_name] = {i: [False, False, False] for i in range(1, decks + 1)}

# Generating player fields
player_1_ship_list = [["~" for _ in range(10)] for _ in range(10)]
player_2_ship_list = [["~" for _ in range(10)] for _ in range(10)]

# Lists of coordinates for the field names on the grid
grid_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
grid_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def get_ship_visual(ship_properties: dict, ship_decks: int) -> str:
    """
    Creates a ship visualization by displaying its decks as a string.
    The following symbols are used:
    - "_" - an unfilled position;
    - "?" - the current deck being input;
    - "X" - a deck whose coordinates have already been entered.

    Parameters:
    ship_properties : dict - A dictionary containing information about the ship
        (specifically its length).
    
    ship_decks : int - A number indicating which deck of the ship is currently
        being input. This is the index of the deck currently being entered (from
        1 to the total number of decks).

    Returns:
    str - A string representing the ship's visualization.
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


def convert_ship_dict_to_field_list(ship_dict: dict, ship_list: list) -> list:
    """
    Fills the list of cells on the field with ships' positions for visualization

    This function takes information about the ships' positions from the
    dictionary and marks the cells on the field as either "O" (for ship
    presence) or "X" (for hit ships).

    Parameters:
    ship_dict : dict - A dictionary containing information about the ships'
        positions. Each ship type has its own list of positions, which includes
        row, column, and whether it has been hit.
    
    ship_list : list - A 2D list representing the game field, where each cell is
        either empty or occupied by a ship.

    Returns:
    list - The updated game field with ships marked as either "O" or "X".
    """
    for ship_type, ship_properties in ship_dict.items():
        for ship_decks, desk_properties in ship_properties.items():

            # Skip if there is no deck information available
            if desk_properties[1] == False:
                continue

            # Get the index of the row and column
            row = grid_letters.index(desk_properties[1])  
            col = grid_numbers.index(str(desk_properties[0]))
            # Mark the cell with "O" for an unhit ship or "X" for a hit ship
            ship_list[row][col] = "O" if desk_properties[2] else "X"  

    return ship_list


def get_surrounding_cells(ship: list) -> list:
    """
    This function creates a list of cells around the given ship. 

    The function considers all the cells around each deck of the ship (including
    diagonals).

    Parameters:
    ship : list - A list of coordinates representing the positions of the ship's
        decks. Each deck is a tuple of (column, row).

    Returns:
    list - A list of coordinates of the cells around the ship (adjacent cells).
    """
    surrounding_cells = []

    # Loop through each deck of the ship
    for coord_cell in ship:

        # Check all the adjacent cells (delta = -1, 0, 1 for row and column)
        for i in range(-1,2):
            for j in range(-1,2):

                # Get the row and column index of the current deck
                coord_row = grid_letters.index(coord_cell[1])
                coord_col = grid_numbers.index(str(coord_cell[0]))

                new_coord_row = coord_row + i
                new_coord_col = coord_col + j

                # Check if the new coordinates are within the field limits
                if not (0 <= new_coord_row < 10 and 0 <= new_coord_col < 10):

                    continue

                # Convert the new coordinates back to our coordinate format
                new_coord = grid_numbers[
                    new_coord_col
                    ] + grid_letters[
                        new_coord_row
                        ]

                # Add the new coordinate to the list if it isn't already there
                if new_coord not in surrounding_cells:
                    surrounding_cells.append(new_coord)

    return surrounding_cells


def r(ship_properties: dict) -> str:
    """
    This function creates a representation of a ship on the board. 
        - If a deck is destroyed or its coordinates are not set, it is marked
            with "X".
        - If a deck exists with defined coordinates, it is marked with "O".

    Parameters:
    ship_properties : dict - A dictionary containing information about the
        ship's decks. Each deck's properties include condition.

    Returns:
    str - A string representing the ship with "X" for destroyed or undefined
        decks, and "O" for existing decks with defined coordinates.
    """
    # Create the ship's representation
    ship = ""

    for ship_decks, desk_properties in ship_properties.items():

        # Check if the deck is destroyed (False) or undefined
        # and set the appropriate symbol
        if desk_properties[2] == False:
            ship += "X"
        else:
            ship += "O"

    return ship


def get_ship_set(
                ship_coords: list,
                new_coord: str
                ) -> tuple[set[str], set[str]]:
    """
    Returns two sets containing the row and column numbers of the ship's
    coordinates for further checks.

    Parameters:
    ship_coords : list - A list of tuples representing the ship's current
        coordinates.
    new_coord : str - A string representing the new coordinate to be added to
        the ship's position.

    Returns:
    tuple : A tuple containing two sets:
        - The first set contains all the column numbers (as strings)
        - The second set contains all the row numbers (as strings)
    """
    # Create empty sets for rows and columns
    col_sets = set()
    row_sets = set()
    
    # Add the coordinates of the existing ship's decks to the sets
    for ship_decks in ship_coords:
        col_sets.add(ship_decks[0])
        row_sets.add(ship_decks[1])

    # Add the new deck's coordinates to the sets
    col_sets.add(new_coord[0])
    row_sets.add(new_coord[1])

    return col_sets, row_sets


def is_adjacent_coordinates(ship_coords: list, new_coord: str) -> bool:
    """
    Checks if the given coordinate is adjacent to the last entered coordinate.

    This function compares the last deck's coordinates with the new coordinate
    to ensure they are adjacent to each other on the grid. It checks if the new
    coordinate is directly next to the last one.

    TODO: The function should be extended to handle cases where the new
    coordinate is on the opposite side of the ship

    Parameters:
    ship_coords : list - A list representing the coordinates of the ship's decks
    new_coord : str - A string representing the new coordinate to be checked

    Returns:
    bool - True if the new coordinate is adjacent to the last entered
        coordinate, otherwise False.
    """
    # If there are no coordinates yet, the first coordinate is always valid
    if not ship_coords:
        return True 
    
    # col_sets, row_sets = get_ship_set(ship_coords, new_coord)
    # first_col, first_row = ship_coords[0]

    # Get the last coordinate of the ship and the new coordinate
    last_col, last_row = ship_coords[-1]
    new_col, new_row = new_coord

    # Find the index of the columns and rows in the grid
    idx_last_col = grid_numbers.index(last_col)
    idx_last_row = grid_letters.index(last_row)
    idx_new_col = grid_numbers.index(new_col)
    idx_new_row = grid_letters.index(new_row)

    # Check if the new coordinate is adjacent to the last one
    # sum of index differences should be 1
    if abs(idx_last_col - idx_new_col) + abs(idx_last_row - idx_new_row) == 1:
        return True
    else:
        return False


def is_ship_in_straight_line(ship_coords: list, new_coord: str) -> bool:
    """
    Checks if the new coordinate forms a straight line with the already entered
    ship coordinates.

    This function verifies whether the coordinates of the ship are aligned
    either horizontally (same row) or vertically (same column), forming
    a straight line.

    Parameters:
    ship_coords : list - A list the coordinates of the ship's already placed
        decks.
    new_coord : str - A string representing the new coordinate to be checked.

    Returns:
    bool - True if the new coordinate forms a straight line with the existing
        coordinates (either horizontally or vertically), otherwise False.
    """
    # If there are no coordinates yet, the first coordinate is always valid
    if not ship_coords:
        return True
    
    # Get the sets of column and row coordinates
    col_sets, row_sets = get_ship_set(ship_coords, new_coord)
    
    # Check if the ship coordinates form a straight line
    # Either all columns are the same or all rows are the same
    if (
        len(col_sets) == 1 and len(row_sets) != 1
        ) or (
            len(col_sets) != 1 and len(row_sets) == 1
            ):
        return True

    return False


def drow_full_display(d1: dict, l1: list, d2: dict, l2: list) -> None:
    """
    TODO
    """
    letters = "abcdefghij"
    
    ship_info = {
        0: ("BB", ["BB1"]),
        2: ("CA", ["CA1", "CA2"]),
        4: ("SS", ["SS1", "SS2", "SS3"]),
        6: ("PB", ["PB1", "PB2", "PB3", "PB4"])
    }

    print(
        "    Your field                                                   Opponent's field\n"
        "   0 1 2 3 4 5 6 7 8 9                                          0 1 2 3 4 5 6 7 8 9"
    )
    print(" +---------------------+                                      +---------------------+")

    for i in range(10):
        left_row = f"{letters[i]}| " + " ".join(l1[i]) + " |"
        right_row = f"{letters[i]}| " + " ".join(l2[i]) + " |"

        # Якщо треба додати інформацію про кораблі
        if i in ship_info:
            ship_name, keys = ship_info[i]
            left_ships = " - ".join(r(d1[k]) for k in keys)
            right_ships = " - ".join(r(d2[k]) for k in keys)
            # важливо: менше місця між лівим і правим, щоб лівий бік не зсувався
            print(f"{left_row}  {ship_name} - {left_ships:<30}{right_row}  {ship_name} - {right_ships}")
        else:
            print(f"{left_row}                                     {right_row}")

    print(" +---------------------+                                      +---------------------+")
    print("                                    Your turn!")


def draw_players_display(d1: dict, l1: list) -> None:
    """
    Displays the player's field during the ship placement phase.

    This function visualizes the game field by filling the provided list with
    ship positions and displaying the current state of the field. It also shows
    the status of each ship type based on the provided ship dictionary.

    Parameters:
    ship_dict : dict - A dictionary containing information about the ships'
        positions. Each ship has a list of positions and their hit status.

    ship_list : list - A 2D list representing the game field. Each sublist
        corresponds to a row and contains characters for empty cells or ship
        positions.

    Returns:
        None
    """ 
    grid_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    ship_info = {
        0: ("BB", ["BB1"]),
        2: ("CA", ["CA1", "CA2"]),
        4: ("SS", ["SS1", "SS2", "SS3"]),
        6: ("PB", ["PB1", "PB2", "PB3", "PB4"]),
    }

    print("""
       Your field                
   0 1 2 3 4 5 6 7 8 9
 +---------------------+ 
""", end="")

    for idx, row in enumerate(l1):
        line = f"{grid_letters[idx]}| " + " ".join(row) + " |"
        if idx in ship_info:
            ship_name, keys = ship_info[idx]
            ship_status = " - ".join(r(d1[k]) for k in keys)
            line += f"  {ship_name} - {ship_status}"
        print(line)

    print(" +---------------------+")


def get_auto_coordinates(orientation: str, coord: str, ship_len: int) -> list:
    """
    Generates a list of coordinates for a ship placed automatically.

    This function computes a list of coordinates based on the provided starting
    coordinate, ship length, and orientation (either horizontal or vertical).

    Parameters:
    orientation : str
        A string that indicates the ship's orientation:
        - "horizontal" for horizontal placement.
        - "vertical" for vertical placement.
    coord : str - A string representing the starting coordinate of the ship.
    ship_len : int - The length of the ship, which determines how many cells the
        ship will occupy.

    Returns: 
    list : A list of strings, each representing the coordinates of the ship's
        cells.
    """
    new_ship = []

    # Find the column and row indexes for the given coordinate
    idx_col = grid_numbers.index(coord[0])
    idx_row = grid_letters.index(coord[1])

    if orientation == "horizontal":
        # Row index stays the same, column changes
        delta_row = 1
        for i in range(ship_len):
            new_ship.append(
                grid_numbers[idx_col + i + delta_row]+grid_letters[idx_row]
                )
    else:
        # Column index stays the same, row changes
        delta_col = 1
        for i in range(ship_len):
            new_ship.append(
                grid_numbers[idx_col ]+grid_letters[idx_row + i + delta_col]
                )
    return new_ship


def add_new_battleship(
                    player_1_ship_list: list,
                    battleships_player_1: dict
                    ) -> None:
    """
    Prompts the player to place battleships on the field.

    This function allows the player to input the coordinates of each ship's
    decks, and checks whether the placement is valid according to the game's
    rules.

    Parameters:
    player_1_ship_list : list - An empty list representing the player's game
        field, where the ships will be placed.
    
    battleships_player_1 : dict - A dictionary containing the ships' properties,
        such as type, length, and status.
    
    Returns:
    None - This function updates the `player_1_ship_list` and
        `battleships_player_1` dictionaries directly.
    """
    blacklist_1 = []
    current_ship = []
    current_ship_type ="BB1"
    surrounding_cells = []

    for ship_type, ship_properties in battleships_player_1.items():
        for ship_decks, desk_properties in ship_properties.items():

            while True:
                try:
                    if current_ship_type != ship_type:
                        surrounding_cells += get_surrounding_cells(current_ship)
                        current_ship = []

                    ship_view = get_ship_visual(ship_properties, ship_decks)

                    player_input = input(
                f"Please put your battleships {ship_type[0:2]} ({ship_view}):"
                ).upper()

                    # Validate input length
                    if len(player_input) != 2:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The ship's deck coordinate must consist of two characters: a number and a letter.")
                        raise ValueError

                    # Validate column input (first character must be a number)
                    if player_input[0] not in grid_numbers:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The first value must be a number between 0 and 9.")
                        raise ValueError

                    # Validate row input (second character must be a letter)
                    if player_input[1] not in grid_letters:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The second value must be a letter from 'A' to 'J'.")
                        raise ValueError

                    # Ensure the coordinate is not duplicated
                    if player_input in blacklist_1:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The coordinate is duplicated.")
                        raise ValueError

                    # Ensure the new coordinate is adjacent to the current ship
                    if not is_adjacent_coordinates(current_ship, player_input):
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The entered coordinate is not adjacent to the previous one.")
                        raise ValueError

                    # Ensure the coordinates form a straight line
                    if not is_ship_in_straight_line(current_ship, player_input):
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The ship's coordinates do not form a straight line")
                        raise ValueError

                    # Ensure the cell is not adjacent to an existing ship
                    if player_input in surrounding_cells:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("This cell is adjacent to an existing ship and cannot be selected.")
                        raise ValueError

                    current_ship_type = ship_type

                    if current_ship_type == ship_type:
                        current_ship.append(player_input[0]+player_input[1])

                    blacklist_1.append(player_input[0]+player_input[1])

                    # Update the ship's coordinates in the battleship dictionary
                    battleships_player_1[ship_type][ship_decks][0] = int(player_input[0])
                    battleships_player_1[ship_type][ship_decks][1] = player_input[1]
                    battleships_player_1[ship_type][ship_decks][2] = True

                    # Convert the updated dictionary to the game field list
                    player_1_ship_list = convert_ship_dict_to_field_list(
                        battleships_player_1,
                        player_1_ship_list
                        )

                    # Draw the updated field
                    draw_players_display(
                        battleships_player_1,
                        player_1_ship_list
                        )

                    break # Exit the loop if no errors
            
                except Exception:
                    print(f"{RED}____________ERROR_______________{RESET}")


def auto_place_ships(ship_list: list, battleships: dict) -> None:
    """
    Automatically places battleships on the field without user input.

    This function randomly selects coordinates and orientation (horizontal or
    vertical) for each ship, ensuring that:
    - Ships do not overlap.
    - Ships are not placed adjacent to one another (no contact).
    - Ships stay within the game grid boundaries.

    Parameters:
    ship_list : list - The player's game field list that visually represents the
        current ship layout.

    battleships : dict - A dictionary containing the player's battleships with
        their properties, such as length and current placement status.

    Returns:
    None - This function modifies the `ship_list` and `battleships` in-place.
    """
    surrounding_cells = []

    for ship_type, ship_properties in battleships.items():

        while True:
            # Random orientation and starting coordinate
            random_orientation = random.choice(["horizontal", "vertical"])
            random_coord = random.choice(grid_numbers) + random.choice(grid_letters)
            ship_len = len(ship_properties)

            try:
                # Generate coordinates for the ship
                auto_ship = get_auto_coordinates(
                                                random_orientation,
                                                random_coord,
                                                ship_len
                                                )
                
                # Check if any cell is adjacent to existing ships
                for i in auto_ship:
                    if i in surrounding_cells:
                        raise ValueError
                    
                # Update the list of surrounding cells
                surrounding_cells += get_surrounding_cells(auto_ship)

                # Assign coordinates to the ship in the dictionary
                for key in ship_properties:
                    ship_properties[key] = [
                        int(auto_ship[key-1][0]), auto_ship[key-1][1], True
                        ]

                # Valid ship placed, exit the loop
                break

            except Exception:
                # Try again if placement is invalid
                continue

    # Convert ship dictionary to field list for visualization
    player_1_ship_list = convert_ship_dict_to_field_list(battleships, ship_list)

    draw_players_display(battleships, player_1_ship_list) # #############################################


def main():
    """
    TODO
    """
    while True:

        add_new_battleship(player_1_ship_list, battleships_player_1)

        auto_place_ships(player_2_ship_list, battleships_player_2)

        drow_full_display(battleships_player_1, player_1_ship_list, battleships_player_2, player_2_ship_list) 
       
        break
 

if "__main__" == __name__:
    main()
