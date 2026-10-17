import random

import pygame
import os
pygame.init()

width = 900
height = 700
screen = pygame.display.set_mode((width, height))
pygame.mixer.init()

BOUNCE_SOUND = pygame.mixer.Sound("assets/sound/bounce.mp3")
#BOUNCE_SOUND.set_volume(0.1)

SPLAT_SOUND = pygame.mixer.Sound("assets/sound/splat.mp3")
SPLAT_SOUND.set_volume(0.4)

SQUACH_SOUND1 = pygame.mixer.Sound("assets/sound/squach1.mp3")
SQUACH_SOUND1.set_volume(0.7)

SQUACH_SOUND2 = pygame.mixer.Sound("assets/sound/squach2.mp3")
SQUACH_SOUND2.set_volume(0.7)

SQUACH_SOUND3 = pygame.mixer.Sound("assets/sound/squach3.mp3")
SQUACH_SOUND3.set_volume(0.7)

SQUACH_SOUND4 = pygame.mixer.Sound("assets/sound/squach4.mp3")
SQUACH_SOUND4.set_volume(0.9)

SQUACH_SOUND5 = pygame.mixer.Sound("assets/sound/squach5.mp3")
SQUACH_SOUND5.set_volume(0.7)

SQUACH_LIST = [SQUACH_SOUND1, SQUACH_SOUND2, SQUACH_SOUND3 , SQUACH_SOUND4 , SQUACH_SOUND5]

HAND1_NR = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "Hand1B.png")).convert_alpha(), 0.6)
HAND1 = pygame.transform.rotate(HAND1_NR , 45)

HAND_DRAG1_NR = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "Hand_Drag1B.png")).convert_alpha(), 0.6)
HAND_DRAG1 = pygame.transform.rotate(HAND_DRAG1_NR , 45)

SOE_VANILLA = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "SOE_VANILLA.png")).convert_alpha(), 2.5)
SOE_S_PRESSED = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "SOE_S_PRESSED.png")).convert_alpha(), 2.5)

SOE_RAHMEN = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "SOE_RAHMEN.png")).convert_alpha(), 2.5)

ULT_RAHMEN = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "ULT_RAHMEN_2.png")).convert_alpha(), 6)
ULT_BALKEN = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "ULT_BALKEN_3.png")).convert_alpha(), 6)

START_V = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "START_V.png")).convert_alpha(), 2.5)
START_PRESSED = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "START_PRESSED.png")).convert_alpha(), 2.5)

OPTIONS_V = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "OPTIONS_V.png")).convert_alpha(), 2.5)
OPTIONS_PRESSED = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "OPTIONS_PRESSED.png")).convert_alpha(), 2.5)

EXIT_V = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "EXIT_V.png")).convert_alpha(), 2.5)
EXIT_PRESSED = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "EXIT_PRESSED.png")).convert_alpha(), 2.5)

ARROW_LEFT = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "ARROW_LEFT.png")).convert_alpha(), 5)
ARROW_LEFT_PRESSED = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "ARROW_LEFT_PRESSED.png")).convert_alpha(), 5)

ARROW_RIGHT = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "ARROW_RIGHT.png")).convert_alpha(), 5)
ARROW_RIGHT_PRESSED = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "ARROW_RIGHT_PRESSED.png")).convert_alpha(), 5)

RED_BALL = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "RED_BALL.png")).convert_alpha() , 3)
RED_BALL_GREY = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "RED_BALL_GREY.png")).convert_alpha() , 3)
RED_BALL_WHITE = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "RED_BALL_WHITE.png")).convert_alpha() , 3)

BLUE_BALL = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "BLUE_BALL.png")).convert_alpha() , 3)
ORANGE_BALL = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "ORANGE_BALL.png")).convert_alpha() , 3)
DARK_BLUE_BALL = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "DARK_BLUE_BALL.png")).convert_alpha() , 3)
GREEN_BALL = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "GREEN_BALL.png")).convert_alpha() , 3)

FIRE_PARTICLE = pygame.image.load(os.path.join("assets", "imgs", "FIRE_PARTICLE_1.png")).convert_alpha()
#EXPLOSION_TEMP = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "EXPLOSION_TEMP.png")).convert_alpha() , 2)

COOL_SLIME = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "COOL_SLIME.png")).convert_alpha() , 4)
EVIL_SLIME = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "EVIL_SLIME.png")).convert_alpha() , 4)
GREEN_SLIME = pygame.transform.scale_by( pygame.image.load(os.path.join("assets", "imgs", "GREEN_SLIME.png")).convert_alpha() , 4)
BLUE_SLIME = pygame.transform.scale_by(pygame.image.load(os.path.join("assets", "imgs", "enemy.png")).convert_alpha(), 4)




#
# Oh Dont Worry about Them .... They like it actually
#
#
#