from pico2d import *

class stage1:
    def __init__(self):
        self.image = load_image('1stage-1.png')
        self.image.clip_image(*screen_scale())

    def draw(self):
        self.image.draw(4900 - 1400 - 700, 350)

    def update(self):
        pass

def screen_scale():
    return 0,0,1400,700