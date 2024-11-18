from pico2d import *
import game_framework

import game_world
from enemy import Crabmeat
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
font = None

score = 0
time_elapsed = 0
rings_collected = 0

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
    global camera_x, bgm, jump_sound, ground, background, sonic, rings, font, enemies
    camera_x = 0

    font = load_font('NiseSegaSonic.TTF', 20)

    # 배경 및 지형 초기화
    background = Background()
    ground = Ground()
    sonic = Sonic(ground)
    enemies = [Crabmeat(sonic) for _ in range(5)]

    rings = [Ring(300 + i * 100, 300, sonic) for i in range(10)]
    game_world.add_objects(rings, 3)

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    game_world.add_object(ground, 1)
    game_world.add_object(sonic, 2)
    game_world.add_objects(enemies, 2)

    # 충돌 체크 그룹
    for enemy in enemies:
        game_world.add_collision_pair(sonic, enemy, 'sonic:crabmeat')

    # 배경음악
    bgm = load_music('green_hill_zone_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    jump_sound = load_wav('jump.mp3')
    jump_sound.set_volume(64)

def finish():
    game_world.clear()

def update():
    global camera_x, time_elapsed
    camera_x = sonic.x - 400
    max_camera_x = background.map_width - 800
    camera_x = max(0, min(camera_x, max_camera_x))

    time_elapsed += game_framework.frame_time

    game_world.handle_collisions()

    game_world.update()

def draw():
    clear_canvas()
    background.draw(camera_x)
    game_world.render(camera_x)

    draw_ui()

    update_canvas()

def draw_ui():
    global font, score, time_elapsed, rings_collected

    minutes = int(time_elapsed // 60)
    seconds = int(time_elapsed % 60)
    time_display = f"{minutes}:{seconds:02}"

    font.draw(20, 570, f"SCORE: {score}", (255, 255, 0))            # 점수
    font.draw(20, 540, f"TIME: {time_display}", (255, 255, 0))      # 경과 시간
    font.draw(20, 510, f"RINGS: {rings_collected}", (255, 255, 0))  # 링 개수

def pause():
    pass

def resume():
    pass
