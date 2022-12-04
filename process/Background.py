from pico2d import *
from Mario import Mario
import server
class Title:
    def __init__(self):
        self.image = load_image('C:/2DGP_Project/image/title.png')
        self.bgm = load_music('C:/2DGP_Project/sound/title.mp3')
        self.bgm.set_volume(20)
        self.bgm.play(1)

    def draw(self):
        self.image.draw(1400 // 2, 700 // 2)

    def update(self):
        pass

class Stage1:
    def __init__(self):
        self.stage1 = [load_image(f'C:/2DGP_Project/image/1stage-{num}.png') for num in range(2)]
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 4850 * 2
        self.bgm = load_music('C:/2DGP_Project/sound/Overworld.mp3')
        self.bgm.set_volume(22)
        self.bgm.repeat_play()
        self.window_left = 0

    def draw(self):
        self.window_left = clamp(0,
                                 int(server.mario.x) - self.canvas_width // 2,
                                 self.w - self.canvas_width - 1)

        tile_left = self.window_left // 4850
        tile_right = (self.window_left + self.canvas_width) // 4850
        left_offset = self.window_left % 4850

        for tx in range(tile_left, tile_right + 1):
            self.stage1[tx].draw_to_origin(-left_offset + (tx - tile_left) * 4850, 0)

    def update(self):
        # self.window_left = clamp(0,
        #                          int(server.mario.x) - self.canvas_width // 2, self.w - self.canvas_width - 1)
        pass
