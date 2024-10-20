import pygame, sys
from Globals_constants import GameOptions, WHITE, Ending_text
from Initializations import Screen
#Ending seqeunce
def start_ending_sequence(clock):
    Ending_rect = pygame.Rect((120, (Screen.get_size()[0] // 2)-50),(50 + (GameOptions.X*75),100))
    help_num = Ending_rect.center
    ednding_text_rect = ((help_num[0]-100,help_num[1]-10),(100,40))
    Ending_surface =  pygame.Surface((50 + (GameOptions.X*75),100))
    Ending_surface.fill(WHITE)
    Screen.display.blit(Ending_surface,Ending_rect)
    Screen.display.blit(Ending_text, ednding_text_rect)

    while(True):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
