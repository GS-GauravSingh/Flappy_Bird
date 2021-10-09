import pygame, pygame.display, pygame.image, pygame.transform, pygame.event, pygame.font, pygame.time, pygame.mixer
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

""" Loading and Adding game images to dictionary """
Game_Imges["background"] = pygame.image.load("images/background.png") # Background
Game_Imges["base"] = pygame.image.load("images/base1.png") # Base

# Small size bird images for main game animation
Game_Imges["upflap1"] = pygame.image.load("images/upflap1.png") 
Game_Imges["midflap1"] = pygame.image.load("images/midflap1.png")
Game_Imges["downflap1"] = pygame.image.load("images/downflap1.png")

# Large bird images for welcome screen animation
Game_Imges["upflap"] = pygame.image.load("images/upflap.png") 
Game_Imges["midflap"] = pygame.image.load("images/midflap.png")
Game_Imges["downflap"] = pygame.image.load("images/downflap.png")

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
        base_x -= 2
    else:
        base_x = 0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    GameWindow.blit(Game_Imges["background"], (0, 0))
    moving_base()


    pygame.display.update()
    clock.tick(FPS)
