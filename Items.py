from pico2d import *
# import maingame as screen

VELOCITY = 1  # 속도
MASS = 1000  # 질량

class Mushroom:
    def __init__(self):
        self.x = 1400 // 2 - 300
        self.y = 700 - 20
        self.image = load_image('Items.png')
        self.dir_x = -0.6

    def draw(self):
        self.image.clip_draw(0, 0, 80, 60, self.x, self.y)
        draw_rectangle(*get_bb(self))

    def update(self):
        screen_check(self)
        if self.y-20 > 100:
            self.y -= 1
        if self.y-20 <= 100:
            self.x += self.dir_x

class Fire_Flower:
    def __init__(self):
        self.x = 1400 // 2
        self.y = 700 - 20
        self.image = load_image('Items.png')
        self.dir_x = -0.6

    def draw(self):
        self.image.clip_draw(190, 0, 100, 60, self.x, self.y)
        draw_rectangle(*get_bb(self))

    def update(self):
        screen_check(self)
        if self.y-20 > 100:
            self.y -= 1


class Star:
    def __init__(self):
        self.image = load_image('Items.png')
        self.dir_x = 0.7
        self.x, self.y = 1400 // 2 + 300, 700  # 초기 위치 (화면 하단 중앙)
        self.isJump = 0  # 점프 확인
        self.v = VELOCITY  # 속도
        self.m = MASS  # 질량

    def draw(self):
        self.image.clip_draw(395, 0, 110, 60, self.x, self.y)
        draw_rectangle(*get_bb(self))

    def update(self):
        screen_check(self)
        if self.y-20 > 100:
            self.x += self.dir_x * 1
            if self.isJump == 0:
                self.y -= 1
        if self.isJump > 0:

            # if self.isJump == 2: # 이단 점프
            #     self.v = VELOCITY

            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:  # 속도가 0보다 클때는 위로 올라감
                F = -(0.005 * self.m * (self.v ** 2))
            else:  # 속도가 0보다 작을때는 아래로 내려감
                F = (0.005 * self.m * (self.v ** 2))

            self.y -= round(F)  # 좌표 반영하기

            self.v -= 0.01  # 속도 줄이기

        if self.y-20 <= 100:  # 바닥에 닿았을때 변수 리셋
            self.y = 120
            self.isJump = 1
            self.v = VELOCITY


def screen_check(obj):
    if obj.x > 1400:
        obj.x = 1400
        obj.dir_x = -obj.dir_x

    elif obj.x < 0:
        obj.x = 0
        obj.dir_x = -obj.dir_x

    elif obj.y < 0:
        obj.y = 0

    elif obj.y > 700:
        obj.y = 700 - 10

def get_bb(obj):
    return obj.x-25, obj.y-30, obj.x+25, obj.y+20

