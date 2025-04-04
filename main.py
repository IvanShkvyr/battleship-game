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

battleships_player_1 = {"BB1":{1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,], 4:[False, False, False,]},
                        "CA1": {1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,]},
                        "CA2": {1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,]},
                        "SS1": {1:[False, False, False,], 2:[False, False, False,]},
                        "SS2": {1:[False, False, False,], 2:[False, False, False,]},
                        "SS3": {1:[False, False, False,], 2:[False, False, False,]},
                        "PB1": {1:[False, False, False,],},
                        "PB2": {1:[False, False, False,],},
                        "PB3": {1:[False, False, False,],},
                        "PB4": {1:[False, False, False,],},
                        }

battleships_player_2 = {"BB1":{1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,], 4:[False, False, False,]},
                        "CA1": {1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,]},
                        "CA2": {1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,]},
                        "SS1": {1:[False, False, False,], 2:[False, False, False,]},
                        "SS2": {1:[False, False, False,], 2:[False, False, False,]},
                        "SS3": {1:[False, False, False,], 2:[False, False, False,]},
                        "PB1": {1:[False, False, False,],},
                        "PB2": {1:[False, False, False,],},
                        "PB3": {1:[False, False, False,],},
                        "PB4": {1:[False, False, False,],},
                        }

player_1_ship_list = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                    ]

player_2_ship_list = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                      ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                    ]

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

    # Create the initial ship template: all positions are unfilled ("_")
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
    TODO
    """
    for ship_type, ship_properties in ship_dict.items():
        for ship_decks, desk_properties in ship_properties.items():
            if desk_properties[1] == False:
                continue

            row = grid_letters.index(desk_properties[1])  # Отримуємо індекс рядка
            col = grid_numbers.index(str(desk_properties[0]))  # Отримуємо індекс колонки
            
            ship_list[row][col] = "O" if desk_properties[2] else "X"  # Позначаємо корабель

    return ship_list


def get_surrounding_cells(ship: list) -> list:
    """
    TODO
    """
    surrounding_cells = []

    for coord_cell in ship:


        for i in range(-1,2):
            for j in range(-1,2):

                coord_row = grid_letters.index(coord_cell[1])  # Отримуємо індекс рядка
                coord_col = grid_numbers.index(str(coord_cell[0]))  # Отримуємо індекс колонки

                new_coord_row = coord_row + i
                new_coord_col = coord_col + j

                if not (
                    new_coord_row >= 0 and new_coord_row < 10
                    ) and (
                        new_coord_col >= 0 and new_coord_col < 10
                        ):
                    continue

                new_coord = grid_numbers[new_coord_col] + grid_letters[new_coord_row]

                if new_coord not in surrounding_cells:
                    surrounding_cells.append(new_coord)

    return surrounding_cells


def r(ship_properties: dict) -> str:
    """
    TODO
    """
    ship = ""

    for ship_decks, desk_properties in ship_properties.items():
        if desk_properties[2] == False:
            ship += "X"
        else:
            ship += "O"

    return ship


def get_ship_set(ship_coords: list, new_coord: str) -> tuple[set[str], set[str]]:
    """
    TODO
    """
    col_sets = set()
    row_sets = set()
    
    for ship_decks in ship_coords:
        col_sets.add(ship_decks[0])
        row_sets.add(ship_decks[1])

    
    col_sets.add(new_coord[0])
    row_sets.add(new_coord[1])

    return col_sets, row_sets


def is_adjacent_coordinates(ship_coords: list, new_coord: str) -> bool:
    """
    TODO
    """
    if not ship_coords:
        return True # Перша координата завжди правильна
    
    col_sets, row_sets = get_ship_set(ship_coords, new_coord)


    first_col, first_row = ship_coords[0]
    last_col, last_row = ship_coords[-1]
    new_col, new_row = new_coord

    idx_last_col = grid_numbers.index(last_col)
    idx_last_row = grid_letters.index(last_row)
    idx_new_col = grid_numbers.index(new_col)
    idx_new_row = grid_letters.index(new_row)

    if abs(idx_last_col - idx_new_col) + abs(idx_last_row - idx_new_row) == 1:
        return True
    else:
        return False


def is_ship_in_straight_line(ship_coords: list, new_coord: str) -> bool:
    """
    TODO
    """

    if not ship_coords:
        return True # Перша координата завжди правильна
    
    col_sets, row_sets = get_ship_set(ship_coords, new_coord)
    
    if (
        len(col_sets) == 1 and len(row_sets) != 1
        ) or (
            len(col_sets) != 1 and len(row_sets) == 1
            ):
        print("len(col_sets) ", len(col_sets))
        print("len(row_sets) ", len(row_sets))
        return True

    return False


def drow_full_display(d1: dict, l1: list) -> None:
    """
    TODO
    """
    X = "X"
    XX = "0X"
    XXX = "X0X"
    XXXX = "X0XX"

    print(
        f"""
       Your field                                             Opponent's field                     
   0 1 2 3 4 5 6 7 8 9                                        0 1 2 3 4 5 6 7 8 9
 +---------------------+                                    +---------------------+  
a| {l1[0][0]} {l1[0][1]} {l1[0][2]} {l1[0][3]} {l1[0][4]} {l1[0][5]} {l1[0][6]} {l1[0][7]} {l1[0][8]} {l1[0][9]} |  BB - {r(d1["BB1"])}                        a| ~ ~ ~ ~ ~ ~ ~ * ~ ~ |  BB - {XXXX}
b| {l1[1][0]} {l1[1][1]} {l1[1][2]} {l1[1][3]} {l1[1][4]} {l1[1][5]} {l1[1][6]} {l1[1][7]} {l1[1][8]} {l1[1][9]} |                                   b| ~ ~ ~ X X X ~ ~ ~ ~ |  
c| {l1[2][0]} {l1[2][1]} {l1[2][2]} {l1[2][3]} {l1[2][4]} {l1[2][5]} {l1[2][6]} {l1[2][7]} {l1[2][8]} {l1[2][9]} |  CA - {r(d1["CA1"])} - {r(d1["CA2"])}                   c| ~ ~ ~ ~ * ~ ~ ~ ~ ~ |  CA - {XXX} - {XXX}
d| {l1[3][0]} {l1[3][1]} {l1[3][2]} {l1[3][3]} {l1[3][4]} {l1[3][5]} {l1[3][6]} {l1[3][7]} {l1[3][8]} {l1[3][9]} |                                   d| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |
e| {l1[4][0]} {l1[4][1]} {l1[4][2]} {l1[4][3]} {l1[4][4]} {l1[4][5]} {l1[4][6]} {l1[4][7]} {l1[4][8]} {l1[4][9]} |  SS - {r(d1["SS1"])} - {r(d1["SS2"])} - {r(d1["SS3"])}                e| ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ |  SS - {XX} - {XX} - {XX}
f| {l1[5][0]} {l1[5][1]} {l1[5][2]} {l1[5][3]} {l1[5][4]} {l1[5][5]} {l1[5][6]} {l1[5][7]} {l1[5][8]} {l1[5][9]} |                                   f| ~ ~ ~ ~ ~ ~ ~ * * ~ |
g| {l1[6][0]} {l1[6][1]} {l1[6][2]} {l1[6][3]} {l1[6][4]} {l1[6][5]} {l1[6][6]} {l1[6][7]} {l1[6][8]} {l1[6][9]} |  PB - {r(d1["PB1"])} - {r(d1["PB2"])} - {r(d1["PB3"])} - {r(d1["PB4"])}               g| ~ ~ X ~ ~ ~ ~ ~ ~ ~ |  PB - {X} - {X} - {X} - {X}
h| {l1[7][0]} {l1[7][1]} {l1[7][2]} {l1[7][3]} {l1[7][4]} {l1[7][5]} {l1[7][6]} {l1[7][7]} {l1[7][8]} {l1[7][9]} |                                   h| ~ ~ X * ~ ~ ~ ~ ~ ~ |
i| {l1[8][0]} {l1[8][1]} {l1[8][2]} {l1[8][3]} {l1[8][4]} {l1[8][5]} {l1[8][6]} {l1[8][7]} {l1[8][8]} {l1[8][9]} |                                   i| ~ ~ ~ * ~ ~ ~ ~ X ~ |
j| {l1[9][0]} {l1[9][1]} {l1[9][2]} {l1[9][3]} {l1[9][4]} {l1[9][5]} {l1[9][6]} {l1[9][7]} {l1[9][8]} {l1[9][9]} |                                   j| ~ ~ ~ * ~ ~ ~ ~ ~ ~ |
 +---------------------+                                    +---------------------+
                                    Your turn!
"""
    )



def drow_players_display(d1: dict, l1: list) -> None:
    """
    TODO
    """
    print(
        f"""
       Your field                
   0 1 2 3 4 5 6 7 8 9
 +---------------------+ 
a| {l1[0][0]} {l1[0][1]} {l1[0][2]} {l1[0][3]} {l1[0][4]} {l1[0][5]} {l1[0][6]} {l1[0][7]} {l1[0][8]} {l1[0][9]} |  BB - {r(d1["BB1"])}
b| {l1[1][0]} {l1[1][1]} {l1[1][2]} {l1[1][3]} {l1[1][4]} {l1[1][5]} {l1[1][6]} {l1[1][7]} {l1[1][8]} {l1[1][9]} |
c| {l1[2][0]} {l1[2][1]} {l1[2][2]} {l1[2][3]} {l1[2][4]} {l1[2][5]} {l1[2][6]} {l1[2][7]} {l1[2][8]} {l1[2][9]} |  CA - {r(d1["CA1"])} - {r(d1["CA2"])}
d| {l1[3][0]} {l1[3][1]} {l1[3][2]} {l1[3][3]} {l1[3][4]} {l1[3][5]} {l1[3][6]} {l1[3][7]} {l1[3][8]} {l1[3][9]} |
e| {l1[4][0]} {l1[4][1]} {l1[4][2]} {l1[4][3]} {l1[4][4]} {l1[4][5]} {l1[4][6]} {l1[4][7]} {l1[4][8]} {l1[4][9]} |  SS - {r(d1["SS1"])} - {r(d1["SS2"])} - {r(d1["SS3"])}
f| {l1[5][0]} {l1[5][1]} {l1[5][2]} {l1[5][3]} {l1[5][4]} {l1[5][5]} {l1[5][6]} {l1[5][7]} {l1[5][8]} {l1[5][9]} |
g| {l1[6][0]} {l1[6][1]} {l1[6][2]} {l1[6][3]} {l1[6][4]} {l1[6][5]} {l1[6][6]} {l1[6][7]} {l1[6][8]} {l1[6][9]} |  PB - {r(d1["PB1"])} - {r(d1["PB2"])} - {r(d1["PB3"])} - {r(d1["PB4"])}
h| {l1[7][0]} {l1[7][1]} {l1[7][2]} {l1[7][3]} {l1[7][4]} {l1[7][5]} {l1[7][6]} {l1[7][7]} {l1[7][8]} {l1[7][9]} |
i| {l1[8][0]} {l1[8][1]} {l1[8][2]} {l1[8][3]} {l1[8][4]} {l1[8][5]} {l1[8][6]} {l1[8][7]} {l1[8][8]} {l1[8][9]} |
j| {l1[9][0]} {l1[9][1]} {l1[9][2]} {l1[9][3]} {l1[9][4]} {l1[9][5]} {l1[9][6]} {l1[9][7]} {l1[9][8]} {l1[9][9]} |
 +---------------------+
"""
    )


def get_auto_coordinates(orientation: str, coord: str, ship_len: int) -> list:
    """
    TODO
    """
    new_ship = []

    idx_col = grid_numbers.index(coord[0])
    idx_row = grid_letters.index(coord[1])

    if orientation == "horizontal":
        delta_row = 1

        for i in range(ship_len):
            new_ship.append(
                grid_numbers[idx_col + i + delta_row]+grid_letters[idx_row]
                )
    else:

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
    TODO
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


                    if len(player_input) != 2:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The ship's deck coordinate must consist of two characters: a number and a letter.")
                        raise ValueError

                    if player_input[0] not in grid_numbers:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The first value must be a number between 0 and 9.")
                        raise ValueError

                    if player_input[1] not in grid_letters:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The second value must be a letter from 'A' to 'J'.")
                        raise ValueError

                    if player_input in blacklist_1:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The coordinate is duplicated.")
                        raise ValueError

                    if not is_adjacent_coordinates(current_ship, player_input):
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The entered coordinate is not adjacent to the previous one.")
                        raise ValueError

                    if not is_ship_in_straight_line(current_ship, player_input):
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("The ship's coordinates do not form a straight line")
                        raise ValueError

                    if player_input in surrounding_cells:
                        print(f"{RED}____________ERROR_______________{RESET}")
                        print("This cell is adjacent to an existing ship and cannot be selected.")
                        raise ValueError

                    current_ship_type = ship_type

                    if current_ship_type == ship_type:
                        current_ship.append(player_input[0]+player_input[1])

                    blacklist_1.append(player_input[0]+player_input[1])

                    battleships_player_1[ship_type][ship_decks][0] = int(player_input[0])
                    battleships_player_1[ship_type][ship_decks][1] = player_input[1]
                    battleships_player_1[ship_type][ship_decks][2] = True

                    player_1_ship_list = convert_ship_dict_to_field_list(
                        battleships_player_1,
                        player_1_ship_list
                        )

                    drow_players_display(
                        battleships_player_1,
                        player_1_ship_list
                        )

                    break
                except Exception:
                    print(f"{RED}____________ERROR_______________{RESET}")


def auto_place_ships(ship_list: list, battleships: dict) -> None:
    """
    TODO
    """
    surrounding_cells = []

    for ship_type, ship_properties in battleships.items():

        while True:
            random_orientation = random.choice(["horizontal", "vertical"])
            random_coord = random.choice(grid_numbers) + random.choice(grid_letters)
            ship_len = len(ship_properties)

            try:
                auto_ship = get_auto_coordinates(
                                                random_orientation,
                                                random_coord,
                                                ship_len
                                                )
                for i in auto_ship:
                    if i in surrounding_cells:
                        raise ValueError
                    
                surrounding_cells += get_surrounding_cells(auto_ship)

                for key in ship_properties:
                    # Присвоюємо відповідне значення з list_1 для кожного індексу
                    ship_properties[key] = [
                        int(auto_ship[key-1][0]), auto_ship[key-1][1], True
                        ]

                break

            except Exception:
                continue

    player_1_ship_list = convert_ship_dict_to_field_list(battleships, ship_list)

    drow_players_display(battleships, player_1_ship_list) # #############################################


def main():
    """
    TODO
    """
    while True:

        # add_new_battleship(player_1_ship_list, battleships_player_1)

        auto_place_ships(player_2_ship_list, battleships_player_2)
       
        break
 

if "__main__" == __name__:
    main()
