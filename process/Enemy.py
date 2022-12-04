from pico2d import *
# import maingame as screen
import game_framework
import game_world
import server

Floor = 100

PIXEL_PER_METER = (50.0/1.0) # 50 pixel 1m
MOVE_SPEED_KMPH = 8.0
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Goomba:
    image = None
    stamp_sound = None
    def __init__(self, x=0, y=0):
        if self.image is None:
            self.image = load_image('C:/2DGP_Project/image/Monsters.png')
        if Goomba.stamp_sound is None:
            Goomba.stamp_sound = load_wav('C:/2DGP_Project/sound/Squish.wav')
            Goomba.stamp_sound.set_volume(15)
        self.w, self.h = 40, 48
        self.dir_x = -1
        self.x, self.y = x, y
        self.frame = 0
        self.timer = 100
        self.state = None

    def draw(self): #그리기
        sx, sy = self.x - server.back.window_left, self.y
        if self.state == 'dead':
            self.image.clip_draw(2 * 64 + 67, 781, 64, 50, sx, sy)
        else:
            self.image.clip_draw(int(self.frame) * 64 + 67, 781, 64, 50, sx, sy)
        # draw_rectangle(*self.get_bb())


    def update(self):

        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor):
            self.y -= 1.5 * MOVE_SPEED_PPS * game_framework.frame_time
            clamp(Floor + self.h / 2, self.y, 1000)
        wl, wr = server.back.window_left, server.back.window_left + server.back.canvas_width
        if wl + 5 < self.x < wr - 5 :
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time
        if self.state == 'dead':
            self.timer -= 1
        if self.timer < 0:
            game_world.remove_object(self)


    def get_bb(self):
        return self.x - 20, self.y - 24, self.x + 20, self.y + 24

    def handle_collision(self, other, group):
        if group == 'mario:enemy':
            pass

    def handle_side_collision(self, other, group):
        if group == 'enemy:wall':
            self.dir_x = -self.dir_x
        if group == 'mario:enemy':
            if other.state == 'invincible':
                self.stamp_sound.play()
                self.dir_x = 0
                self.state = 'dead'
            else:
                pass
            pass

    def handle_floor_collision(self, other, group):
        if group == 'enemy:floor':
            self.y = other.y + other.h/2 + 1 + 25
        if group == 'mario:enemy':
            if self.y > other.y:
                pass
            else:
                self.stamp_sound.play()
                self.dir_x = 0
                self.state = 'dead'
            pass

class KoopaTroopa:
    image = None
    stamp_sound = None
    kick_sound = None
    def __init__(self, x=0, y=0):
        if self.image is None:
            self.image = load_image("C:/2DGP_Project/image/Monsters.png")
        if KoopaTroopa.stamp_sound is None:
            KoopaTroopa.stamp_sound = load_wav('C:/2DGP_Project/sound/Squish.wav')
            KoopaTroopa.stamp_sound.set_volume(15)
        if KoopaTroopa.kick_sound is None:
            KoopaTroopa.kick_sound = load_wav('C:/2DGP_Project/sound/Kick.wav')
            KoopaTroopa.kick_sound.set_volume(15)
        self.dir_x = -1
        self.x, self.y = x, y
        self.w, self.h = 50, 60
        self.pose = 0
        self.frame = 0
        self.state = None

    def draw(self): #그리기
        sx, sy = self.x - server.back.window_left, self.y
        if self.state == None:
            if self.dir_x == 1: # 오른쪽을 향할 때
                self.image.clip_draw(int(self.frame) * 64 + 67, 520, 64, 75, sx, sy)
            elif self.dir_x == -1: # 왼쪽을 향할때
                self.image.clip_composite_draw(int(self.frame) * 64 + 67, 520, 64, 75, 0,'h',sx, sy, 64, 75)
        else:
            self.image.clip_draw(int(self.frame) * 64 + 67, 450, 64, 75, sx, sy)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor):
            self.y -= 2.0 * MOVE_SPEED_PPS * game_framework.frame_time
        wl, wr = server.back.window_left, server.back.window_left + server.back.canvas_width
        if wl + 5 < self.x < wr - 5:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time
        if self.y < 0:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x-(self.w/2), self.y-(self.h/2), self.x+(self.w/2),self.y+(self.h/2)

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
            if self.y > other.y:
                pass
            else:
                if self.state == 'STAMPED':
                    self.kick_sound.play()
                    self.dir_x = 2
                else:
                    self.stamp_sound.play()
                    self.state = 'STAMPED'
                    self.dir_x = 0
            pass

class RedTroopa:
    image = None
    stamp_sound = None
    kick_sound = None
    def __init__(self, x=0, y=0):
        if self.image is None:
            self.image = load_image("C:/2DGP_Project/image/Monsters.png")
        if RedTroopa.stamp_sound is None:
            RedTroopa.stamp_sound = load_wav('C:/2DGP_Project/sound/Squish.wav')
            RedTroopa.stamp_sound.set_volume(15)
        if RedTroopa.kick_sound is None:
            RedTroopa.kick_sound = load_wav('C:/2DGP_Project/sound/Kick.wav')
            RedTroopa.kick_sound.set_volume(15)
        self.dir_x = -1
        self.x, self.y = x, y
        self.w, self.h = 50, 60
        self.pose = 0
        self.frame = 0
        self.state = None

    def draw(self): #그리기
        sx, sy = self.x - server.back.window_left, self.y
        if self.state == None:
            if self.dir_x == 1: # 오른쪽을 향할 때
                self.image.clip_draw(int(self.frame) * 64 + 67*6-10, 520, 64, 75, sx, sy)
            elif self.dir_x == -1: # 왼쪽을 향할때
                self.image.clip_composite_draw(int(self.frame) * 64 + 67*6, 520, 64, 75, 0,'h',sx, sy, 64, 75)
        else:
            self.image.clip_draw(int(self.frame) * 64 + 67 * 6 - 10, 450, 64, 75, sx, sy)
        # draw_rectangle(*self.get_bb())

    def update(self):
        if 3230 < self.x < 3300 or 4030 < self.x < 4135 or 7160 < self.x < 7210 or (self.y - 20 > Floor):
            self.y -= 1 * MOVE_SPEED_PPS * game_framework.frame_time
        wl, wr = server.back.window_left, server.back.window_left + server.back.canvas_width
        if wl + 5 < self.x < wr - 5:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            self.x += self.dir_x * MOVE_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        return self.x - (self.w / 2), self.y - (self.h / 2), self.x + (self.w / 2), self.y + (self.h / 2)

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
            if other.get_bb()[0] + 10 < self.x < other.get_bb()[2] - 10:
                pass
            else:
                self.dir_x = -self.dir_x

        if group == 'mario:enemy':
            if self.y > other.y:
                pass
            else:
                if self.state == 'STAMPED':
                    self.kick_sound.play()
                    self.dir_x = 2
                else:
                    self.stamp_sound.play()
                    self.state = 'STAMPED'
                    self.dir_x = 0
            pass
