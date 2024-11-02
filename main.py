from pico2d import *

from sonic import Sonic
from ground import Ground

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                sonic.handle_event(event)


def reset_world():
    global running
    global ground
    global world
    global sonic
    global camera_x
    global bgm

    running = True
    world = []
    camera_x = 0

    grass = Ground()
    world.append(grass)

    sonic = Sonic()
    world.append(sonic)

    bgm = load_music('green_hill_zone_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

def update_world():
    global camera_x

    camera_x = sonic.x - 400
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw(camera_x)
    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()