from os import pipe
import pygame, pygame.display, pygame.image, pygame.transform, pygame.event, pygame.font, pygame.time, pygame.mixer
from pygame.constants import K_RETURN, K_SPACE
import sys, random, os
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
font = pygame.font.SysFont("footlight", 32)
base_x = 0
bird_index = 0
gravity = 1
bird_movement = 0
pipe_list = []
pipe_height = [400, 320, 500, 250]
game_on = True
game_start = False
score = 0
can_score = True

# Creating HiScore File if not exists
if not (os.path.exists("hiscore.txt")):
    with open("hiscore.txt", "w") as f:
        f.write("0")
    
with open("hiscore.txt", "r") as f:
        highscore = f.read()
    



# Colors
black = (0, 0, 0)

""" Loading and Adding game images to dictionary """
Game_Imges["background"] = pygame.image.load("images/background.png") # Background
Game_Imges["base"] = pygame.image.load("images/base1.png") # Base
Game_Imges["welcome"] = pygame.image.load("images/welcome.png") # Welcome message

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
def welcome_screen():
    with open("hiscore.txt", "r") as f:
        highscore = f.read()
   
    base_x = 0
    index_bird = 0
    bird_move = -2

    
    flap_bird = pygame.USEREVENT
    pygame.time.set_timer(flap_bird, 200)

    while True:
        GameWindow.blit(Game_Imges["background"], (0, 0))
        text_screen(f"Score:{str(score)}", black, 5, 5)
        text_screen(f"HiScore:{str(highscore)}", black, 180, 5)
        GameWindow.blit(Game_Imges["welcome"], (-20, 30))
        # Bird
        select_bird = Game_Imges["welcome_screen_bird"][index_bird]
        rect_bird = select_bird.get_rect(center = (bird_move, 300))
        bird_move += 1
        if bird_move >= 150:
            bird_move = 150
        
        # Base
        base_x -= 1
        GameWindow.blit(Game_Imges["base"], (base_x, 500))
        GameWindow.blit(Game_Imges["base"], (base_x + 333, 500))
        if base_x > -333:
            base_x -= 3
        else:
            base_x = 0
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    return
            
            if event.type == flap_bird:
                if index_bird <= 1:
                    index_bird += 1
                else:
                    index_bird = 0
        GameWindow.blit(select_bird, rect_bird)
            
        pygame.display.update()
        clock.tick(FPS)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    GameWindow.blit(screen_text, (x, y))


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
    """ This function returns a new list in which pipes are moving in -x direction """
    for pipes in p_list:
        pipes.centerx -= 4
    return p_list


def check_collision(p_list):
    global Bird_rect, score
    
    for pipes in p_list:

        if pipes.colliderect(Bird_rect):
            with open("hiscore.txt", "w") as f:
                    f.write(str(highscore))
            text_screen(f"Score: {str(score)}", black, 110, 20)
            text_screen(f"HiScore: {str(highscore)}", black, 100, 475)
            text_screen("Game Over!!", black, 70, 170)
            text_screen("Press Enter to Continue", black, 6, 210)
            return False
    
    if Bird_rect.top < -5:
        with open("hiscore.txt", "w") as f:
            f.write(str(highscore))
        text_screen(f"Score: {str(score)}", black, 110, 20)
        text_screen(f"HiScore: {str(highscore)}", black, 100, 475)
        text_screen("Game Over!!", black, 70, 170)
        text_screen("Press Enter to Continue", black, 6, 210)
        return False
    
    if Bird_rect.bottom > 500:
        with open("hiscore.txt", "w") as f:
             f.write(str(highscore))
        text_screen(f"Score: {str(score)}", black, 110, 20)
        text_screen(f"HiScore: {str(highscore)}", black, 100, 475)
        text_screen("Game Over!!", black, 70, 170)
        text_screen("Press Enter to Continue", black, 6, 210)
        return False
    return True


def point_check():
    global new_pipe_list, score, can_score, highscore 
    if new_pipe_list:
        for pipe in new_pipe_list:
            if  pipe.centerx == 70 and can_score:
                Game_Sounds["point"].play()
                score += 1
                if score >= int(highscore):
                    highscore = score
                
                can_score = False
            if pipe.centerx < 0:
                can_score = True 

    text_screen(f"{str(score)}", black, 150, 50)


""" Rects """
bird_select = Game_Imges["main_game_bird"][bird_index]
Bird_rect = bird_select.get_rect(center = (80, 200))
Bird_flap = pygame.USEREVENT
pygame.time.set_timer(Bird_flap, 200)

# Pipes
Spawn_Pipe = pygame.USEREVENT + 1
pygame.time.set_timer(Spawn_Pipe, 1200)

welcome_screen()

while True:
    # welcome_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and game_on:
                bird_movement = 0
                bird_movement -= 15
                Game_Sounds["wing"].play()

            if event.key == K_RETURN and game_on == False:
                game_on = True
                bird_movement = 0
                new_pipe_list.clear()
                Bird_rect.center= (80, 200)

        if event.type == Bird_flap:
            if bird_index <= 1:
                bird_index += 1
            else:
                bird_index = 0

        if event.type == Spawn_Pipe:
            pipe_list.extend(creating_pipes())


    GameWindow.blit(Game_Imges["background"], (0, 0))

    if game_on:
        # Bird
        bird_movement += gravity
        Bird_rect.centery += bird_movement
        bird_select, Bird_rect = bird_animation()
        GameWindow.blit(bird_select, Bird_rect)

        #Pipes
        new_pipe_list = pipes_velocity(pipe_list)
        blitting_pipes(new_pipe_list)

        point_check()

    # Base
    moving_base()

    #collision
    game_on = check_collision(new_pipe_list)
     
    

    

    pygame.display.update()
    clock.tick(FPS)
