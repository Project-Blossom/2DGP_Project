from pico2d import *
import game_framework
import Mario
import main as screen

image = None

def enter():
    global image
    image = load_image('item_panel.png')
    pass

def exit():
    global image
    del image
    pass

def update():
    pass

def draw():
    clear_canvas()
    Mario.draw()
    image.draw(screen.WIDTH // 2, screen.HEIGHT // 2)
    update_canvas()
    pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_state()
                case pico2d.SDLK_1:
                    Mario.spawnmush = 1
                    game_framework.pop_state()






