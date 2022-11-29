from pico2d import *
# import maingame as screen
import game_framework
import game_world
import server

PIXEL_PER_METER = (10.0/0.3)
MOVE_SPEED_KMPH = 15.0
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Goomba:
    def __init__(self):
        self.image = load_image('C:/2DGP_Project/image/Monsters.png')
        self.dir_x = -1
        self.x, self.y = 1400 // 2 , 500  # 초기 위치 (화면 하단 중앙)
        self.frame = 0
        self.timer = 100
        self.state = None

    def draw(self): #그리기
        sx, sy = self.x - server.back.window_left, self.y
        if self.state == 'dead':
            self.image.clip_draw(2 * 64 + 67, 785, 64, 50, sx, sy)
        else:
            self.image.clip_draw(int(self.frame) * 64 + 67, 785, 64, 50, sx, sy)
        draw_rectangle(*self.get_bb())


    def update(self): # 이동 관련
        screen_check(self)
        if self.y-20 > 100:
            self.y -= 1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time
        if self.state == 'dead':
            self.timer -= 1
        if self.timer == 0:
            game_world.remove_object(self)


    def get_bb(self):
        return self.x - 20, self.y - 27, self.x + 20, self.y + 20

    def handle_collision(self, other, group):
        if group == 'mario:enemy':
            pass

    def handle_side_collision(self, other, group):
        if group == 'enemy:wall':
            self.dir_x = -self.dir_x
        if group == 'mario:enemy':
            if other.state == 'invincible':
                self.dir_x = 0
                self.state = 'dead'
            else:
                pass
            pass

    def handle_floor_collision(self, other, group):
        if group == 'enemy:floor':
            self.y = other.y + other.h/2 + 1 + 25
        if group == 'mario:enemy':
            self.dir_x = 0
            self.state = 'dead'
            pass

class KoopaTroopa:
    def __init__(self):
        self.image = load_image("C:/2DGP_Project/image/Monsters.png")
        self.dir_x = -1
        self.x, self.y = 1400 // 2 - 350,  500   # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0
        self.state = None

    def draw(self): #그리기
        sx, sy = self.x - server.back.window_left, self.y
        if self.state == None:
            if self.dir_x == 1: # 오른쪽을 향할 때
                self.image.clip_draw(int(self.frame) * 64 + 67, 525, 64, 75, sx, sy)
            elif self.dir_x == -1: # 왼쪽을 향할때
                self.image.clip_composite_draw(int(self.frame) * 64 + 67, 525, 64, 75, 0,'h',sx, sy, 64, 75)
        else:
            self.image.clip_draw(int(self.frame) * 64 + 67, 450, 64, 75, sx, sy)
        draw_rectangle(*self.get_bb())

    def update(self): # 이동 관련
        screen_check(self)
        if self.y-20 > 100:
            self.y -= 1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 20

    def handle_collision(self, other, group):
        if group == 'mario:enemy':
            pass

    def handle_side_collision(self, other, group):
        if group == 'enemy:wall':
            self.dir_x = -self.dir_x
            pass

    def handle_floor_collision(self, other, group):
        if group == 'enemy:floor':
            self.y = other.y + other.h/2 + 1 + 25
        if group == 'mario:enemy':
            if self.state == 'STAMPED':
                self.dir_x = 2
            else:
                self.state = 'STAMPED'
                self.dir_x = 0
            pass

class RedTroopa:
    def __init__(self):
        self.image = load_image("C:/2DGP_Project/image/Monsters.png")
        self.dir_x = -1
        self.x, self.y = 1400 // 2 + 350, 400   # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0
        self.state = None

    def draw(self): #그리기
        sx, sy = self.x - server.back.window_left, self.y
        if self.state == None:
            if self.dir_x == 1: # 오른쪽을 향할 때
                self.image.clip_draw(int(self.frame) * 64 + 67*6-10, 525, 64, 75, sx, sy)
            elif self.dir_x == -1: # 왼쪽을 향할때
                self.image.clip_composite_draw(int(self.frame) * 64 + 67*6, 525, 64, 75, 0,'h',sx, sy, 64, 75)
        else:
            self.image.clip_draw(int(self.frame) * 64 + 67 * 6 - 10, 450, 64, 75, sx, sy)
        draw_rectangle(*self.get_bb())

    def update(self): # 이동 관련
        screen_check(self)
        if self.y-20 > 100:
            self.y -= 1
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 20

    def handle_collision(self, other, group):
        if group == 'mario:enemy':
            pass

    def handle_side_collision(self, other, group):
        if group == 'enemy:wall':
            self.dir_x = -self.dir_x
            pass

    def handle_floor_collision(self, other, group):
        if group == 'enemy:floor':
            self.y = other.y + other.h/2 + 1 + 25
        if group == 'mario:enemy':
            if self.state == 'STAMPED':
                self.dir_x = 2
            else:
                self.state = 'STAMPED'
                self.dir_x = 0
            pass

class Stamped:
    def __init__(self):
        pass

def screen_check(obj):
    if obj.x > 1400:
        obj.x = 1400
        obj.dir_x = -obj.dir_x

    elif obj.x < 0:
        obj.x = 0
        obj.dir_x = -obj.dir_x

    elif obj.y < 35:
        obj.y = 35

    elif obj.y > 700:
        obj.y = 700 - 10