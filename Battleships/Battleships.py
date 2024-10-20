# Hra na Lode
# Peter Vidlička
# 1.ročník 2023/2024
# Programování 1

import sys, pygame, Ending, Options_screen
from Globals_constants import *
from Ships import *
from Initializations import Initialize_Main_Screen, Initialize_Options_Screen, Screen ,HitBox, MessageBox
from Player_internal_logic import Player, TileState, hit, check_ending, check_if_hit
from AI_internal_logic import start_AI_turn, AI_place_ships

#returns the number of the rectangle that the mouse is over
def get_new_active_tile(pos, tiles):
    for x in range(len(tiles)):         #checks all rectangles if the mouse is over them
        if is_over(tiles[x], pos):
            return(x)

#swtiches displayed map
def blit_change_map(player,tiles,surfaces):
    for x in range(len(tiles)):                                
        surface = surfaces[player.map_list[x].value]
        Screen.display.blit(surface, tiles[x])


####Options part of the game
###start initiations
clock = pygame.time.Clock()  
chosen_mode = Options_screen.start_options_menu(clock)

####Main game
#Options initiation
POSITIONED_RECTS_FOR_TILES, MAP_RECT, player_score_board, AI_score_board, map_tiles_surface, map_tiles_highlited_surface  = Initialize_Main_Screen(chosen_mode)

PLAYER = Player(GameOptions.ships.copy(),GameOptions.RECT_NUM, player_score_board)
AI = Player(GameOptions.ships.copy(),GameOptions.RECT_NUM,AI_score_board)

AI_place_ships(AI)

###Working bools
##game mod bools
MOUSE_DOWN = True
End_Game = False
placing_mode = True
shooting_mode = False
##step bools
ctc = False
AI_turn = False
change_map = False
##other
active_player = PLAYER
start_time = None

#Vars
direction = Direction.RIGHT
ship_tiles = (0,0,0)
active_tile = [0,1,2,0]
active_ship = ShipsTypes.SMALL

###Main Game Loop
while End_Game == False:

    map_change_queue = []               #queue of blit changes for map
    mouse_pos = pygame.mouse.get_pos()  #x, y coordinates of mouse
    new_active_tile = None

    #if still placing ships, checks if any remaining
    if placing_mode == True:
        if not all(ships == 0 for ships in PLAYER.ships_to_place):
            if PLAYER.ships_to_place[active_ship.value] == 0:
                active_ship = ShipsTypes(rotate_available_ships(Direction.RIGHT,active_ship.value, PLAYER.remaining_ships) )    
            active_tile_size = get_size_by_type(active_ship)
        else:
            active_tile_size = SHOOTING_RANGE
            placing_mode = False
            ctc = True
            MessageBox.new_message("Battleships placed. Click to start.")
            
    ##checking if mouse moved and highlights active tiles     
    if is_over(MAP_RECT, mouse_pos):       #when the mouse is inside the map highlits the tile          
        if len(active_tile) == active_tile_size and is_over(POSITIONED_RECTS_FOR_TILES[active_tile[0]], mouse_pos):  #highlited tile didn't change
            pass
        else:  
            new_position = get_new_active_tile(mouse_pos, POSITIONED_RECTS_FOR_TILES)
            new_active_tile = get_whole_ship_location(new_position, active_tile_size, direction,GameOptions.X,GameOptions.RECT_NUM)
            for x in active_tile: map_change_queue.append(x)  


    if AI_turn and (pygame.time.get_ticks() - start_time) > AI_TIME_DELAY:
        shot, End_Game = start_AI_turn(PLAYER,AI)
        AI_turn = False
        map_change_queue.append(shot)
        start_time = None
        ctc = True
 
   
    buttons = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()     
        if event.type == pygame.KEYDOWN:
            ##changes size of ships
            if event.key == pygame.K_UP:
                if placing_mode == True:
                    active_ship = ShipsTypes(rotate_available_ships(Direction.RIGHT,active_ship.value, PLAYER.remaining_ships) )                 
            if event.key == pygame.K_DOWN:
                if placing_mode == True:
                    active_ship = ShipsTypes(rotate_available_ships(Direction.LEFT,active_ship.value, PLAYER.remaining_ships))
            ##changes direction of ships
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                if placing_mode == True:
                    if direction == Direction.RIGHT: direction = Direction.UP
                    else:direction = Direction.RIGHT
                    for x in active_tile: map_change_queue.append(x)
                    active_tile = []
            if event.key == pygame.K_SPACE and MOUSE_DOWN == False:
                buttons = (True, False)

    ##checks for map change
    if buttons[0] and ctc and MOUSE_DOWN == False:
        change_map = True
        ctc = False
        MOUSE_DOWN = True
    if buttons[0] and start_time != None and MOUSE_DOWN == False:
        start_time -= AI_TIME_DELAY 
        MOUSE_DOWN = True
    
    #placing or shooting if inside map based on current mode
    if is_over(MAP_RECT, mouse_pos):   
        ##player shooting. Checks if possible to shoot and shoots if possible.      
        if buttons[0] and shooting_mode and MOUSE_DOWN == False:
            if AI.map_list[active_tile[0]] == TileState.WATER:
                MessageBox.new_message("Shots fired (click to continue)")               
                shooting_mode = False
                ctc = True
                if check_if_hit(AI,active_tile):End_Game = check_ending(PLAYER,AI)  
                map_change_queue.append(active_tile[0])           
            else:
                MessageBox.new_message("Cannot shoot. (select different tile)")

            MOUSE_DOWN = True

        ###placing of ships at the beginning
        if buttons[0] and placing_mode and MOUSE_DOWN == False: 
            placing_ship(PLAYER,active_tile, active_ship)
            MOUSE_DOWN = True
    if buttons[0] == False:
        MOUSE_DOWN = False
        
    ##changes map based on current player and switches all the necessary infomation
    if change_map:
        new_active_tile = active_tile       
        if active_player == PLAYER: active_player = AI
        else: active_player = PLAYER
        blit_change_map(active_player,POSITIONED_RECTS_FOR_TILES, map_tiles_surface.get_tiles())
        if active_player == AI:            
            shooting_mode = True
            MessageBox.new_message("Shooting")
            Screen.display.blit(player_name_reset,player_name_rect)
            Screen.display.blit(player_text,player_name_rect)

        if active_player == PLAYER:
            start_time = pygame.time.get_ticks()
            AI_turn = True
            MessageBox.new_message("Enemy Shooting")
            Screen.display.blit(player_name_reset,player_name_rect)
            Screen.display.blit(enemy_text,player_name_rect)
        change_map = False



    ##updates the changed tiles from queue to display them
    while len(map_change_queue) > 0:                #queue for changing tiles to its current map state
        change_rec = map_change_queue.pop()
        if active_player == PLAYER:surface_type = PLAYER.map_list[change_rec].value
        if active_player == AI:surface_type = AI.map_list[change_rec].value
        Screen.display.blit(map_tiles_surface.get_tiles()[surface_type], POSITIONED_RECTS_FOR_TILES[change_rec])

    #if theres a new active tile changes its appearance based on the current map and player
    if new_active_tile != None:
        active_tile = []
        if active_tile_size == SHOOTING_RANGE:
            if active_player == PLAYER:help_num = PLAYER.map_list[new_active_tile[0]].value
            if active_player == AI:help_num = AI.map_list[new_active_tile[0]].value
            surface_type = map_tiles_highlited_surface.get_tiles()[help_num]
        else:
            surface_type = map_tiles_surface.ship_tile
        for x in range(len(new_active_tile)):            
            Screen.display.blit(surface_type, POSITIONED_RECTS_FOR_TILES[new_active_tile[x]])  
            active_tile.append(new_active_tile[x])
        new_active_tile = None

    
    pygame.display.update()
    clock.tick(60)

Ending.start_ending_sequence(clock)

