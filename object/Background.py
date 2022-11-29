from pico2d import *
from Mario import Mario
import server
class stage1:
    def __init__(self):
        self.stage1 = [load_image(f'C:/2DGP_Project/image/1stage-{num}.png') for num in range(2)]
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 4850 * 2

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
