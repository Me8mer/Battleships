from Initializations import Initialize_Options_Screen, Screen
from Globals_constants import RECTS, Start_button_rect, is_over, GameMode
import pygame, sys


def start_options_menu(clock):
    game_option_surface, game_option_surface_highlited = Initialize_Options_Screen()

    ###Options game Loop
    Screen.display.blit(game_option_surface_highlited, RECTS[1])
    start_game = False
    MOUSE_DOWN =False
    active_tile = GameMode.MEDIUM #difficulty option tile
    while start_game == False:
        new_active_tile = None
        mouse_pos = pygame.mouse.get_pos()
    
        #checks for clicks on start button
        buttons = pygame.mouse.get_pressed()
        if is_over(Start_button_rect, mouse_pos):        
            if buttons[0] and MOUSE_DOWN == False:
                MOUSE_DOWN = True
                start_game = True
                continue

        #checks for button presses to toggle difficulty optiions or start the game      
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    new_active_tile = GameMode((active_tile.value + 1) % 3)  
                if event.key == pygame.K_LEFT:  
                    new_active_tile = GameMode((active_tile.value - 1) % 3)  
                if event.key == pygame.K_SPACE:
                    SPACE_DOWM = True
                    start_game = True
                    continue
        
        if new_active_tile != None:
            Screen.display.blit(game_option_surface, RECTS[active_tile.value])
            Screen.display.blit(game_option_surface_highlited, RECTS[new_active_tile.value])
            active_tile = new_active_tile 
        pygame.display.update()
        clock.tick(60)

    return active_tile
