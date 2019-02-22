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
pygame.display.set_caption('Fucking Mario')

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

enemies = [[],[],[]]    #   collection of enemies of different level

destination = 4     #  destination level


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

def touch(player, enemy):
    touched = True
    if player.getRoleX() > enemy.getRoleX() + enemy.getRoleXSize() or player.getRoleX() + player.getRoleXSize() < enemy.getRoleX():
        touched = False
    if player.getRoleY() > enemy.getRoleY() + enemy.getRoleYSize() or player.getRoleY() + player.getRoleYSize() < enemy.getRoleY():
        touched = False
    return touched

#  add player1 in this game
player1 = role.role()
player1.setRoleX(player_x)
player1.setRoleY(player_y)
player1.setRoleXSize(player_x_size)
player1.setRoleYSize(player_y_size)
player1.setImageFile('image/player.png')

#  level 1 no enemy

#  add enemy1 in level 2
enemy2 = role.role()
enemy2.setHealth(100)
enemy2.setRoleType(1)
enemy2.setRoleXSize(56)
enemy2.setRoleYSize(56)
enemy2.setRoleX(540)
enemy2.setRoleY(350 - 56)
enemy2.setImageFile('image/enemy1.png')
enemies[1].append(enemy2)


#   add enemy3 in level 3
enemy3 = role.role()
enemy3.setHealth(100)
enemy3.setRoleType(1)
enemy3.setRoleXSize(56)
enemy3.setRoleYSize(56)
enemy3.setRoleX(400)
enemy3.setRoleY(100)
enemy3.setStartMoving(250)
enemy3.setImageFile('image/enemy1.png')
enemies[2].append(enemy3)

#    add enemy4 in level3
enemy4 = role.role()
enemy4.setHealth(100)
enemy4.setRoleType(1)
enemy4.setRoleXSize(54)
enemy4.setRoleYSize(54)
enemy4.setRoleX(620)
enemy4.setRoleY(200)
enemy4.setStartMoving(400)
enemy4.setImageFile('image/enemy2.png')
enemies[2].append(enemy4)

while True:

    if toNextLevel(player1.getRoleX(), player1.getRoleY()):
        player1.setRoleX(0)
        level += 1
        if level == destination:
            print('Your Win!')
            exit()

    ground, left, right = move.getGround(player_x, player_y, player_x_size, player_y_size, level)    # the ground position y coordinate

    move.move(player1, level)  

  
    if player1.getRoleY() > move.deadline:   # determine whether player is falling to death
    	print('Game Over')
    	exit()
    

    showMap(level)

    for enemy in enemies[level - 1]:
        if player1.getRoleX() > enemy.getStartMoving():
            enemy.setApp(1)
        if not enemy.getHealth() == 0 and enemy.getApp() == 1:
            move.move(enemy, level)
            enemyImage = pygame.image.load(enemy.getRoleImageFile()).convert()
            screen.blit(enemyImage, (enemy.getRoleX(), enemy.getRoleY()))
        if touch(player1, enemy):
            print('Game Over')
            exit()

    player = pygame.image.load(player1.getRoleImageFile()).convert()
    screen.blit(player,(player1.getRoleX(), player1.getRoleY()))
    pygame.display.update()
