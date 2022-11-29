from pico2d import *
import game_world
import server
class Brick: #1F_singleblock
    def __init__(self, x=0,y=0,w=0):
        self.x, self.y = x, y
        self.w, self.h = w, 50
        self.image = load_image('C:/2DGP_Project/image/Tiles.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x-(self.w/2), self.y-(self.h/2), self.x+(self.w/2),self.y+(self.h/2)

    def handle_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            pass

class ItemBox: #2F_singleblock
    def __init__(self,x=0,y=0):
        self.x, self.y = x, y
        self.w, self.h = 50, 50
        self.image = load_image('C:/2DGP_Project/image/Tiles.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x-(self.w/2), self.y-(self.h/2), self.x+(self.w/2),self.y+(self.h/2)

    def handle_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            pass


class Pipe:
    def __init__(self,x=0,y=0,h=0):
        self.image = load_image('C:/2DGP_Project/image/Tiles.png')
        self.w = 80
        self.h = h
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x-(self.w/2), self.y-(self.h/2), self.x+(self.w/2),self.y+(self.h/2)

    def handle_collision(self, other, group):
        pass

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            pass

class Grid: #디버그용 격자무늬
    def __init__(self):
        self.image = load_image('C:/2DGP_Project/image/Tiles.png')
        self.x, self.y = 0, 0

    def update(self):
        self.x -= server.mario.x
        pass

    def draw(self):
        # for i in range(30):
        #     for j in range(60):
        #         draw_rectangle(self.x + j * 46,self.y + i*46,self.x + (j+1) * 46,self.x + (i+1) * 46)
        pass

