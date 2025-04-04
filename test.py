

ship_properties = {1:[False, False, False,], 2:[False, False, False,], 3:[False, False, False,], 4:[False, False, False,]}
auto_ship = ['1E', '2E', '3E', '4E']

for key in ship_properties:
    ship_properties[key] = [int(auto_ship[key-1][0]), auto_ship[key-1][1], True]


print(ship_properties)
