from pico2d import *
import game_world
import server
class Tile:
    def __init__(self):
        self.x, self.y = 770 ,255
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

class Brick:
    def __init__(self):
        self.x, self.y = 1050, 440
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

class Item_Box:
    def __init__(self):
        self.x, self.y = 1050 ,255
        self.w, self.h = 240, 50
        self.image = load_image('C:/2DGP_Project/image/Tiles.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x-(self.w/2), self.y-(self.h/2), self.x+(self.w/2),self.y+(self.h/2)

    def handle_collision(self, other, group):
        if group == 'mario:item':
            pass

    def handle_side_collision(self, other, group):
        if group == 'item:wall':
            pass

    def handle_floor_collision(self, other, group):
        if group == 'item:floor':
            pass

class Pipe:
    def __init__(self):
        self.image = load_image('C:/2DGP_Project/image/Tiles.png')
        self.w, self.h = 90, 100
        self.dis = 35
        self.x, self.y = 1355, 135

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

class Grid:
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

