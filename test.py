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

import os
import platform

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



def clear_console():
    """Очищує консоль з урахуванням операційної системи"""
    if platform.system() == "Windows":
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Mac та Linux


def get_ship_visual(ship_properties, ship_decks):
    """TODO"""

    ship_length = len(ship_properties)

    ship_visual = ["_"] * ship_length

    ship_visual[ship_decks - 1] = "?"

    if ship_decks != 1:
        for i, value in enumerate(ship_visual[:ship_decks-1]):
            ship_visual[i] = "X"


    ship_visual = "".join(ship_visual)  # Перетворюємо список назад у рядок
    return ship_visual

def convert_ship_dict_to_field_list(ship_dict, ship_list):
    """TODO"""

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

                if not (new_coord_row >= 0 and new_coord_row < 10) and (new_coord_col >= 0 and new_coord_col < 10):
                    continue

                new_coord = grid_numbers[new_coord_col] + grid_letters[new_coord_row]

                if new_coord not in surrounding_cells:
                    surrounding_cells.append(new_coord)

    return surrounding_cells



                



def r(ship_properties):
    ship = ""

    for ship_decks, desk_properties in ship_properties.items():
        if desk_properties[2] == False:
            ship += "X"
        else:
            ship += "O"
    
    return ship

    
def is_adjacent_coordinates(ship_coords, new_coord):
    """TODO"""

    if not ship_coords:
        return True # Перша координата завжди правильна



    last_col, last_row = ship_coords[-1]
    new_col, new_row = new_coord

    idx_last_col = grid_numbers.index(last_col)
    idx_last_row = grid_letters.index(last_row)
    idx_new_col = grid_numbers.index(new_col)
    idx_new_row = grid_letters.index(new_row)

    if abs(idx_last_col - idx_new_col) + abs(idx_last_row - idx_new_row) == 1:

        return True

    return False


def is_ship_in_straight_line(ship_coords, new_coord):
    """TODO"""

    if not ship_coords:
        return True # Перша координата завжди правильна
    
    col_sets = set()
    row_sets = set()
    
    for ship_decks in ship_coords:
        col_sets.add(ship_decks[0])
        row_sets.add(ship_decks[1])

    
    col_sets.add(new_coord[0])
    row_sets.add(new_coord[1])


    if (len(col_sets) == 1 and len(row_sets) != 1) or (len(col_sets) != 1 and len(row_sets) == 1):
        return True

    return False




def drow_display(d1, l1):
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

def add_new_battleship(player_1_ship_list, battleships_player_1):
    """TODO"""

    blacklist_1 = []


    current_ship = []
    current_ship_type =""
    surrounding_cells = []


    for ship_type, ship_properties in battleships_player_1.items():
        for ship_decks, desk_properties in ship_properties.items():



            while True:

                


                try:

                    ship_view = get_ship_visual(ship_properties, ship_decks)

                    player_input = input(f"Please put your battleships ({ship_view}):").upper()

                    print("current_ship - ", current_ship)
                    print(surrounding_cells)
                    print(f"ship_type - {ship_type}")
                    print(f"current_ship_type - {current_ship_type}")

                    # if current_ship_type != ship_type:
                    #     surrounding_cells += get_surrounding_cells(current_ship)


                    if len(player_input) != 2:
                        print("The ship's deck coordinate must consist of two characters: a number and a letter.")
                        raise ValueError
                    
                    if player_input[0] not in grid_numbers:
                        print("The first value must be a number between 0 and 9.")
                        raise ValueError
                    
                    if player_input[1] not in grid_letters:
                        print("The second value must be a letter from 'A' to 'J'.")
                        raise ValueError

                    if player_input in blacklist_1:
                        print("The coordinate is duplicated.")
                        raise ValueError
                    

                    if not is_adjacent_coordinates(current_ship, player_input):
                        print("The entered coordinate is not adjacent to the previous one.")
                        raise ValueError

                    if not is_ship_in_straight_line(current_ship, player_input):
                        print("The ship's coordinates do not form a straight line")
                        raise ValueError
                    
                    if player_input in surrounding_cells:
                        print("This cell is adjacent to an existing ship and cannot be selected.")
                        raise ValueError


                    if current_ship_type == ship_type:
                        current_ship.append(player_input[0]+player_input[1])

                    else:
                        # TODO додати перевірку на те що корабель не межує з іншим кораблем

                        

                        

                        surrounding_cells = get_surrounding_cells(current_ship)

                        current_ship = []


                        current_ship.append(player_input[0]+player_input[1])
                    




                    blacklist_1.append(player_input[0]+player_input[1].upper())

                    battleships_player_1[ship_type][ship_decks][0] = int(player_input[0])
                    battleships_player_1[ship_type][ship_decks][1] = player_input[1]
                    battleships_player_1[ship_type][ship_decks][2] = True


                    player_1_ship_list = convert_ship_dict_to_field_list(battleships_player_1, player_1_ship_list)

                    drow_display(battleships_player_1, player_1_ship_list)

                    current_ship_type = ship_type

                    break

                except Exception as e:
                    print(f"--------------------")

            

def main():
    """
    TODO
    """

    while True:

        add_new_battleship(player_1_ship_list, battleships_player_1)

        # player_input = input("Please put your battleships:")

        # if player_input == "q":
        #     break
        
        break
 
    




if "__main__" == __name__:
    main()





