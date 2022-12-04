import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from pico2d import *
import game_framework
import play_state
import title_state
import server
import pickle
image = None
recorded = 0.0
def enter():
    global image, recorded
    image = load_image('C:/2DGP_Project/image/clear.png')
    recorded = server.timer.record()
    save(recorded)
    pass

def exit():
    global image
    del image
    pass

def update():
    pass

def draw():
    clear_canvas()
    play_state.draw_world()
    image.draw(700,350)
    server.timer.draw_cur_record(600 - server.timer.w / 2, 350 - server.timer.h / 2, [250, 250, 250])
    update_canvas()
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.pop_state()

def save(data):
    with open('C:/2DGP_Project/save/data.recorded', 'wb') as f:
        pickle.dump(data, f)
