from pico2d import *
import game_framework
import game_world

from Background import stage1
from Items import Mushroom, Fire_Flower, Star
from Mario import Mario
from Enemy import Goomba, KoopaTroopa, RedTroopa
from Tiles import ItemBox, Pipe, Brick
import server

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.mario.handle_events(event)

# 초기화
def enter():
    server.mario = Mario()
    server.items = []
    server.enemy = [Goomba(), KoopaTroopa(), RedTroopa()]
    server.back = stage1()
    server.tiles = []
    game_world.add_object(server.back, 0)
    game_world.add_object(server.mario, 1)
    for item in server.items:
        game_world.add_object(item, 1)
    for mob in server.enemy:
        game_world.add_object(mob, 1)
    # for tile in server.tiles:
    #     game_world.add_object(tile, 1)

    with open("C:/2DGP_Project/object_map/brick_map.json") as f:
        brick_list = json.load(f)
        for o in brick_list:
            brick = Brick(o['x'], o['y'], o['w'])
            game_world.add_object(brick, 1)
            game_world.add_collision_pairs(server.mario, brick, 'mario:block')
            server.tiles.append(brick)

    with open("C:/2DGP_Project/object_map/pipe_map.json") as f:
        pipe_list = json.load(f)
        for o in pipe_list:
            pipe = Pipe(o['x'], o['y'], o['h'])
            game_world.add_object(pipe, 1)
            game_world.add_collision_pairs(server.mario, pipe, 'mario:block')
            server.tiles.append(pipe)

    with open("C:/2DGP_Project/object_map/mushroom_map.json") as f:
        mushroom_list = json.load(f)
        for o in mushroom_list:
            mushroom = Mushroom(o['x'], o['y'], o['dir'])
            game_world.add_object(mushroom, 1)
            game_world.add_collision_pairs(server.mario, mushroom, 'mario:mushroom')
            server.items.append(mushroom)

    with open("C:/2DGP_Project/object_map/flower_map.json") as f:
        fire_flower_list = json.load(f)
        for o in fire_flower_list:
            fire_flower = Fire_Flower(o['x'], o['y'])
            game_world.add_object(fire_flower, 1)
            game_world.add_collision_pairs(server.mario, fire_flower, 'mario:fire_flower')
            server.items.append(fire_flower)


    # 충돌대상 정보 등록
    game_world.add_collision_pairs(server.items, server.tiles, 'item:wall')
    game_world.add_collision_pairs(server.items, server.tiles, 'item:floor')
    game_world.add_collision_pairs(server.mario, server.enemy, "mario:enemy")
    game_world.add_collision_pairs(server.mario, server.tiles, "mario:block")
    game_world.add_collision_pairs(server.items, server.tiles, "item:wall")
    game_world.add_collision_pairs(server.enemy, server.tiles, "enemy:wall")
    game_world.add_collision_pairs(server.items, server.tiles, "item:floor")
    game_world.add_collision_pairs(server.enemy, server.tiles, "enemy:floor")

# 종료
def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            # print('Collision', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
        if floor_collide(a, b):
            # print('Floor_Collision', group)
            a.handle_floor_collision(b, group)
            b.handle_floor_collision(a, group)
        elif side_collide(a, b):
            # print('Side_Collision', group)
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

def collide(a,b): # 일반 충돌 판정
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def floor_collide(a,b): # 바닥 충돌 판정 (a가 b를 밟았을 때)
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if lb < (la + ra) / 2 < rb:
        if ba > tb :
            return False
        if ta < bb :
            return False
        return True

def side_collide(a,b): # 측면 충돌 판정
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if bb < (ta + ba) / 2 < tb:
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
