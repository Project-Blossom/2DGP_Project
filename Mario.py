from pico2d import *
import game_framework
import main as screen

VELOCITY = 4
MASS = 2

class Mario:
    def __init__(self):
        self.image = load_image('SmallMario.png')
        self.dir_x = 0
        self.x, self.y = screen.WIDTH // 2, screen.HEIGHT // 2
        self.rect = None
        self.pose = 0
        self.frame = 0
        self.isJump = 0
        self.v = VELOCITY
        self.m = MASS

    def draw(self):
        if self.dir_x == 1:
            self.image.clip_draw(self.frame * 100 + 100, self.pose + 80, 100, 75, self.x, self.y)
            self.pose = 90
        elif self.dir_x == -1:
            self.image.clip_draw(self.frame * 100 + 1000, self.pose + 412, 100, 75, self.x, self.y)
            self.pose = 0
        elif self.dir_x == 0:
            self.pose += 90
            self.image.clip_draw(0, 170, 100, 75, self.x, self.y)
            self.pose -= 90

    def screen_check(self):
        self.frame = (self.frame + 1) % 3
        self.x += self.dir_x * 1
        if self.x > screen.WIDTH:
            self.x = screen.WIDTH

        elif self.x < 0:
            self.x = 0

def handle_events():
    global playing, mario
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RIGHT:
                mario.dir_x += 1
            elif event.key == SDLK_LEFT:
                mario.dir_x -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir_x -= 1
            elif event.key == SDLK_LEFT:
                mario.dir_x += 1

playing = True
mario = None


def enter():
    global mario, playing
    mario = Mario()
    playing = True

def update():
    global mario
    mario.screen_check()


def draw():
    clear_canvas()
    mario.draw()
    update_canvas()
def exit():
    quit()

