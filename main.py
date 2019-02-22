import pygame
import box
import role
import constant
import move
from pygame.locals import *
from sys import exit

 
pygame.init()
level = 1
screen = pygame.display.set_mode((640, 480), 0, 32)

player_x_size = 46
player_y_size = 50

pygame.mixer.init()                     # BGM player
pygame.mixer.music.load('BG.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

player_x = 0
player_y = 300

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
light_blue = (128, 128, 255)

deadline = 700		# the falling deadline


def toNextLevel(player_x, player_y):
    if player_x + player_x_size >= 670 :
        return True
    else:
        return False


def showMap(level):
    screen.fill(light_blue)
    box_col = white
    for box_ in box.boxes[level - 1]:
        x = box_[0][0][0]
        y = box_[1][0][0]
        length = box_[0][0][1] - box_[0][0][0]
        height = box_[1][0][1] - box_[1][0][0]
        box_col = box_[2]
        pygame.draw.rect(screen, box_col, (x, y, length, height))

    # load enemy test
    
    # enemy1 = pygame.image.load(role.level1_enemy1.getEnemyImageFile()).convert()
    # if role.level1_enemy1.judgeDeath() == constant.ROLE_ALIVE :
    #     role.level1_enemy1.enemyMove()
    #     screen.blit(enemy1, (role.level1_enemy1.getEnemyX(), role.level1_enemy1.getEnemyY()))
    # screen.blit(player, (player_x, player_y))


player1 = role.role()
player1.setRoleX(player_x)
player1.setRoleY(player_y)
player1.setRoleXSize(player_x_size)
player1.setRoleYSize(player_y_size)
player1.setImageFile('image/player.png')

while True:

    if toNextLevel(player1.getRoleX(), player1.getRoleY()):
        player1.setRoleX(0)
        level += 1

    ground, left, right = move.getGround(player_x, player_y, player_x_size, player_y_size, level)    # the ground position y coordinate

    move.move(player1, level)
  
    if player1.getRoleY() > deadline:   # determine whether player is falling to death
    	print('Game Over')
    	exit()
    
    

    player = pygame.image.load(player1.getRoleImageFile()).convert()
    showMap(level)
    screen.blit(player,(player1.getRoleX(), player1.getRoleY()))

    pygame.display.update()
