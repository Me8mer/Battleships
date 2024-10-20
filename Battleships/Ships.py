from enum import Enum
from Player_internal_logic import TileState
from Initializations import MessageBox
from Globals_constants import Direction

class ShipsTypes(Enum):
    '''Types of ships. Numbered for easier rotating through them'''
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

class Ship:
    '''Ship instances with size and health based on the ship type'''
    def __init__(self,type):
        self.type = type
        self.size = get_size_by_type(type)
        self.health = self.size

#gets tiles locations on map based on the chosen ship  
def get_whole_ship_location(main_pos,ship_size, direction,X,RECT_NUM):
    new_active_tiles = list(-1 for x in range(ship_size))
    new_active_tiles[0] = main_pos
    for x in range(1, ship_size):
        if direction == Direction.UP: shift = 1 ; shift_mod = X
        else: shift = -X ; shift_mod = RECT_NUM
        if x == 3: shift = -shift
        new_pos = (new_active_tiles[0] % shift_mod) + shift
        if (x == 2): new_pos = new_pos + shift
        if (new_pos < 0) or new_pos >= shift_mod:
            new_pos = new_pos + (ship_size * (-1 * shift))
        shift = new_pos - (new_active_tiles[0] % shift_mod)
        new_active_tiles[x] = new_active_tiles[0] + shift
    return(new_active_tiles)

#rotates between available ships when placing them
def rotate_available_ships(direction, current_ship, remaining_ships):
    if direction == Direction.RIGHT:
        current_ship = (current_ship + 1) % 3
    else:
        current_ship = (current_ship - 1) % 3
    if remaining_ships[current_ship] == 0:
        current_ship = rotate_available_ships(direction, current_ship, remaining_ships)
    return(current_ship)

#size of ship based on it's type
def get_size_by_type(type):
        if type == ShipsTypes.SMALL:
            return 2
        elif type == ShipsTypes.MEDIUM:
            return 3
        else:
            return 4
        
def placing_ship(player, active_tile, active_ship):
        place = True
        for x in active_tile:
            if player.map_list[x] == TileState.ALIVE_SHIP:
                place = False
                MessageBox.new_message("Cannot place. (select different tiles)")
        if place:
            MessageBox.new_message("Place Ships")
            new_ship = Ship(active_ship)
            for x in active_tile:
                player.map_list[x] = TileState.ALIVE_SHIP
                player.ship_locations.update({x:new_ship})  
            player.ships_to_place[active_ship.value] -= 1
    

