
from enum import Enum
from Initializations import MessageBox,HitBox
 
class TileState(Enum):
    '''States of tiles displayed to player'''
    WATER = 0
    ALIVE_SHIP = 1
    MISSED_SHOT = 2
    DESTROYED_SHIP = 3

class Player:
    '''Main class for storing parameters of PLayer and AI'''
    def __init__(self, ships, NUM_RECT, score_box):
        self.ships_to_place = ships.copy()
        self.remaining_ships = ships.copy() #keeping track of ships not destroyed yet
        self.map_list = [TileState.WATER] * NUM_RECT #map of ships placements for recreating the map 
        self.ship_locations = {} #ship locations for registering hits and keeping track of ships health
        self.score_box = score_box #score box of player
    
    #updates the score box
    def update_score(self,ship_type):
        help_text = str(self.remaining_ships[ship_type.value])
        self.score_box.update_box(help_text,ship_type.value)

#chceks ending conditions
def check_ending(Player, AI):      
    if all(ships_numbers == 0 for ships_numbers in AI.remaining_ships):
        MessageBox.new_message("YOU WIN")
        return True
    if all(ships_numbers == 0 for ships_numbers in Player.remaining_ships):
        MessageBox.new_message("ENEMY WINS")
        return True
    return False

#checks if current hit hits the opposite player. Updates score and data if hit lands.
def hit(num,player):
    ships_dict = player.ship_locations
    ships_list = player.remaining_ships
    if num in ships_dict:
        help_ship = ships_dict[num]
        help_ship.health -= 1
        if help_ship.health <= 0:
            ships_list[help_ship.type.value] -= 1 
            player.update_score(help_ship.type)           
            MessageBox.new_message("Shots fired. Ship destroyed")
            return(True)
        return(False)
    
def check_if_hit(AI,active_tile):
    if active_tile[0] in AI.ship_locations:                                  
        HitBox.hit_message(True)
        hit(active_tile[0],AI)
        AI.map_list[active_tile[0]] = TileState.DESTROYED_SHIP
        return True
    else:
        HitBox.hit_message(False)
        AI.map_list[active_tile[0]] = TileState.MISSED_SHOT
        return False



