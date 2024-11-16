from pico2d import *
import game_framework

import game_world
from ground import Ground, Background
from ring import Ring
from sonic import Sonic

# 전역 변수
camera_x = 0
bgm = None
jump_sound = None
ground = None
background = None
sonic = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                sonic.handle_event(event)

def init():
    global camera_x, bgm, jump_sound, ground, background, sonic, rings
    camera_x = 0

    # 배경 및 지형 초기화
    background = Background()
    ground = Ground()
    sonic = Sonic(ground)

    rings = [Ring(300 + i * 100, 150) for i in range(10)]
    for ring in rings:
        game_world.add_object(ring, 2)

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(ground, 1)
    game_world.add_object(sonic, 2)

    # 배경음악
    bgm = load_music('green_hill_zone_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    jump_sound = load_wav('jump.mp3')
    jump_sound.set_volume(64)

def finish():
    game_world.clear()

def update():
    global camera_x
    camera_x = sonic.x - 400
    max_camera_x = background.map_width - 800
    camera_x = max(0, min(camera_x, max_camera_x))
    game_world.update()

def draw():
    clear_canvas()
    background.draw(camera_x)
    game_world.render(camera_x)
    update_canvas()

def pause():
    pass

def resume():
    pass
