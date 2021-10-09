from os import pipe
import pygame, pygame.display, pygame.image, pygame.transform, pygame.event, pygame.font, pygame.time, pygame.mixer
from pygame.constants import K_SPACE
import sys, random
pygame.init()
pygame.mixer.init()

# Creating Window
ScreenWidth = 320
ScreenHeight = 640
GameWindow = pygame.display.set_mode([ScreenWidth, ScreenHeight])
pygame.display.set_caption("Crazy Bird by VishuCool")

# Game Specific Variables
FPS = 30
Game_Imges = {} # Dictionary to store all images as key value pairs
Game_Sounds = {} # Dictionary to store all sounds as key value pairs
clock = pygame.time.Clock()
font = pygame.font.SysFont("footlight", 40)
base_x = 0
bird_index = 0
gravity = 1
bird_movement = 0
pipe_list = []
pipe_height = [400, 320, 500, 250]

""" Loading and Adding game images to dictionary """
Game_Imges["background"] = pygame.image.load("images/background.png") # Background
Game_Imges["base"] = pygame.image.load("images/base1.png") # Base

# Small size bird images for main game animation
Game_Imges["main_game_bird"] = [

    pygame.image.load("images/upflap1.png"),
    pygame.image.load("images/midflap1.png"),
    pygame.image.load("images/downflap1.png")

]

# Large bird images for welcome screen animation
Game_Imges["welcome_screen_bird"] = [

    pygame.image.load("images/upflap.png"),
    pygame.image.load("images/midflap.png"),
    pygame.image.load("images/downflap.png")
    
]

# Pipes
Game_Imges["pipe"] = pygame.image.load("images/pipe.png")
""" ------------------------------------------------------------------ """

""" Loading and Adding game sounds to dictionary """
Game_Sounds["hit"] = pygame.mixer.Sound("audio/hit.wav")
Game_Sounds["wing"] = pygame.mixer.Sound("audio/wing.wav")
Game_Sounds["point"] = pygame.mixer.Sound("audio/point.wav")
""" ------------------------------------------------------------------ """

""" Game Functions """
def moving_base():
    global base_x
    GameWindow.blit(Game_Imges["base"], (base_x, 500))
    GameWindow.blit(Game_Imges["base"], (base_x + 333, 500))
    if base_x > -333:
        base_x -= 3
    else:
        base_x = 0
    

def bird_animation():
    global Bird_rect
    new_bird = Game_Imges["main_game_bird"][bird_index]
    new_bird_rect = new_bird.get_rect()
    new_bird_rect.center = (80, Bird_rect.centery)
    return new_bird, new_bird_rect


def creating_pipes():
    random_pipe = random.choice(pipe_height)
    lower_pipe = Game_Imges["pipe"].get_rect(midtop = (350, random_pipe ))
    upper_pipe = Game_Imges["pipe"].get_rect(midbottom = (350, random_pipe - 200 ))
    return upper_pipe, lower_pipe


def blitting_pipes(p_list):
    """ Function for blitting pipes on screen """
    for pipes in p_list:    
        if pipes.bottom >= 540:
            GameWindow.blit(Game_Imges["pipe"], pipes)
        else:
            flip_pipe = pygame.transform.flip(Game_Imges["pipe"], False, True)
            GameWindow.blit(flip_pipe, pipes)


def pipes_velocity(p_list):
    """ This function returns a new list in which pipes are moving in -x directiuon """
    for pipes in p_list:
        pipes.centerx -= 4
    return p_list

""" Rects """
bird_select = Game_Imges["main_game_bird"][bird_index]
Bird_rect = bird_select.get_rect(center = (80, 200))
Bird_flap = pygame.USEREVENT
pygame.time.set_timer(Bird_flap, 200)

# Pipes
Spawn_Pipe = pygame.USEREVENT + 1
pygame.time.set_timer(Spawn_Pipe, 1200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                bird_movement = 0
                bird_movement -= 15
                Game_Sounds["wing"].play()
        
        if event.type == Bird_flap:
            if bird_index <= 1:
                bird_index += 1
            else:
                bird_index = 0

        if event.type == Spawn_Pipe:
            pipe_list.extend(creating_pipes())
            
            


    GameWindow.blit(Game_Imges["background"], (0, 0))

    # Bird
    bird_movement += gravity
    Bird_rect.centery += bird_movement
    bird_select, Bird_rect = bird_animation()
    GameWindow.blit(bird_select, Bird_rect)

    #Pipes
    new_pipe_list = pipes_velocity(pipe_list)
    blitting_pipes(new_pipe_list)

    # Base
    moving_base()

     
    

    

    pygame.display.update()
    clock.tick(FPS)