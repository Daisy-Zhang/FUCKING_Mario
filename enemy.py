import constant

class enemy:            # basic class, funny just for test
    enemy_x = 0
    enemy_y = 0
    enemy_image_file = "null"
    enemy_track = [[0, 0], [0, 0]]

    health = 0
    speed = 0
    direction = 'n'     # h for Horizontal, v for Vertical, n for nothing
    face_to = 'n'       # l for Left, r for Right, u for Up, d for down

    def setImageFile(self, s):
        self.enemy_image_file = s

    def setEnemyTrack(self, sx, sy, ex, ey):
        self.enemy_track[0][0] = sx
        self.enemy_track[0][1] = sy
        self.enemy_track[1][0] = ex
        self.enemy_track[1][1] = ey

    def setEnemyInitialPos(self, x, y):
        self.enemy_x = x
        self.enemy_y = y

    def getEnemyImageFile(self):
        return self.enemy_image_file

    def getEnemyX(self):
        return self.enemy_x
    
    def getEnemyY(self):
        return self.enemy_y

    def setDirection(self, d):
        self.direction = d
    
    def setInitialFaceto(self, f):
        self.face_to = f

    def setSpeed(self, sp):
        self.speed = sp

    def setHealth(self, h):
        self.health = h
    
    def judgeDeath(self):
        if self.health == 0:
            return constant.ENEMY_DIED
        else:
            return constant.ENEMY_ALIVE

    def enemyMove(self):
        if self.direction == 'h' :
            if self.face_to == 'r' :
                self.enemy_x += self.speed
                if self.enemy_x >= max(self.enemy_track[1][0], self.enemy_track[0][0]):
                    self.enemy_x = max(self.enemy_track[1][0], self.enemy_track[0][0])
                    self.face_to = 'l'
            else:
                self.enemy_x -= self.speed
                if self.enemy_x <= min(self.enemy_track[1][0], self.enemy_track[0][0]):
                    self.enemy_x = min(self.enemy_track[1][0], self.enemy_track[0][0])
                    self.face_to = 'r'
        #else:   # for vertical movement, too lazy to finish it

    #maybe next time to finish them
    #def beAttacked(self):
    #def beTouched(self, player_x, player_y):

# just for quick test
level1_enemy1 = enemy()
level1_enemy1.setImageFile("image/enemy1.png")
level1_enemy1.setEnemyInitialPos(100, 290)
level1_enemy1.setEnemyTrack(100, 300, 200, 300)
level1_enemy1.setDirection('h')
level1_enemy1.setInitialFaceto('r')
level1_enemy1.setSpeed(2)
level1_enemy1.setHealth(1)