from pico2d import *
from Mario import Mario
class stage1:
    def __init__(self):
        self.stage1 = load_image('C:/2DGP_Project/image/1stage-1.png')
        # self.stage1_2 = load_image('1stage-2.png')
        # self.image.clip_image(*screen_scale())
        self.loc = 0

    def draw(self):
        # self.image.draw(4900 - 1400 - 700, 350)
        self.stage1.clip_draw(0 , 0, 1400, 700, 700, 350)


    def update(self):
        # self.loc += 1
        pass

def screen_scale():
    return 0,0,1400,700