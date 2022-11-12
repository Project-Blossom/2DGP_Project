from pico2d import *
import game_framework
import game_world

from Background import stage1
from Items import Mushroom, Fire_Flower, Star
from Mario import Mario
from Enemy import Goomba, KoopaTroopa
from Tiles import Tile, Item_Box, Pipe, Grid

mario = None
enemy = []
items = []
back = None
tiles = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            mario.handle_events(event)

# 초기화
def enter():
    global mario, items, enemy, back, tiles
    mario = Mario()
    items = [Mushroom(), Fire_Flower(), Star()]
    enemy = [Goomba(), KoopaTroopa()]
    back = stage1()
    tiles = [Tile(), Item_Box(), Pipe(), Grid()]
    game_world.add_object(back, 0)
    game_world.add_object(mario, 1)
    for item in items:
        game_world.add_object(item, 1)
    for mob in enemy:
        game_world.add_object(mob, 1)
    for tile in tiles:
        game_world.add_object(tile, 1)

    # 충돌대상 정보 등록
    game_world.add_collision_pairs(mario, items[0], "mario:mushroom")

# 종료
def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('Collision', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def collide(a,b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def test_self():
    import play_state

    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
