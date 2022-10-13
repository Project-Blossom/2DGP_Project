from pico2d import *

WIDTH, HEIGHT = 1280, 800

def handle_events():
    global running
    global dir_x
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1


open_canvas(WIDTH, HEIGHT)

character = load_image('SmallMario.png')

running = True
pose = 0
x, y = WIDTH // 2, HEIGHT // 2
frame = 0
dir_x = 0
dir_y = 0
accel = 0

while running:
    clear_canvas()
    if dir_x == 1 :
        character.clip_draw(frame * 100 + 100, pose+80, 100, 75, x, y)
        pose = 90
    elif dir_x == -1 :
        character.clip_draw(frame * 100 + 1000, pose+412, 100, 75, x, y)
        pose = 0
    elif dir_x == 0 :
        pose += 90
        character.clip_draw(0, 170, 100, 75, x, y)
        pose -= 90
    update_canvas()

    handle_events()
    delay(0.05)
    frame = (frame + 1) % 3
    if x + 10 <= WIDTH  and x - 10 >= 0 + 20:
        x += dir_x * 10
    elif x + 10 > WIDTH:
        x -= 10
    elif x - 10 < 0 + 20:
        x += 10

    delay(0.01)

close_canvas()

