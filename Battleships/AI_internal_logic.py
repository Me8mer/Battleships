from Initializations import MessageBox, HitBox
from enum import Enum
from Player_internal_logic import TileState, Player, check_ending, hit
from Globals_constants import GameOptions
from Ships import *
import random


class AI_Personal_Tile_States(Enum):
    '''AI's personal noting of known tiles states.'''
    POSSIBLE_HIT_TILE = 0
    ALREADY_HIT_TILE = 1
    ALREADY_MISSED_TILE = 2


class Ai_Internal:
        '''Internal globals for AI'''
        active_shooting = False  #actively shooting or randomly shooting
        attack_plan = None
        plan_direction = None
        active_shooting_tile = None #tile around which creates an attack plan
        largest_remaining_ship_size = None
        AI_map_list_personal = None

        @classmethod
        def Create_AI_Personal_Map(cls):
            cls.AI_map_list_personal = [AI_Personal_Tile_States.POSSIBLE_HIT_TILE] * GameOptions.RECT_NUM  #AI's own memory of players ships


#attack plan fo AI
def get_attack_plan(main_pos,ship_size, direction,X,RECT_NUM):
    sorting_list = []
    new_active_tiles = []
    for x in range(1, ship_size):
        if direction == 1: shift = 1 ; shift_mod = X
        if direction == 0: shift = -X ; shift_mod = RECT_NUM
        if direction == -1: shift = -1 ; shift_mod = X
        if direction == 2: shift = X ; shift_mod = RECT_NUM
        new_pos = (main_pos % shift_mod) + shift
        if x == 2: new_pos = new_pos + shift
        if x == 3: new_pos = new_pos + shift + shift
        if (new_pos < 0) or new_pos >= shift_mod:
            new_pos = new_pos + (ship_size * (-1 * shift))
            shift = new_pos - (main_pos % shift_mod)
            sorting_list.insert(0,main_pos + shift)
        else:
            shift = new_pos - (main_pos % shift_mod)
            new_active_tiles.append(main_pos + shift)
    new_active_tiles = new_active_tiles + sorting_list
    return(new_active_tiles)


def rotate_attack_plan(directions):
        if len(directions) == 1:
                new_dir = (directions[0] + 1) % 2
                if new_dir == 1: directions = [-1,1]
                else: directions = [0,2]
        else: directions.pop(0)
        return(directions)


##Ships placement at the beginning
def AI_place_ships(AI):  
    Ai_Internal.Create_AI_Personal_Map() #initates map personal list   
    #for each ship_to_place tries to place it on the map and remebers the positions of the placed ship
    for ship_type in range(len(AI.ships_to_place)):
        for _ in range(AI.ships_to_place[ship_type]):
            ship_to_be_placed = Ship(ShipsTypes(ship_type))
            placed = False
            while not placed:
                skip = False
                ship_direction = Direction(random.randint(0,1))
                place_num = random.randint(0,(GameOptions.X*GameOptions.Y)-1)
                ship_to_place = get_whole_ship_location(place_num,ship_to_be_placed.size,ship_direction,GameOptions.X,GameOptions.RECT_NUM)           
                for x in ship_to_place:
                    #chesks if possible to place
                    if x in AI.ship_locations:
                        skip = True
                if not skip:
                    for x in ship_to_place:
                        AI.ship_locations.update({x:ship_to_be_placed}) #remebers the locations of placed ship
                    placed = True

#gets largest remaining ship of a player. 
def get_largest_remaining_ship(remaining_ships):
    index = len(remaining_ships) - 1  # Start from the last index
    while index >= 0:
        if remaining_ships[index] > 0:        
           return(index)
        index -= 1

def get_rotated_attack_plan():
    Ai_Internal.plan_direction = rotate_attack_plan(Ai_Internal.plan_direction)
    Ai_Internal.attack_plan = get_attack_plan(Ai_Internal.active_shooting_tile,Ai_Internal.largest_remaining_ship_size,Ai_Internal.plan_direction[0],GameOptions.X,GameOptions.RECT_NUM)

###Main AI function.
def start_AI_turn(player,AI):
    end_game = False
    ship_destroyed = False
    MessageBox.new_message("Shots fired (click to continue)")
    #Tt's actively shooting if it hit a ship. Tries to compute som basic attack plan of possible ship locations around hit zone
    if Ai_Internal.active_shooting:
        #if theres not an attack plan calculates one based on current hit positions and largest remaining ship
        if Ai_Internal.attack_plan == None:
            Ai_Internal.largest_remaining_ship_size = get_size_by_type(get_largest_remaining_ship(player.remaining_ships))
            Ai_Internal.plan_direction = [-1,0,1,2]
            Ai_Internal.attack_plan = get_attack_plan(Ai_Internal.active_shooting_tile,Ai_Internal.largest_remaining_ship_size,Ai_Internal.plan_direction[0],GameOptions.X,GameOptions.RECT_NUM)

        #checks its own map memory and tries to compute an attack plan and a viable shot. There has to be at least one viable shot around
        #the hit position, unless there was a ship destroyed message.
        shot = Ai_Internal.attack_plan.pop(0)
        while Ai_Internal.AI_map_list_personal[shot]  != AI_Personal_Tile_States.POSSIBLE_HIT_TILE:    #while not a viable shot
            if Ai_Internal.AI_map_list_personal[shot]  == AI_Personal_Tile_States.ALREADY_HIT_TILE:
                get_rotated_attack_plan()
            if len(Ai_Internal.attack_plan) == 0:   
                get_rotated_attack_plan()
            shot = Ai_Internal.attack_plan.pop(0)

        #if shot hits continues with plan attack and upates all the neccesary data
        if player.map_list[shot] == TileState.ALIVE_SHIP:
            if len(Ai_Internal.plan_direction) > 2: Ai_Internal.plan_direction = [Ai_Internal.plan_direction[0],Ai_Internal.plan_direction[0]+2]
            HitBox.hit_message(True)
            ship_destroyed = hit(shot,player)
            Ai_Internal.AI_map_list_personal[shot]  = AI_Personal_Tile_States.ALREADY_HIT_TILE 
            player.map_list[shot] = TileState.DESTROYED_SHIP    
            if len(Ai_Internal.attack_plan) == 0: ##rotates the attack plan 
                get_rotated_attack_plan()
        #if hit misses, updates data and changes attack plan                
        if player.map_list[shot] == TileState.WATER:
            HitBox.hit_message(False)
            Ai_Internal.AI_map_list_personal[shot]  = AI_Personal_Tile_States.ALREADY_MISSED_TILE
            player.map_list[shot] = TileState.MISSED_SHOT  
            get_rotated_attack_plan()

        # if a ship gets destroyed, end active shooting and checks for ending conditions
        if ship_destroyed == True:
            end_game = check_ending(player,AI)
            Ai_Internal.active_shooting = False
            Ai_Internal.attack_plan = None  

    ## no active shooting plan. Randomly shoots until it hits something             
    else:
        shot = random.randint(0,(GameOptions.X*GameOptions.Y)-1)
        while Ai_Internal.AI_map_list_personal[shot]  != AI_Personal_Tile_States.POSSIBLE_HIT_TILE: ##not shooting on the same tile
            shot = random.randint(0,(GameOptions.X*GameOptions.Y)-1)
        #checks if hit landed
        if player.map_list[shot] == TileState.ALIVE_SHIP:            
            HitBox.hit_message(True)
            ship_destroyed = hit(shot,player)
            if ship_destroyed:
                end_game = check_ending(player,AI)
            if not ship_destroyed:
                Ai_Internal.active_shooting = True
                Ai_Internal.active_shooting_tile = shot             
            Ai_Internal.AI_map_list_personal[shot]  = AI_Personal_Tile_States.ALREADY_HIT_TILE
            player.map_list[shot] = TileState.DESTROYED_SHIP  
        
        if player.map_list[shot] == TileState.WATER:
            HitBox.hit_message(False)
            Ai_Internal.AI_map_list_personal[shot]  = AI_Personal_Tile_States.ALREADY_MISSED_TILE
            player.map_list[shot] = TileState.MISSED_SHOT  
    return shot, end_game