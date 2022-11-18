from pico2d import *
import game_framework
import game_world

from Background import stage1
from Items import Mushroom, Fire_Flower, Star
from Mario import Mario
from Enemy import Goomba, KoopaTroopa, RedTroopa
from Tiles import Tile, Item_Box, Pipe, Brick

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
    enemy = [Goomba(), KoopaTroopa(), RedTroopa()]
    back = stage1()
    tiles = [Tile(), Brick(),Item_Box(), Pipe()]
    game_world.add_object(back, 0)
    game_world.add_object(mario, 1)
    for item in items:
        game_world.add_object(item, 1)
    for mob in enemy:
        game_world.add_object(mob, 1)
    for tile in tiles:
        game_world.add_object(tile, 1)

    # 충돌대상 정보 등록

    game_world.add_collision_pairs(mario, items, "mario:item")
    game_world.add_collision_pairs(mario, enemy, "mario:enemy")
    game_world.add_collision_pairs(mario, tiles, "mario:block")
    game_world.add_collision_pairs(items, tiles, "item:wall")
    game_world.add_collision_pairs(enemy, tiles, "enemy:wall")
    game_world.add_collision_pairs(items, tiles, "item:floor")
    game_world.add_collision_pairs(enemy, tiles, "enemy:floor")

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
        if floor_collide(a, b):
            print('Floor_Collision', group)

            a.handle_floor_collision(b, group)
            b.handle_floor_collision(a, group)
        elif side_collide(a, b):
            print('Side_Collision', group)
            a.handle_side_collision(b, group)
            b.handle_side_collision(a, group)



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

def floor_collide(a,b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if lb+5 < la < rb-5 or lb+5 < ra < rb-5:
        if ba > tb:
            return False
        if ta < bb:
            return False
        return True

def side_collide(a,b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if bb+1 < ta < tb-1 or bb+1 < ba < tb-1:
        if la > rb:
            return False
        if ra < lb:
            return False
        return True

def test_self():
    import play_state

    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
