from pico2d import *
import maingame as screen

class Goomba:
    def __init__(self):
        self.image = load_image("Monsters.png")
        self.dir_x = 1
        self.x, self.y = screen.WIDTH // 2, 35 + 200  # 초기 위치 (화면 하단 중앙)
        self.frame = 0

    def draw(self): #그리기
            self.image.clip_draw(self.frame * 80 , 780, 50, 50, self.x, self.y)

    def screen_check(self): # 화면 밖으로 못나가게 하기
        if self.x > screen.WIDTH:
            self.x = screen.WIDTH
            self.dir_x = -1

        elif self.x < 0:
            self.x = 0
            self.dir_x = 1

    def update(self): # 이동 관련
        self.frame = (self.frame + 1) % 3
        self.x += self.dir_x * 1

class KoopaTroopa:
    def __init__(self):
        self.image = load_image("Monsters.png")
        self.dir_x = 0
        self.x, self.y = screen.WIDTH // 2, 35 + 200  # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0

    def draw(self): #그리기
        if self.dir_x == 1: # 오른쪽을 향할 때
            self.image.clip_draw(self.frame * 100 + 100, self.pose + 91, 100, 75, self.x, self.y)
            self.pose = -1
        elif self.dir_x == -1: # 왼쪽을 향할때
            self.image.clip_draw(self.frame * 100 + 1000, self.pose + 12, 100, 75, self.x, self.y)
            self.pose = 320
        elif self.dir_x == 0: # 스탠딩
            self.image.clip_draw(0, self.pose, 100, 75, self.x, self.y)
            self.pose -= 92

    def screen_check(self): # 화면 밖으로 못나가게 하기
        if self.x > screen.WIDTH:
            self.x = screen.WIDTH
            self.dir_x = -1

        elif self.x < 0:
            self.x = 0
            self.dir_x = 1

    def update(self): # 이동 관련
        self.frame = (self.frame + 1) % 2
        self.x += self.dir_x * 1