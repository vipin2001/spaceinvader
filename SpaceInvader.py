import pygame
import random
import math
from pygame import mixer

#intialize the pygame
pygame.init()

#creating screen(width,height)
screen = pygame.display.set_mode((800,600))

#score font
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

#game over font
gm_font = pygame.font.Font("freesansbold.ttf",64)


#Title and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#bg
bgImg = pygame.image.load('bg.jpg')
bgImg = pygame.transform.scale(bgImg, (800, 600))

#bg sound 
mixer.music.load('bg_music.mp3')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('spaceship.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 524
playerX_change = 0

#Enemy
num_enemy = 6
enemyImg = pygame.image.load('monster.png')
enemyImg = pygame.transform.scale(enemyImg, (48, 48))
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = 24
for i in range(num_enemy):
	enemyX.append(random.randint(0,750))
	enemyY.append(random.randint(50,400))
	enemyX_change.append(0.3)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (24, 24))
bulletX = 0
bulletY = playerY
bulletY_change = 1
bullet_state = "notfired"

#score
score = 0

#functions
def player(x,y):
	# Drawing on screen
	screen.blit(playerImg,(x,y))

def enemy(x,y):
	# Drawing on screen
	screen.blit(enemyImg,(x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg,(x+20,y-10))

def isCOllision(xb,xe,yb,ye):
	distance = math.sqrt((math.pow(xb-xe,2)+(math.pow(ye-yb,2))))
	if distance < 30:
		return True
	else:
	 return False

def show_score(x,y):
	score_value = font.render("Score : " + str(score), True, (255,255,255)) 
	screen.blit(score_value,(x,y))

def game_over():
	gm_text = gm_font.render("GAME OVER", True, (255,255,255)) 
	screen.blit(gm_text,(200,250))

#Game Loop
running = True
while running:
	#screen color
	screen.fill((0,20,0))
	screen.blit(bgImg,(0,0))
	#exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		#if keystroke is pressed checck wether it is right or left
		#first check any key pressed, keydown = pressing the key keyup = leaving the key
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -0.3

			if event.key == pygame.K_RIGHT:
				playerX_change = 0.3
			if event.key == pygame.K_SPACE:
				if bullet_state == "notfired":
					bullet_sound = mixer.Sound("bullet_sound.mp3")
					bullet_sound.play()
					bulletX=playerX
					fire_bullet(bulletX,bulletY)


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
	playerX+=playerX_change
	
	#Bullet mvt
	if bullet_state == "fire":
		fire_bullet(bulletX,bulletY)
		bulletY-=bulletY_change
	if bulletY<0:
		bulletY=playerY
		bullet_state = "notfired"

	if playerX<0:
		playerX=0
	if playerX>736:
		playerX=736
	
	for i in range(num_enemy):
		if enemyY[i]>476:
			for j in range(num_enemy):
				enemyY[j]=2000
				game_over()	
		enemyX[i]+=enemyX_change[i]	
		if enemyX[i]<0:
			enemyX[i]=0
			enemyX_change[i]=0.3
			enemyY[i]+=enemyY_change
		if enemyX[i]>736:
			enemyX[i]=736
			enemyX_change[i]=-0.3
			enemyY[i]+=enemyY_change
		
	#after coloring screen we draw the image
		if isCOllision(bulletX,enemyX[i],bulletY,enemyY[i]):
			if bullet_state == "fire":
				score += 1
				bulletY=playerY
				crash_sound = mixer.Sound("crash.mp3")
				crash_sound.play()
				bullet_state = "notfired"
			enemyX[i] = random.randint(0,750)
			enemyY[i] = random.randint(50,400)
					
		enemy(enemyX[i],enemyY[i])	
	player(playerX,playerY)
	show_score(10,10)
	#Updating the game window
	pygame.display.update()