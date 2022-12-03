from pico2d import *
import game_framework
import play_state

running = True
image = None


def enter():
    global image
    image = load_image('C:/2DGP_Project/image/title.png')
    pass

def exit():
    global image
    del image
    # fill here
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(1400 // 2, 700 // 2)
    update_canvas()
    # fill here
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