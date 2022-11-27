from pico2d import *
from Mario import Mario
import server
class stage1:
    def __init__(self):
        self.stage1 = load_image('C:/2DGP_Project/image/1stage-1.png')
        # self.stage1_2 = load_image('1stage-2.png')
        # self.image.clip_image(*screen_scale())
        self.loc = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.stage1.w

    def draw(self):
        # self.image.draw(4900 - 1400 - 700, 350)
        # self.stage1.clip_draw(0 , 0, 1400, 700, 700, 350)
        self.stage1.clip_draw_to_origin(
            self.window_left, 0,
            self.canvas_width, self.canvas_height,
            0, 0)


    def update(self):
        # self.loc += 1
        self.window_left = clamp(0,
                                 int(server.mario.x) - self.canvas_width // 2, self.w - self.canvas_width - 1)
        pass

def screen_scale():
    return 0,0,1400,700