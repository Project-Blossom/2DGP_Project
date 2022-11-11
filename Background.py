from pico2d import *

class stage1:
    def __init__(self):
        self.x = 1400 // 2
        self.y = 700 // 2
        self.image = load_image('1stage.png')


    def draw(self):
        self.image.draw()