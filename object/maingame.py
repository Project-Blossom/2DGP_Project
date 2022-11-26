from pico2d import *
import game_framework
import play_state
import title_state

WIDTH, HEIGHT = 1400, 700

open_canvas(WIDTH, HEIGHT)
game_framework.run(play_state)
close_canvas()
