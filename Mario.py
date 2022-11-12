from pico2d import *
import game_framework
import time

VELOCITY = 1 # 속도
MASS = 1000 # 질량

PIXEL_PER_METER = (10.0/0.3)
MOVE_SPEED_KMPH = 40.0
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

RD, LD, RU, LU, SPACE = range(5)
event_name = ['RD', 'LD', 'RU', 'LU', 'SPACE']

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

class IDLE:
    @staticmethod
    def enter(self,event):
        # print('ENTER IDLE')
        self.dir = 0

    @staticmethod
    def exit(self, event):
        pass
        # print('EXIT IDLE')

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        if self.dir == 0:
            self.pose += 92
            self.image.clip_draw(0, self.pose, 100, 75, self.x, self.y)
            self.pose -= 92

class RUN:
    def enter(self, event):
        # print('ENTER RUN')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        # print('EXIT RUN')
        self.face_dir = self.dir


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * self.speed * game_framework.frame_time
        self.x = clamp(0, self.x, 1290)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(int(self.frame) * 100 + 1000, self.pose + 12, 100, 75, self.x, self.y)
            self.pose = 320
        elif self.dir == 1:
            self.image.clip_draw(int(self.frame) * 100 + 100, self.pose + 91, 100, 75, self.x, self.y)
            self.pose = -1
class JUMP:
    def enter(self, event):
        print('JUMP!')
        if self.isJump == 0:
            self.jump(1)
        elif self.isJump == 1:
            self.jump(2)
        pass

    def exit(self,event):
        pass

    def do(self):
        if self.isJump > 0:

            # if self.isJump == 2: # 이단 점프
            #     self.v = VELOCITY

            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0: # 속도가 0보다 클 때는 위로 올라감
                F = -(0.005 * self.m * (self.v **2))
            else: # 속도가 0보다 작을 때는 아래로 내려감
                F = (0.005 * self.m * (self.v **2))

            self.y -= round(F) # 좌표 반영하기

            self.v -= 0.009 # 속도 줄이기

            if self.y-20 < 100: # 바닥에 닿았을때 변수 리셋
                self.y = 120
                self.isJump = 0
                self.v = VELOCITY
        pass

    def draw(self):
        if self.dir == 1: # 오른쪽을 향할 때
            self.image.clip_draw(600, 91, 100, 75, self.x, self.y)
        elif self.dir == -1: # 왼쪽을 향할때
            self.image.clip_draw(700, 335, 100, 75, self.x, self.y)
        elif self.dir == 0:  # 스탠딩
            self.image.clip_draw(600, 91, 100, 75, self.x, self.y)
        pass

next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE},
}

class Mario:
    def __init__(self): # 초기화
        self.image = load_image('SmallMario.png')
        # self.bigform = load_image('BigMario.png')
        self.dir, self.face_dir = 0, 1
        self.x, self.y = 1400 // 2, 25 + 100 # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0
        self.isJump = 0 # 점프 확인
        self.v = VELOCITY # 속도
        self.m = MASS # 질량
        self.life = 1
        self.state = None
        self.speed = MOVE_SPEED_PPS

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def draw(self): #그리기
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def jump(self, j): # 점프 상태 체크
        self.isJump = j

    def update(self): # 이동 관련
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_events(self, event):
        # events = get_events()
        # for event in events:
        #     if event.type == SDL_QUIT:
        #         game_framework.quit()
        #     elif event.type == SDL_KEYDOWN:
        #         if event.key == SDLK_ESCAPE:
        #             game_framework.quit()
        #         elif event.key == SDLK_RIGHT:
        #             self.dir += 1
        #         elif event.key == SDLK_LEFT:
        #             self.dir -= 1
        #         elif event.key == SDLK_SPACE:
        #             if self.isJump == 0:
        #                 self.jump(1)
        #             elif self.isJump == 1:
        #                 self.jump(2)
        #     elif event.type == SDL_KEYUP:
        #         if event.key == SDLK_RIGHT:
        #             self.dir -= 1
        #         elif event.key == SDLK_LEFT:
        #             self.dir += 1
        #         # elif event.key == SDLK_SPACE:
        #         #     if mario.isJump == 1:
        #         #         mario.jump(0)
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                JUMP.enter(self,event)

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 10

    def handle_collision(self, other, group):
        self.speed = self.speed * 2
        pass


