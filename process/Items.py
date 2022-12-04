import sys
import os
sys.path.append('C:/2DGP_Project/processor/')
from pico2d import *
import game_world

import game_framework
import server

Floor = 100

VELOCITY = 1  # 속도
MASS = 20  # 질량

PIXEL_PER_METER = (50.0/1.0) # 50 pixel 1m
MOVE_SPEED_KMPH = 8.0
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

class Mushroom:
    image = None
    def __init__(self, x=0, y=0, dir=-1):
        if Mushroom.image == None:
            Mushroom.image = load_image('C:/2DGP_Project/image/Items.png')
        self.x = x
        self.y = y
        self.w, self.h = 50, 50
        self.dir = dir
        self.dir_x = dir * 1
        self.on_floor = False

    def draw(self):
        sx, sy = self.x - server.back.window_left, self.y
        self.image.clip_draw(0, 0, 75, 60, sx, sy)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor):
            self.y -= 1.5 * MOVE_SPEED_PPS * game_framework.frame_time
        wl, wr = server.back.window_left, server.back.window_left + server.back.canvas_width
        if wl + 5 < self.x < wr - 5:
            if self.y-20 <= 100 or self.on_floor:
                self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, other, group):
        if group == 'mario:mushroom':
            game_world.remove_object(self)

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            self.dir_x = -self.dir_x
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            self.y = other.y + other.h/2 + 30
            self.on_floor = True



class Fire_Flower:
    image = None
    def __init__(self, x=0, y=0):
        if Fire_Flower.image == None:
            Fire_Flower.image = load_image('C:/2DGP_Project/image/Items.png')
        self.x = x
        self.y = y
        self.on_floor = False

    def draw(self):
        sx, sy = self.x - server.back.window_left, self.y
        self.image.clip_draw(190, 0, 100, 60, sx, sy)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor):
            self.y -= 1.5 * MOVE_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 20

    def handle_collision(self, other, group):
        if group == 'mario:fire_flower':
            game_world.remove_object(self)
            pass

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            self.y = other.y + other.h / 2 + 30
            self.on_floor = True




class Star:
    def __init__(self, x=0, y=0):
        self.image = load_image('C:/2DGP_Project/image/Items.png')
        self.dir_x = 1
        self.x, self.y = x, y
        self.isJump = 0  # 점프 확인
        self.v = VELOCITY  # 속도
        self.m = MASS  # 질량

    def draw(self):
        sx, sy = self.x - server.back.window_left, self.y
        self.image.clip_draw(395, 0, 110, 60, sx, sy)
        # draw_rectangle(*self.get_bb())

    def update(self):
        wl, wr = server.back.window_left, server.back.window_left + server.back.canvas_width
        if wl + 5 < self.x < wr - 5:
            self.x += self.dir_x * 1 * MOVE_SPEED_PPS * game_framework.frame_time
        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor):
            if self.isJump == 0:
                self.y -= 1.5 * MOVE_SPEED_PPS * game_framework.frame_time
        if self.isJump > 0:

            # if self.isJump == 2: # 이단 점프 비 활성화
            #     self.v = VELOCITY

            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:  # 속도가 0보다 클때는 위로 올라감
                F = -(0.5 * self.m * (self.v ** 2))
            else:  # 속도가 0보다 작을때는 아래로 내려감
                F = (0.5 * self.m * (self.v ** 2))

            self.y -= round(F) * MOVE_SPEED_PPS * game_framework.frame_time # 좌표 반영하기

            self.v -= 0.05  # 속도 줄이기

        if self.y-20 <= 100:  # 바닥에 닿았을때 변수 리셋
            self.y = 120
            self.isJump = 1
            self.v = VELOCITY

    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 20

    def handle_collision(self, other, group):
        if group == 'mario:star':
            game_world.remove_object(self)
            pass

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            self.dir_x = -self.dir_x
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            if self.y < other.y:
                self.y = other.get_bb()[1] - 11
                self.v = -self.v
            if self.y > other.y:
                self.y = other.get_bb()[3] + 31
                self.isJump = 1
                self.v = VELOCITY
            pass

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



