import pygame
import random
import math
pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("space invaders.UPDATE: TOO TIRED TO ADD, MIGHT FINISH AS IS. ADD TITLE GAMEOVER MUSIC MORE ENEMIES&BULLET BOSS??? ")
icon = pygame.image.load("ship.png")
pygame.display.set_icon(icon)
playerimg = pygame.image.load("ship.png")
enemyimg = pygame.image.load("ghost.png")
bg= pygame.image.load("background.png")
bulletimg = pygame.image.load("bullet.png")

playerx=370
playery=480
xchange=0
ychange=0

enemyx=random.randint(0,730)
enemyy=random.randint(50,150)
enemyxchange=2
enemyychange=40

bullx=0
bully=480
bullxchange=0
bullychange=4
bullstate = "ready"

def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y):
    screen.blit(enemyimg,(x,y))
def bullet(x,y):
    global bullstate
    bullstate = "fire"
    screen.blit(bulletimg,(x+16,y+10))
def collision(enemyx,enemyy,bulletx,bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
    if distance <27:
        return True
    else:
        return False
        
run = True

while run:
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xchange =-2
            if event.key == pygame.K_RIGHT:
                xchange = 2
            if event.key == pygame.K_UP:
                ychange =-2
            if event.key == pygame.K_DOWN:
                ychange = 2
            if event.key == pygame.K_SPACE:
                if bullstate is "ready":
                    bullx = playerx
                bullet(bullx,bully)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                xchange = 0
                ychange = 0
    
    playerx +=  xchange
    playery+= ychange
    enemyx +=enemyxchange
    
    if playerx <=0:
        playerx = 0
    elif playerx >=736:
        playerx = 736
        
    if enemyx <=0:
        enemyxchange = 2
        enemyy += enemyychange
    elif enemyx >=736:
        enemyxchange = -2
        enemyy += enemyychange
        
    if bullstate is "fire":
        bullet(bullx,bully)
        bully -= bullychange
    if bully<=0:
        bully = 480
        bullstate = "ready"
        
    collisionn = collision(enemyx,enemyy,bullx,bully)
    if collisionn:
        bully = 480
        bullstate = "ready"
        enemyx=random.randint(0,730)
        enemyy=random.randint(50,150)
    player(playerx,playery)
    enemy(enemyx,enemyy)
    
    pygame.display.update()
    
# IMAGES USED FROM FLAT ICONS
# BULLET:https://www.flaticon.com/free-icon/bullet_224681?term=bullet&page=1&position=3&page=1&position=3&related_id=224681&origin=search
# SHIP:https://www.flaticon.com/premium-icon/spaceship_1985789?term=spaceship&page=1&position=2&page=1&position=2&related_id=1985789&origin=search
# ENEMY:https://www.flaticon.com/free-icon/enemy_1477179?term=enemy&page=1&position=1&page=1&position=1&related_id=1477179&origin=search
# ALL ABOVE IN 64B
# BACKGROUND:WHATEVER U LIKE, CANT FIND MY BG ANYMORE
