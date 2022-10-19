from pico2d import *
import game_framework
import Mario

WIDTH, HEIGHT = 1400, 700

open_canvas(WIDTH, HEIGHT)
game_framework.run(Mario)
close_canvas()
