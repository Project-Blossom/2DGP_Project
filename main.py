import Mario
import game_framework
from pico2d import *

WIDTH, HEIGHT = 1280, 800

open_canvas(WIDTH, HEIGHT)
game_framework.run(Mario)
close_canvas()
