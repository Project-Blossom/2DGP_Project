from pico2d import *
import game_framework
import maingame as screen
import item_state
from Items import *
from Enemy import *

VELOCITY = 1 # 속도
MASS = 1000 # 질량

PIXEL_PER_METER = (10.0/0.3)
MOVE_SPEED_KMPH = 30.0
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

RD, LD, RU, LU, TIMER, SPACE = range(6)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU
}
PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Mario:
    def __init__(self): # 초기화
        self.smallform = load_image('SmallMario.png')
        self.bigform = load_image('BigMario.png')
        self.dir_x = 0
        self.x, self.y = screen.WIDTH // 2, 35 # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0
        self.isJump = 0 # 점프 확인
        self.v = VELOCITY # 속도
        self.m = MASS # 질량
        self.life = 1
        self.state = None
        self.rect = [(self.x - 20, self.y + 25), (self.x + 20, self.y + 25), (self.x - 20, self.y - 25) ,(self.x + 20, self.y - 25)]

    def draw(self): #그리기
        if self.dir_x == 1: # 오른쪽을 향할 때
            if self.isJump > 0: # 점프할 때
                if self.state == 'mushroom':
                    self.bigform.clip_draw(600, 91 + 50, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(600, 91, 100, 75, self.x, self.y)
            else:
                if self.state == 'mushroom':
                    self.bigform.clip_draw(int(self.frame) * 100 + 100, self.pose + 91 + 192, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(int(self.frame) * 100 + 100, self.pose + 91, 100, 75, self.x, self.y)
            if self.state == 'mushroom':
                self.pose = 0
            else:
                self.pose = -1
        elif self.dir_x == -1: # 왼쪽을 향할때
            if self.isJump > 0:
                if self.state == 'mushroom':
                    self.bigform.clip_draw(700, 335 + 222, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(700, 335, 100, 75, self.x, self.y)
            else:
                if self.state == 'mushroom':
                    self.bigform.clip_draw(int(self.frame) * 100 + 1000, self.pose + 12 + 272, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(int(self.frame) * 100 + 1000, self.pose + 12, 100, 75, self.x, self.y)
            if self.state == 'mushroom':
                self.pose = 410
            else:
                self.pose = 320
        elif self.dir_x == 0: # 스탠딩
            if self.state == 'mushroom':
                self.pose += 92
            else:
                self.pose += 92
            if self.isJump > 0:
                if self.state == 'mushroom':
                    self.bigform.clip_draw(600, 91 + 50, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(600, 91, 100, 75, self.x, self.y)
            else:
                if self.state == 'mushroom':
                    self.bigform.clip_draw(0, self.pose + 192, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(0, self.pose, 100, 75, self.x, self.y)
            if self.state == 'mushroom':
                self.pose -= 92
            else:
                self.pose -= 92

    def screen_check(self): # 화면 밖으로 못나가게 하기
        if self.x > screen.WIDTH:
            self.x = screen.WIDTH

        elif self.x < 0:
            self.x = 0

        elif self.y < 35:
            self.y = 35

        elif self.y > screen.HEIGHT:
            self.y = screen.HEIGHT -10

    def jump(self, j): # 점프 상태 체크
        self.isJump = j

    def update(self): # 이동 관련
        get_item()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time
        if self.isJump > 0:

            # if self.isJump == 2: # 이단 점프
            #     self.v = VELOCITY

            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0: # 속도가 0보다 클때는 위로 올라감
                F = -(0.005 * self.m * (self.v **2))
            else: # 속도가 0보다 작을때는 아래로 내려감
                F = (0.005 * self.m * (self.v **2))

            self.y -= round(F) # 좌표 반영하기

            self.v -= 0.009 # 속도 줄이기

            if self.y < 35: # 바닥에 닿았을때 변수 리셋
                self.y = 35
                self.isJump = 0
                self.v = VELOCITY

def handle_events():
    global playing, mario
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_i:
                game_framework.push_state(item_state)
            elif event.key == SDLK_RIGHT:
                mario.dir_x += 1
            elif event.key == SDLK_LEFT:
                mario.dir_x -= 1
            elif event.key == SDLK_SPACE:
                if mario.isJump == 0:
                    mario.jump(1)
                elif mario.isJump == 1:
                    mario.jump(2)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir_x -= 1
            elif event.key == SDLK_LEFT:
                mario.dir_x += 1
            # elif event.key == SDLK_SPACE:
            #     if mario.isJump == 1:
            #         mario.jump(0)

playing = True
mario = None
spawnmush = 0
mushroom = None
spawnflower = 0
flower = None
spawnstar = 0
star = None


def collider(mario, item):
    if mario.x + 20 > item.x - 20 > mario.x - 20 and mario.y + 50 > item.y - 20 > mario.x - 50:
        return 1
    pass

def get_item():
    if (collider(mario, mushroom) == 1) and (mario.state != 'flower'):
        mario.state = 'mushroom'
        game_framework.quit()
        mario.life = 2
    if (collider(mario, flower) == 1):
        mario.state = 'flower'
        mario.life = 3
    if (collider(mario, star) == 1):
        mario.state = 'star'

def enter():
    global mario, playing, mushroom, flower, star, tile
    mario = Mario()
    mushroom = Goomba()
    flower = Fire_Flower()
    star = Star()
    playing = True

def update():
    global mario
    mario.update()
    mario.screen_check()
    mushroom.update()
    mushroom.screen_check()
    flower.update()
    flower.screen_check()
    star.update()
    star.screen_check()
    get_item()

def draw():
    clear_canvas()
    mario.draw()
    mushroom.draw()
    flower.draw()
    star.draw()
    update_canvas()

def exit():
    quit()

def pause():
    pass

def resume():
    pass
