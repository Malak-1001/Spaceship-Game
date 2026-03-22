import os
import pygame
import random
import math 
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "Assets")

from pygame import mixer
pygame.font.init()

#initialize the game
pygame.init()

# --------------------  ASSETS  --------------------

# Background
Background= pygame.image.load(os.path.join(ASSETS,"background.jpg"))

# Icon
icon=pygame.image.load(os.path.join(ASSETS,"vaisseau-spatial.png"))

# Player
PlayerImg = pygame.image.load(os.path.join(ASSETS,"Spaceship.png"))

# Enemy
# EnemyImg = pygame.image.load("D:/ideas-Project/Spaceship Game/Assets/png/ENEMY.png")

# Bullets
BulletImg = pygame.image.load(os.path.join(ASSETS,"balle.png"))

# Music Backg
mixer.music.load(os.path.join(ASSETS,"background.wav"))
mixer.music.play(-1)

#-----------------------------------------------------

# Create the game's screen 
width, height = 600 ,600
screen=pygame.display.set_mode((width,height))

# Caption of the window 
pygame.display.set_caption('Welcome to my Spaceship Game')

# Setting the icon 
pygame.display.set_icon(icon)


# PLAYER 
Player_X= width/2 - 64/2
Player_Y= height- 64*2
Mouvement_X=0



# ENEMY
EnemyImg= []
Enemy_X= []
Enemy_Y= []
Mouv_X= []
Mouv_Y=[]
num_of_enemies = 6
Speed = 0.6  

for i in range (num_of_enemies):
    EnemyImg.append(pygame.image.load(os.path.join(ASSETS,"png","ENEMY.png")))
    Enemy_X.append(random.randint(0,536))
    Enemy_Y.append(random.randint(50,150))
    Mouv_X.append(Speed)
    Mouv_Y.append(25)


# BULLET 
Bullet_X =0
Bullet_Y = 480
M_X = 0
M_Y = -8
Bullet_state= "ready"



def Player(x,y):
    screen.blit(PlayerImg,(x,y))  # Draws the image on the screen


def ENEMY(x,y,i):
    screen.blit(EnemyImg[i],(x,y))  # Draws the image on the screen


def fire_bullet(x,y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg,(x +16,y+10))


def isCollision (Enemy_X, Enemy_Y, Bullet_X, Bullet_Y):
    distance = math.sqrt((math.pow((Enemy_X - Bullet_X),2))+(math.pow((Enemy_Y - Bullet_Y),2)))
    if distance < 25 :
        return True
    else :
        return False
    
def Game_over_text():
     over_font = pygame.font.SysFont("ArcadeClassic", 68)
     Game_over_label = over_font.render(f"GAME OVER", 1, (255,255,255))
     screen.blit(Game_over_label,(150,250))


    
def main():
    # Global Variables
    global Player_X ,Player_Y,Mouvement_X
    global Enemy_X, Enemy_Y, Mouv_X,Mouv_Y, Speed
    global Bullet_X,Bullet_Y,M_Y,Bullet_state
    
    FPS = 120
    Level = 1
    Score = 0
    previous_score = -1
    running = True
    Clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("ArcadeClassic", 40)

    
    while running :

        Clock.tick(FPS)

        # Change the screen
        screen.fill((0,0,0))  #  RGB - Red , Green, Blue MAX 255
        screen.blit(Background,(0,0))

        # Write text
        Levels_label = FONT.render(f"Level: {Level}", 1, (255,255,255))
        screen.blit(Levels_label,(15,15))

        Score_label = FONT.render(f"Score: {Score}", 1, (255,255,255))
        screen.blit(Score_label,((width - Score_label.get_width()-10),15))
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
                
                
            # If Keystroke is pressed check if it's right or down
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT:
                    Mouvement_X = -3
                if event.key == pygame.K_RIGHT:
                    Mouvement_X = 3
                if event.key == pygame.K_SPACE:
                    if Bullet_state == "ready":
                        bullet_Sound= mixer.Sound(os.path.join(ASSETS,"laser.wav"))
                        bullet_Sound.play()
                        Bullet_X = Player_X
                        fire_bullet(Bullet_X,Bullet_Y) 
            
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    Mouvement_X= 0


       # Player  
        Player_X += Mouvement_X
        
        if Player_X <= 0 :
            Player_X = 0
        elif Player_X >= width - 64 :
            Player_X=width - 64
        
        Player(Player_X,Player_Y)

        
        # Enemy

        for i in range ( num_of_enemies):
            if Enemy_Y[i] > ( height- 64*2.5-5):
                for j in range ( num_of_enemies):
                  Enemy_Y[j] = 950
                Game_over_text()
                break
            
            
            Enemy_X[i] += Mouv_X[i]
            
            if Enemy_X[i] <= 0 :
                Mouv_X[i] = Speed
                Enemy_Y[i] += Mouv_Y[i]
            elif Enemy_X[i] >= width - 64 :
                Mouv_X[i]= -Speed
                Enemy_Y[i] += Mouv_Y[i]
            if Enemy_Y[i] >= height- 64*2.5 :
                Enemy_Y[i] = height- 64*2.5
                
                # Collisions
            Collision = isCollision ( Enemy_X[i], Enemy_Y[i], Bullet_X, Bullet_Y)
            if Collision :
               boom_Sound= mixer.Sound(os.path.join(ASSETS,"explosion.wav"))
               boom_Sound.play() 
               Bullet_Y = Player_Y
               Bullet_state = "ready"
               Score += 1
               Enemy_X[i]= random.randint(0,536)
               Enemy_Y[i]= random.randint(50,150)
            ENEMY(Enemy_X[i],Enemy_Y[i],i)
            

        # Bullet
        if Bullet_Y <= 0 :
            Bullet_Y = 480
            Bullet_state = "ready"
            
        if Bullet_state == "fire":
            fire_bullet(Bullet_X, Bullet_Y)
            Bullet_Y += M_Y

        if Score != 0 and Score % 10 == 0 and previous_score != Score :
           Speed += 0.1
           Level += 1
           previous_score = Score

            
        # Surface update
        pygame.display.update()   # To update just like C
        

main()    
pygame.quit()
