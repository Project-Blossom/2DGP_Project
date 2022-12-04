from pico2d import *
import time
import pickle

class Timer:
    def __init__(self):
        self.font = load_font('C:/2DGP_Project/font/NanumMyeongjo-YetHangul.TTF', 80)
        self.small_font = load_font('C:/2DGP_Project/font/NanumMyeongjo-YetHangul.TTF', 30)
        self.w, self.h = 300,90
        self.set_timer = time.time()
        self.recorded = 0.0
        with open('C:/2DGP_Project/save/data.recorded', 'rb') as f:
            self.recorded = pickle.load(f)

    def update(self):
        self.cur_time = time.time() - self.set_timer
        pass

    def draw(self, x=20, y=650, rgb=[238, 238, 238]):
        self.font.draw(x, y, f'{int(self.cur_time // 60)}min {self.cur_time % 60:.1f}sec', rgb)
        if self.recorded != 0.0:
            self.small_font.draw(x, y-50, f'previous record : {int(self.recorded // 60)}min {self.recorded % 60:.1f}sec', rgb)
        pass

    def draw_cur_record(self, x=20, y=660, rgb=[238, 238, 238]):
        self.font.draw(x, y, f'{int(self.cur_time // 60)}min {self.cur_time % 60:.1f}sec', rgb)

    def record(self):
        self.recorded = self.cur_time
        return self.recorded