from Globals_constants import *


class Screen:
    '''Abstraction for screen blitting with the size of screen info.'''
    display = None
    width = None
    height = None

    @classmethod
    def initiate_screen(cls, size):
        cls.width = size[0]
        cls.height = size[1] 
        cls.display = pygame.display.set_mode(size)

    @classmethod
    def get_size(cls):
        return(cls.width, cls.height)
    

class ScoreBox:
    '''Data for Player's scoreboards'''
    score_box_font = None
    def __init__(self,score_box_rect):
        self.score_box_rect = score_box_rect

    def update_box(self,text,ship_type_value):
        help_text_surface = self.score_box_font.render(text, True, BLACK,GREY)
        Screen.display.blit(help_text_surface,self.score_box_rect[ship_type_value])
        

class MessageBox:
    '''Box for messages'''
    message_box_rect = None
    message_box_reset = None
    message_box_font = None

    @classmethod
    def initiate(cls,message_mox_rect , message_box_reset , message_box_font ):
        cls.message_box_font = message_box_font
        cls.message_box_rect = message_mox_rect
        cls.message_box_reset = message_box_reset

    @classmethod
    def new_message(cls,message):
        Screen.display.blit(message_box_reset , cls.message_box_rect)
        Screen.display.blit(cls.message_box_reset, cls.message_box_rect)
        text1 = cls.message_box_font.render(message, True, BLACK, WHITE)
        Screen.display.blit(text1, cls.message_box_rect) 


class HitBox:
    '''Box for announcing hits or misses'''
    hit_box_rect = None
    hit_box_reset = None
    hit_box_font = None

    @classmethod
    def initiate(cls,hit_box_rect , hit_box_reset , hit_box_font ):
        cls.hit_box_font = hit_box_font
        cls.hit_box_rect = hit_box_rect
        cls.hit_box_reset = hit_box_reset
    
    
    @classmethod
    def hit_message(cls,hit):
        Screen.display.blit(cls.hit_box_reset, cls.hit_box_rect)
        if hit:
            message_surface = cls.hit_box_font.render("Hit", True, GREEN, WHITE)
        else:
            message_surface = cls.hit_box_font.render("Miss", True, RED, WHITE)
        Screen.display.blit(message_surface, cls.hit_box_rect) 

class MainTiles:
    '''Object for keeping main map tiles'''
    def __init__(self,water_tile,ship_tile, hit_tile, miss_tile):
        self.water_tile = water_tile
        self.ship_tile = ship_tile 
        self.hit_tile = hit_tile
        self.miss_tile = miss_tile

    def get_tiles(self):
        return ((self.water_tile, self.ship_tile, self.hit_tile, self.miss_tile))


def get_path_to_assets(path):
    return (os.path.join(assets_directory, path))

#loads main map tiles
def load_main_tiles():
    water_tile = pygame.image.load(get_path_to_assets('Ocean_tile.xcf')).convert()      #basic water tile surface
    ship_tile = pygame.image.load(get_path_to_assets('Ship_tile.xcf')).convert()   #higlighted tile surface
    hit_tile = pygame.image.load(get_path_to_assets('Hit_tile.xcf')).convert() 
    miss_tile = pygame.image.load(get_path_to_assets('Miss_tile.xcf')).convert() 

    ship_tile_highlited = pygame.image.load(get_path_to_assets('Ship_tile_Highlited.xcf')).convert()
    water_tile_highlited = pygame.image.load(get_path_to_assets('Highlited_tile.xcf')).convert()
    hit_tile_highlited = pygame.image.load(get_path_to_assets('Hit_tile_Highlited.xcf')).convert()
    miss_tile_highlited = pygame.image.load(get_path_to_assets('Miss_tile_Highlited.xcf')).convert()

    map_tiles_surface = MainTiles(water_tile, ship_tile, miss_tile, hit_tile) 
    map_tiles_highlited_surface = MainTiles(water_tile_highlited,ship_tile_highlited,miss_tile_highlited,hit_tile_highlited)
    
    
    return  map_tiles_surface, map_tiles_highlited_surface

#loads neccesary data for options screen and blits the screen 
def Initialize_Options_Screen():
    ##initial blitting
    pygame.display.set_caption('Battleships Options')
    Screen.initiate_screen(INITIAL_SCREEN)

    game_option_surface = pygame.image.load(get_path_to_assets('Ship_tile.xcf')).convert()
    game_option_surface_highlited = pygame.image.load(get_path_to_assets('game_option_highlited.xcf')).convert()


    background_surface = pygame.image.load(get_path_to_assets('background_options.xcf')).convert()
    Start_button_surface = pygame.Surface((200 ,40))
    Start_button_surface.fill(WHITE)
    Screen.display.blit(background_surface,background_options)
    Screen.display.blit(Start_button_surface, Start_button_rect)
    Screen.display.blit(text1, Start_rect) 

    ##options rects blitting
    for x in range(len(RECTS)):
        Screen.display.blit(game_option_surface, RECTS[x])
        rect = pygame.Rect((182 + (x*150), 170),(75,40))
        Screen.display.blit(texts[x], rect) 
    
    return game_option_surface, game_option_surface_highlited


#loads and initializes neccesary data for main screen and blits the screen. 
def Initialize_Main_Screen(mode):
    GameOptions.set_game_options(mode)
    ###Display innitiation
    pygame.display.set_caption('Battleships')

    screen_size = ((250 + (GameOptions.X*75) , 150 + (GameOptions.Y*75) ))
    Screen.initiate_screen(screen_size)
    

    background_main = pygame.Surface(Screen.get_size()) 
    background_main.fill(DARK_GREY)
    
    map_tiles_surface, map_tiles_highlited_surface = load_main_tiles()

    ###Create field of rects for tiles. Positioned for map.
    tilerect = map_tiles_surface.water_tile.get_rect()
    tilerect = tilerect.move(200, 100)
    positioned_rects_for_tiles = []
    for y in range(GameOptions.Y):
        for x in range(GameOptions.X):
            copy_tile = tilerect.copy()
            copy_tile = copy_tile.move(75*x, 75*y)
            positioned_rects_for_tiles.append(copy_tile)


    ###Score tables
    ScoreBox.score_box_font = font_score
    player_score_board = ScoreBox(score_rect_player)
    AI_score_board = ScoreBox(score_rect_AI)

    ###GUI Initiation
    help_var_shift = 100
    if GameOptions.X == 6: help_var_shift = 175
    message_box_rect = pygame.Rect((((GameOptions.X*75)/2) - help_var_shift, 55),(525,30))
    hit_box_rect = pygame.Rect(((((GameOptions.X*75)/2) - help_var_shift) + 530, 55),(70,30))


    ###Hit box and Message box initiation
    HitBox.initiate(hit_box_rect,hit_box_reset, font_hit_box)
    MessageBox.initiate(message_box_rect,message_box_reset, font_basic)    


    #initial blitting of the map 
    background = pygame.transform.smoothscale(background_main, Screen.get_size())  
    Screen.display.blit(background, (0, 0))                 #blits the Screen.display    
    Screen.display.blit(player_name_reset, player_name_rect)
    Screen.display.blit(player_text, player_name_rect) 
    Screen.display.blit(message_box_reset, message_box_rect)  
    Screen.display.blit(hit_box_reset,hit_box_rect) 
    MessageBox.new_message("Place Ships")
    for x in positioned_rects_for_tiles:                                 #blits beginning tiles
        Screen.display.blit(map_tiles_surface.water_tile, x)

    # Initial blitting of score tables
    table_score_name = pygame.Rect((20, 95),(100,90))
    PLAYERS = 2
    for y in range(PLAYERS):
        help_rect1 = table_rect.move(0,y*150)
        Screen.display.blit(table_surface,help_rect1)
        for x in range(3):
            help_rect2 = table_text_rect.move(0, (x*30) + (y*150))
            Screen.display.blit(score_texts[x],help_rect2)
    Screen.display.blit(table_player,table_score_name)
    table_score_name = table_score_name.move((0,150))
    Screen.display.blit(table_enemy,table_score_name)
    for x in range(len(GameOptions.ships)):
        help_text = str(GameOptions.ships[x])
        player_score_board.update_box(help_text,x)
        AI_score_board.update_box(help_text,x)

    # rectangle for the map
    map_rect = pygame.Rect((200,100),(GameOptions.X*75,GameOptions.Y*75))

    return positioned_rects_for_tiles, map_rect, player_score_board, AI_score_board, map_tiles_surface, map_tiles_highlited_surface