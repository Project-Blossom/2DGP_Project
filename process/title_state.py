from pico2d import *
import game_framework
import play_state
from Background import Title


title = None

def enter():
    global title
    title = Title()
    pass

def exit():
    global title
    del title
    pass

def update():
    pass

def draw():
    clear_canvas()
    title.draw()
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
            game_framework.change_state(play_state)