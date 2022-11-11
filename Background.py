from pico2d import *

class stage1:
    def __init__(self):
        self.image = load_image('11stage.png')
        self.image.clip_image(*screen_scale())

    def draw(self):
        self.image.draw(700, 350)

    def update(self):
        pass

def screen_scale():
    return 0,0,1400,700