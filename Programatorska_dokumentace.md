# Sections
1. [Battleships.py](#battleships)
2. [AI_internal_logic.py](#ai_internal_logic)
3. [Player_internal_logic.py](#player_internal_logic)
4. [Ships.py](#ships)
5. [Initializations.py](#initializations)
6. [Options_screen.py](#options_screen)
7. [Ending.py](#ending)
8. [Globals_constants.py](#global_constants)

# [Battleships](Battleships/Battleships.py)
## Options screen and initiation
Main program file.  
Starts by initiating *Options sequence* from [Options_screen.py](#options_screen)
by running *Options_screen.start_options_menu()* function.  
Then it initiates game options and main screen from [Initializations.py](#initializations)
by running *Initialize_Main_Screen()* based on chosen mode and remebers necesseary data.  
Creates two instances of *Player* class from [Player_internal_logic.py](#player_internal_logic) one
for **Player** and one for **AI**.  
Initiates placement of ships for AI [AI_place_ships()](#def-ai_place_ships)
## Main loop
### All modes
Checks if mouse is over the map and if the mouse moved to a different tile. If it did,
then it calculates new positions to highlight. *is_over(rec, mouse_pos)* is used to check if mouse is over the map
and over whioh tile.  
At the end updates checks if the map has changed. If it did, updates the map first then it updates new active tile to be highlited.  
### Placing mode(**Player** only)
Main loop starts with *Placing mode*.  
First it checks if there are still ships to be placed or if it should switch to *Shooting mode*.  
*get_whole_ship_location()* calculaes tile positions of active ship based on active tile.(The tile that the mouse is over)  
Then pygame checks for *key events*.  
If *up* or *right* arrow key was pressed changes the type(up arrow key) of avalaible ships or the direction(right arrow key) of the current ship.  
If there was a *mouse click* creates an insatnce of class [Ship](#class-ship) based on current position.  
After all the ships has been placed, switches to *Shooting Mode*
### Shooting mode(**Player**)
Waits for player to *Mouse click* on a tile.  
If the player clicks on a tile that has already been shot at, an error message shows on *message box*. 
Once the player clicks on a tile that has not been shot at yet, shoots at the tile and reveals if it hit or missed with check_if_hit() function.  
Updates the necesseary information like *scoreboard* and *messsage box* etc.  
Chedcks for ending with check_ending() func.  
Player continues to **AI** turn by clicking.
Active PLayer changes and the function blit_change_map() changes the map based on the new active player.
### Shooting mode(**AI**) 
**AI** starts with a small delay that can be skipped by clicking.  
Starts AI turn with func start_AI_turn().  More in [AI_turn](#def-start_ai_turnplayerai)  
Updates necessary data.
Checks for ending.  
Player continues by *Mouse click*  
Changes Active Player and changes map.  
## Ending
Starts ending screen from ***Ending.py***

# [AI_internal_logic](Battleships/AI_internal_logic.py)
## class Ai_Internal:
    Internal globals for AI. Has these attributes:
    active_shooting
    attack_plan = plan for shooting in next rounds
    plan_direction = direction of the plan of attack
    active_shooting_tile = tile around which creates an attack plan
    largest_remaining_ship_size = size of the latgest remaning ship of player. For lenght of the attack plan.
    AI_map_list_personal = AI's own memory of players ships. Basically what would AI see on the screen if it was a plyer.   

## def start_AI_turn(player,AI)
Main function of AI.  
General idea: At first the AI randomly shoots at available tiles until it hits a player's ship.
Once a ship is hit, *active_shooting* is activated around the *active_shooting_tile*. Then it computes *Attack_plan*  
The main idea of attack plan is, that a ship must be around the *active_shooting_tile*. Shoots in all directions (the direction plan is pre set. Should randomize it.) until the ship is destroyed, rotating attack_plan if it misses a shot. Switches of active shooting and begins randomly shooting again.  
Active shooting on:  
If there's no *Attack_plan* calculates attack plan with get_attack_plan()  
Takes the next shot from *Attack_plan* and checks with it's own *AI_map_list_personal* memory of the shot is viable. It did noi shoot there before. Takes next shot from *attack_plan* until it finds a viable one. If the *attack_plan* is empty rotates the attack plan.  
Shoots the shot and checks if it hit.  
On a hit, updates data. If a ship was destroyed, ends active shooting. If the *attack_plan* is at zero, rotates the plan.  
On a miss, updates data and rotates plan.

## def get_attack_plan()
Calculates attack plan. Positions of tiles to shoot at based on given position, direction of the plan and the given lenght.

## def AI_place_ships()
For all ship types of AI based on the game options creates class ***Ship*** instance of that ship. Randomly chooses direction and a tile from map tiles. Then it calculates the active tiles of the ship with get_whole_ship_location() and tries to place it. Updates the data or randomly chooses another location.

# [Player_internal_logic](Battleships/Player_internal_logic.py)
## class Player:
    Main class for storing parameters of PLayer and AI
        self.ships_to_place = ships to be placed at the begining
        self.remaining_ships = keeping track of ships not destroyed yet
        self.map_list = list map of ships placements for recreating the map 
        self.ship_locations = dict for ship locations. For registering hits and keeping track of ships health
        self.score_box = score box of player
## def check_ending(Player, AI)
Checks if any ships remain after a ship was destroyed. End the game if there are no ships left for **Player** or **AI**
## def hit(num,player)
Checks if given position hits any ship based on given active player. If it hits, subtracts a point from the ships health and checks if a ship was detroyed.
## def check_if_hit(AI,active_tile)
Has some additional data updates for player on top of def hit()

# [Ships](Battleships/Ships.py)
## Class ShipsTypes(Enum)
Enum class for ship types. Int 0,1,2 for rotating through ship types when placing.

## class Ship
Ship instances with size and health based on the ship type. Tracks health of ships and their locations.
 
## def get_whole_ship_location()
Calculates the positions of tiles of the given ship type based on given active tile.  

## def rotate_available_ships()
Rotates through available remaining ships when placing them and changing the ship type.  

## def placing_ship()
Tries to place the ship based on fiven positions during *Placing mode*. Shows error message when unable to place.

# [Initializations](Battleships/Initializations.py)
## class Screen
Static class used for blitting screen and storing wifth and height of the screen.

## classes ScoreBox, MessageBox, HitBox
Necessary data for updating and blitting Score, Messages and Hits.

## def Initialize_Options_Screen()
loads neccesary data for options screen and blits the screen 

## def Initialize_Main_Screen(mode)
Loads and initializes neccesary data for main screen and blits the screen. 

# [Options_screen](Battleships/Options_screen.py)
Initializes and blits the options screen. Checks for *Key Events*
Starts the game when *Mouse click* on Start rectangle or *spacebar* key pressed.  
Left and Right arrow keys rotate difficutly options.  

# [Ending](Battleships/Ending.py)
Initializes and blits the ending screen.

# [Global_constants](Battleships/Globals_constants.py)
Globals constants for the game.
## class GameOptions
    Options of the game
    X = width in map tiles
    Y = height in map tiles
    ships = numbers of ships to place based on types
    RECT_NUM = X*Y (number of tiles in the game)
