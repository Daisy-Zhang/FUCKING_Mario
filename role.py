import constant
import move

class role():            # basic class, funny just for test

    role_type = 0    #  role_type = 0 player,   role_type = 1 enemy
    role_x = 0    #  position of the role
    role_y = 0
    role_image_file = "null"    #   role image file name

    start_moving = 0   #   the position of player when the role start moving
    app = 0


    role_x_size = 0    #  role size
    role_y_size = 0

    top_health = 100
    health = top_health    #   health of the role
    

    total_jump_time = 200   # total time of a jump on a ground
    jump_height = 120    # height of a jump on a ground

    move_speed = 0.1      # horizental move speed
    top_move_speed = 0.6    # horizontal top move speed

    up_speed = 0    # the speed of up going
    jump_direction = 0  # 0 jump vertically    1 jump towards left    2 jump towards right
   
    or_acceleration = 0.0003    # original horizental move acceleration
    acceleration = or_acceleration    # horizental move acceleration

    face = 1   #   face = 1 towards right    face = -1 towards left

    def setApp(self, a):
        self.app = a

    def setStartMoving(self, s):
        self.start_moving = s

    def setRoleType(self, rt):
        self.role_type = rt

    def setImageFile(self, s):
        self.role_image_file = s

    def setRoleX(self, x):
        self.role_x = x
    
    def setRoleY(self, y):
        self.role_y = y

    def setRoleXSize(self, l):
        self.role_x_size = l

    def setRoleYSize(self, h):
        self.role_y_size = h

    def setHealth(self, heal):
        self.health = heal

    def setTotalJumpTime(self, totJT):
        self.total_jump_time = totJT

    def setJumpHeight(self, h):
        self.jump_height = h

    def setMoveSpeed(self, mv):
        self.move_speed = mv

    def setUpSpeed(self, us):
        self.up_speed = us

    def setJumpDirection(self, jumpDR):
        self.jump_direction = jumpDR

    def setTopMoveSpeed(self, topMS):
        self.top_move_speed = topMS

    def setOrAcceleration(self, orA):
        self.or_acceleration = orA

    def setAcceleration(self, acc):
        self.acceleration = acc

    def setFace(self, f):
        self.face = f

    
    def getApp(self):
        return self.app

    def getStartMoving(self):
        return self.start_moving

    def getRoleType(self):
        return self.role_type

    def getRoleImageFile(self):
        return self.role_image_file

    def getRoleX(self):
        return self.role_x
    
    def getRoleY(self):
        return self.role_y

    def getRoleXSize(self):
        return self.role_x_size

    def getRoleYSize(self):
        return self.role_y_size

    def getHealth(self):
        return self.health

    def getTotalJumpTime(self):
        return self.total_jump_time

    def getJumpHeight(self):
        return self.jump_height

    def getMoveSpeed(self):
        return self.move_speed

    def getUpSpeed(self):
        return self.up_speed

    def getJumpDirection(self):
        return self.jump_direction

    def getTopMoveSpeed(self):
        return self.top_move_speed

    def getOrAcceleration(self):
        return self.or_acceleration

    def getAcceleration(self):
        return self.acceleration

    def getA(self):
        return -8 * self.jump_height / (self.total_jump_time ** 2)   # coefficient of jump action

    def getJumpSpeed(self):
        return - self.getA() * self.total_jump_time / 2

    def getFace(self):
        return self.face

    def judgeDeath(self):
        if self.health <= 0:
            return constant.ROLE_DIED
        else:
            return constant.ROLE_ALIVE

    #maybe next time to finish them
    #def beAttacked(self):
    #def beTouched(self, player_x, player_y):
