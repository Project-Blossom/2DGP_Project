from pico2d import *
import game_framework
import server

Floor = 100 # 바닥 높이
VELOCITY = 1
MASS = 50

PIXEL_PER_METER = (50.0/1.0) # 50 pixel 1m
MOVE_SPEED_KMPH = 10.0
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

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
        sx, sy = self.x - server.back.window_left, server.mario.y
        if self.dir == 0:
            self.pose += 92
            self.image.clip_draw(0, self.pose, 100, 75, sx, sy)
            self.pose -= 92
        self.font.draw(sx + 20, sy + 10, f'x={self.x:.2f},y={self.y:.2f}, speed={self.speed:.2f}',
                       (255, 255, 255))

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
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * self.speed) % 3
        self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time * self.speed
        self.x = clamp(1, self.x, 4850*2)

    def draw(self):
        sx, sy = self.x - server.back.window_left, server.mario.y
        if self.dir == -1:
            self.image.clip_draw(int(self.frame) * 100 + 1000, self.pose + 12, 100, 75, sx, sy)
            self.pose = 320
        elif self.dir == 1:
            self.image.clip_draw(int(self.frame) * 100 + 100, self.pose + 91, 100, 75, sx, sy)
            self.pose = -1
        self.font.draw(sx + 20, sy + 10, f'x={self.x:.2f},y={self.y:.2f}, speed={self.speed:.2f}',
                       (255, 255, 255))

class JUMP:
    def enter(self):
        # print('JUMP!')
        if self.isJump == 0:
            self.jump(1)
        elif self.isJump == 1:
            self.jump(2)
        pass

    def exit(self):
        pass

    def do(self):
        if self.isJump > 0:
            # self.jump_sound.play()
            # if self.isJump == 2: # 이단 점프
            #     self.v = VELOCITY

            # 역학공식 계산 (F). F = 0.5 * mass * velocity^2.
            if self.v > 0: # 속도가 0보다 클 때는 위로 올라감
                F = -(0.5 * self.m * (self.v **2))
            else: # 속도가 0보다 작을 때는 아래로 내려감
                F = (0.5 * self.m * (self.v **2))

            self.y -= F # * MOVE_SPEED_PPS * game_framework.frame_time # 좌표 반영하기
            # if(self.v > )
            self.v -= self.gravity

            if self.y-20 < Floor: # 바닥에 닿았을때 변수 리셋
                self.y = Floor + 20
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

class HITBACK:
    def do(self):
        if self.ishit > 0:
            if self.v <= 0:
                self.v = VELOCITY
                self.ishit = 0
            if self.v > 0:
                F = (0.2 * self.m * (self.v ** 2)) * MOVE_SPEED_PPS * game_framework.frame_time
            self.x -= F
            self.v -= 0.01

next_state = {
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE},
}

class Mario:
    jump_sound = None
    item_sound = None
    hit_sound = None
    dead_sound = None
    def __init__(self): # 초기화
        self.image = load_image('C:/2DGP_Project/image/SmallMario.png')
        if Mario.jump_sound is None:
            Mario.jump_sound = load_wav('C:/2DGP_Project/sound/Jump.wav')
            Mario.jump_sound.set_volume(15)
        if Mario.item_sound is None:
            Mario.item_sound = load_wav('C:/2DGP_Project/sound/Coin.wav')
            Mario.item_sound.set_volume(15)
        if Mario.hit_sound is None:
            Mario.hit_sound = load_wav('C:/2DGP_Project/sound/Thwomp.wav')
            Mario.hit_sound.set_volume(10)
        if Mario.dead_sound is None:
            Mario.dead_sound = load_wav('C:/2DGP_Project/sound/Die.wav')
            Mario.dead_sound.set_volume(15)
        self.font = load_font('C:/2DGP_Project/font/ENCR10B.TTF', 16) # 디버그용
        self.dir, self.face_dir = 0, 1
        self.x, self.y = 350, 50 + 900 # 초기 위치
        self.w, self.h = 40, 40
        self.isJump, self.ishit = 0, 0  # 점프 확인, 피격 확인
        self.v, self.m = VELOCITY, MASS  # 점프 인자
        self.pose = 0
        self.frame = 0
        self.speed = 0
        self.gravity = 0.035
        self.item_effect = 0
        self.state = None

        self.item_que = []
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def draw(self): #그리기
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())


    def jump(self, j): # 점프 상태 체크
        self.isJump = j

    def hit(self, h):
        self.ishit = h

    def update(self): # 이동 관련
        self.cur_state.do(self)
        self.speed = 0.5 + ((self.y-125)/150) + self.item_effect
        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor and self.isJump == 0):
            self.y -= 0.5 * self.m * (self.v ** 2) / 4 * MOVE_SPEED_PPS * game_framework.frame_time
        if self.y < 50:
            self.dead_sound.play()
            self.x, self.y = 350, 150
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

        if self.isJump > 0: # 점프
            JUMP.do(self)
        if self.ishit > 0:  # 적과 측면충돌했을때
            HITBACK.do(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def add_item(self, item):
        self.item_que.insert(0, item)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if (event.type, event.key) in key_event_table:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                if self.isJump == 0:
                    self.jump_sound.play()
                self.jump(1)
            if (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
                pass

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 10

    def handle_collision(self, other, group):
        if group == 'mario:mushroom':
            self.item_sound.play()
            self.item_effect += 0.5
        if group == 'mario:fire_flower':
            self.item_sound.play()
            self.m += 10
        if group == 'mario:star':
            self.item_sound.play()
            self.state = 'invincible'
        pass

    def handle_side_collision(self, other, group):
        if group == 'mario:enemy':
            if self.state != 'invincible':
                self.hit_sound.play()
                self.hit(1)
            pass
        if group == 'mario:block':
            if self.x < other.x:
                self.x = other.get_bb()[0] - 21
            if self.x > other.x:
                self.x = other.get_bb()[2] + 21
        pass

    def handle_floor_collision(self, other, group):
        if group == 'mario:enemy':
            if self.y > other.y:
                self.jump(1)
            else:
                self.hit_sound.play()
                self.hit(1)
        if group == 'mario:block':
            if self.y < other.y:
                self.y = other.get_bb()[1] - 11
                self.v = -self.v
            if self.y > other.y:
                self.y = other.get_bb()[3] + 31
                self.isJump = 0
                self.v = VELOCITY
            pass
        pass


