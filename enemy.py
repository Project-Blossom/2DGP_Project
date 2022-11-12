from pico2d import *
# import maingame as screen
import game_framework

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
        self.image = load_image("Monsters.png")
        self.dir_x = 1
        self.x, self.y = 1400 // 2 + 350, 35 + 200  # 초기 위치 (화면 하단 중앙)
        self.frame = 0


    def draw(self): #그리기
        self.image.clip_draw(int(self.frame) * 64 + 67, 785, 64, 50, self.x, self.y)
        draw_rectangle(*self.bb)

    def update(self): # 이동 관련
        screen_check(self)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time
        self.bb = [self.x - 23, self.y - 30, self.x + 23, self.y + 20]

class KoopaTroopa:
    def __init__(self):
        self.image = load_image("Monsters.png")
        self.dir_x = -1
        self.x, self.y = 1400 // 2 - 350, 35 + 200  # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0


    def draw(self): #그리기
        if self.dir_x == 1: # 오른쪽을 향할 때
            self.image.clip_draw(int(self.frame) * 64 + 67, 525, 64, 75, self.x, self.y)
        elif self.dir_x == -1: # 왼쪽을 향할때
            self.image.clip_composite_draw(int(self.frame) * 64 + 67, 525, 64, 75, 0,'h',self.x, self.y, 64, 75)
        draw_rectangle(*self.bb)

    def update(self): # 이동 관련
        screen_check(self)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time
        self.bb = [self.x - 25, self.y - 30, self.x + 25, self.y + 20]

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