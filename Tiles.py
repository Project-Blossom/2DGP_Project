from pico2d import *


class Tile:
    def __init__(self):
        self.x, self.y = 24 ,24
        self.image = load_image('Tiles.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 24, self.y - 24, self.x + 24, self.y + 24

class Item_Box:
    def __init__(self):
        self.x, self.y = 1100 ,250
        self.image = load_image('Tiles.png')

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 24, self.y - 24, self.x + 24, self.y + 24

class Pipe:
    def __init__(self):
        self.image = load_image('Tiles.png')
        self.x, self.y = 1350, 150

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x-50, self.y-50, self.x+50,self.y+50

class Grid:
    def __init__(self):
        self.image = load_image('Tiles.png')
        self.x, self.y = 0, 0

    def update(self):
        pass

    def draw(self):
        for i in range(30):
            for j in range(60):
                draw_rectangle(self.x + j * 46,self.y + i*46,self.x + (j+1) * 46,self.x + (i+1) * 46)

