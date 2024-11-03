from pico2d import *

from sonic import Sonic
from ground import Ground, Background

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
    global running, background, world, sonic, camera_x, bgm

    running = True
    world = []
    camera_x = 0

    # 뒷배경
    background = Background()
    world.append(background)

    # 지형
    ground = Ground()
    world.append(ground)

    # 소닉(플레이어)
    sonic = Sonic(ground)
    world.append(sonic)

    # 배경음악
    bgm = load_music('green_hill_zone_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

def update_world():
    global camera_x

    # 소닉이 카메라 중앙에 보이도록
    camera_x = sonic.x - 400
    max_camera_x = background.map_width - 800
    # 카메라가 설정된 범위를 벗어나지 않도록 제한함
    camera_x = max(0, min(camera_x, max_camera_x))

    for o in world:
        o.update()

def render_world():
    clear_canvas()
    background.draw(camera_x)
    for o in world:
        o.draw(camera_x)
    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.016)

close_canvas()