from enum import Enum
import pygame,os

pygame.init()

class Direction(Enum):
    '''Direction enum for ship placing direction'''
    RIGHT = 0
    LEFT = -1
    UP = 1

class GameMode(Enum):
    '''Class for game mode'''
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

class GameOptions:
    '''Options of the game. X = width of map in tiles, Y = height of map in tiles ,
       ships = playing ships, RECT_NUM = number of map tiles. Deafult is MEDIUM'''
    X = 8
    Y = 7
    ships = [3,2,1]  
    RECT_NUM = X*Y

    @classmethod
    def set_game_options(cls,mode):
        if mode == GameMode.SMALL:
            cls.X = 6 
            cls.Y = 7
            cls.ships = [3,1,0]                       
            cls.RECT_NUM = cls.X*cls.Y
        if mode == GameMode.LARGE:
            cls.X = 10
            cls.Y = 9
            cls.ships = [5,4,3]                       
            cls.RECT_NUM = cls.X*cls.Y


def is_over(rect, pos):
    return True if rect.collidepoint(pos[0], pos[1]) else False


current_directory = os.path.dirname(__file__)
assets_directory = os.path.join(current_directory, '..', 'Assets')


##Game options
INITIAL_SCREEN = width, height = 700, 350
AI_TIME_DELAY = 1000
SHOOTING_RANGE = 1

###Buttons bools
UP_DOWN_ARROW_DOWN = False
LEFT_RIGHT_ARROW_DOWN = False
MOUSE_DOWN = False
SPACE_DOWM = False

##colors
GREEN = (50,205,50)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (211,211,211)
RED = (255,0,0)
DARK_GREY = (70,130,180)

##rects
Start_button_rect = pygame.Rect((260, 270),(200,40))
Start_rect = pygame.Rect((325, 280),(100,20))
Easy_rect = pygame.Rect((170, 90),(75,75))
Medium_rect = pygame.Rect((320 , 90),(75,75))
Hard_rect = pygame.Rect((470, 90),(75,75))
RECTS = (Easy_rect,Medium_rect,Hard_rect)
background_options = pygame.Rect((0,0),INITIAL_SCREEN)

##font and texts
font_modes = pygame.font.Font('freesansbold.ttf', 20)
font_START_BUTTON = pygame.font.Font('freesansbold.ttf', 17)
text1 = font_modes.render("START", True, BLACK)
easy = font_START_BUTTON.render("Small", True, BLACK)
medium = font_START_BUTTON.render("Norm", True, BLACK)
hard =  font_START_BUTTON.render("Large", True, BLACK)
texts = (easy,medium,hard)

font_basic = pygame.font.Font('freesansbold.ttf', 20)
player_text = font_basic.render('Player', True, BLACK, GREY)
enemy_text = font_basic.render('Enemy', True, BLACK, GREY)
font = pygame.font.Font('freesansbold.ttf', 25)
font_hit_box = pygame.font.Font('freesansbold.ttf', 30)

Ending_text = font.render("END OF THE GAME", True, BLACK, WHITE)


###Score tables
##texts and fonts
font_score = pygame.font.Font('freesansbold.ttf', 17)
font_table_name = pygame.font.Font('freesansbold.ttf', 20)
table_enemy = font_table_name.render("Enemy", True, RED)
table_player = font_table_name.render("Player", True, GREEN)
Destroyer_text = font_score.render("Destroyers", True, BLACK)
Submarine_text = font_score.render("Submarines", True, BLACK)
Battleship_text = font_score.render("Battleships", True, BLACK)
score_texts = (Destroyer_text,Submarine_text,Battleship_text)
##rects
table_rect = pygame.Rect((20, 120),(160,90))
table_text_rect = pygame.Rect((20, 125),(140,20))
score_rect_player = (pygame.Rect((160, 125),(20,20)),pygame.Rect((160, 155),(20,20)),pygame.Rect((160, 185),(20,20)))
score_rect_AI = (pygame.Rect((160, 125+150),(20,20)),pygame.Rect((160, 155+150),(20,20)),pygame.Rect((160, 185+150),(20,20)))

##surfaces
table_surface = pygame.Surface((160, 90))
table_surface.fill(GREY)

#GUI Recta
player_name_rect = pygame.Rect((50, 10),(75,24))
player_name_reset  = pygame.Surface((75, 24))
player_name_reset.fill(GREY)
message_box_reset = pygame.Surface((525, 30))
hit_box_reset = pygame.Surface((70, 30))
message_box_reset.fill(WHITE)
hit_box_reset.fill(WHITE)



