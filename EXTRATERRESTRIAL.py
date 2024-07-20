import pygame
import random
import math
from pygame import mixer
 

#initialize the pygame
pygame.init()


#make the screen
screen=pygame.display.set_mode(size=(900,600))


#background
background = pygame.image.load('EXT_Background.jpg')
background = pygame.transform.scale(background,(900,650))
mixer.music.load("EXT_Bgsound.wav")
mixer.music.play(-1)


#make the title and icon
pygame.display.set_caption("EXTRATERRESTRIAL")
icon = pygame.image.load('EXT_Icon.png')
pygame.display.set_icon(icon) 


#insert player image
playerImg=pygame.image.load("EXT_Player.png")
playerX=420
playerY=450
playerX_change=0

def player1(x,y):
    screen.blit(playerImg,(x,y))


#insert enemy image
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_enemy=16
for i in range (no_enemy):
    enemyImg.append(pygame.image.load("EXT_Enemy.png"))
    enemyX.append(random.randint(0,834))
    enemyY.append(random.randint(0,100))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

    def enemy1(x,y,i):
        screen.blit(enemyImg[i],(x,y))


#insert bullet image
 #"stop" --> can not see the bullet
 #"fire" --> bullet will be seen
bulletImg=pygame.image.load("EXT_Bullet.png")
bulletX = 0
bulletY = 460
bulletX_change = 0
bulletY_change = 2
bullet_state = "stop"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+36, y))
    

#collision detect
def ifcollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 30:
        return True


#score board text
score_value= 0
score_font = pygame.font.Font("EXT_Font.otf", 35)

textX = 10
textY = 10

def show_score(x,y):
    score= score_font.render("SCORE : " + str(score_value), True, (255,255,255), (0,0,100))
    screen.blit(score, (x,y))


#game over text
over_font = pygame.font.Font("EXT_Font.otf", 80)

def game_over():
    over = over_font.render(" GAME OVER " , True, (255,0,0))
    screen.blit(over, (280,250))


#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Keystroke
        if event.type == pygame.KEYDOWN: #keystroke pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "stop":
                    bullet_sound = mixer.Sound("EXT_Shoot.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP: #keystroke released
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0


    #rgb --> red, green, blue
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    

    #player movement
    playerX += playerX_change
    
    #player boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 834:
        playerX = 834

    #player recall
    player1(playerX,playerY)


    #enemies
    for i in range (no_enemy):
        #enemy boundaries
        if enemyX[i] <= 0:
            enemyX_change[i]  = 0.5
            enemyY[i]  += enemyY_change[i] 
        elif enemyX[i] >= 834:
            enemyX_change[i]  = -0.5
            enemyY[i] += enemyY_change[i]
        
        #enemy movement
        enemyX[i] += enemyX_change[i]

        #enemy recall
        enemy1(enemyX[i],enemyY[i],i)

        #collision
        collision = ifcollision(enemyX[i] ,enemyY[i] ,bulletX ,bulletY )
        if collision:
            col_sound = mixer.Sound("EXT_Explosion.wav")
            col_sound.play()
            bulletY = 460
            bullet_state = "stop"
            score_value += 1
            enemyX[i]=random.randint(0,834)
            enemyY[i]=random.randint(0,100)
        
        #game over
        if enemyY[i] > 420:
            for j in range (no_enemy):
                enemyY[j]=1000
            death_sound = mixer.Sound("EXT_Invaderkilled.wav")
            death_sound.play()
            game_over()
            break
    

    #bullet
    #bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    #bullet boundaries
    if bulletY <= 0:
        bulletY = 460
        bullet_state = "stop"

    
    #score board recall
    show_score(textX,textY) 

    pygame.display.update()