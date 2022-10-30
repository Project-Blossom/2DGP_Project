from pico2d import *
import maingame as screen

class Goomba:
    def __init__(self):
        self.image = load_image("Monsters.png")
        self.dir_x = 0
        self.x, self.y = screen.WIDTH // 2, 35 + 200  # 초기 위치 (화면 하단 중앙)
        self.pose = 0
        self.frame = 0

    def draw(self): #그리기
        if self.dir_x == 1: # 오른쪽을 향할 때
            if self.isJump > 0: # 점프할 때
                if self.state == 'mushroom':
                    self.bigform.clip_draw(600, 91 + 50, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(600, 91, 100, 75, self.x, self.y)
            else:
                if self.state == 'mushroom':
                    self.bigform.clip_draw(self.frame * 100 + 100, self.pose + 91 + 192, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(self.frame * 100 + 100, self.pose + 91, 100, 75, self.x, self.y)
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
                    self.bigform.clip_draw(self.frame * 100 + 1000, self.pose + 12 + 272, 100, 110, self.x, self.y)
                else:
                    self.smallform.clip_draw(self.frame * 100 + 1000, self.pose + 12, 100, 75, self.x, self.y)
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