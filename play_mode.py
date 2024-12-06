# play_mode.py
from pico2d import *
import game_framework

import game_world
import title_mode
from boss import Eggman, MetalBall
from enemy import Crabmeat, Caterkiller, Burrobot, BuzzBomber, Newtron, Batbrain
from ground import Ground, Background
from ring import Ring
from sonic import Sonic

# 전역 변수
camera_x = 0
camera_y = 0
bgm = None
jump_sound = None
ground = None
background = None
sonic = None
font = None

score = 0
time_elapsed = 0
rings_collected = 0

is_game_over = False
is_game_clear = False

boss_spawned = False
is_camera_locked = False

life_display = None
lives = 3

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r and is_game_over == True:
            game_framework.change_mode(title_mode)
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                sonic.handle_event(event)

def init():
    global camera_x, camera_y, bgm, jump_sound, ground, background, sonic, rings, font, font2, crabmeat, caterkiller,\
        burrobot, buzzbomber, newtron, batbrain, boss, life_display, lives, time_elapsed, rings_collected, is_game_over,\
        score, is_camera_locked, is_game_clear, boss_spawned
    is_game_over = False
    is_game_clear = False
    boss_spawned = False
    is_camera_locked = False
    camera_x = 0
    camera_y = 0
    time_elapsed = 0
    rings_collected = 0
    if lives == 0:
        score = 0
        lives = 3
    font = load_font('NiseSegaSonic.TTF', 20)
    font2 = load_font('NiseSegaSonic.TTF', 50)

    crabmeat_positions = [(1000, 100, 400), (4415, 305, 20), (16290, 178, 30)]
    caterkiller_positions = [(2800, 230, 200), (9610, 590, 250), (14100, 230, 200)]
    burrobot_positions = [(5200, 465, 500), (6000, 588, 200), (15300, 102, 500)]
    buzzbomber_positions = [(2000, 300, 1000), (6200, 720, 500), (6500, 700, 500), (7700, 1000, 1000)]
    newtron_positions = [(8830, 800, 200), (11000, 900, 200), (11100, 800, 100), (11200, 900, 200)]
    batbrain_positions = [(14200, 270, 300), (14645, 300, 200), (16600, 350, 300), (16900, 300, 200)]

    background = Background()
    ground = Ground()
    life_display = LifeDisplay(lives)
    crabmeat = [Crabmeat(sonic, x, y, move_range) for x, y, move_range in crabmeat_positions]
    caterkiller = [Caterkiller(sonic, x, y, move_range) for x, y, move_range in caterkiller_positions]
    burrobot = [Burrobot(sonic, x, y, move_range) for x, y, move_range in burrobot_positions]
    buzzbomber = [BuzzBomber(sonic, x, y, move_range) for x, y, move_range in buzzbomber_positions]
    newtron = [Newtron(sonic, x, y, move_range) for x, y, move_range in newtron_positions]
    batbrain = [Batbrain(sonic, x, y, move_range) for x, y, move_range in batbrain_positions]
    # boss = Eggman(sonic, 18900, 400, 250)
    # metal_ball = MetalBall(sonic, boss)
    # boss.metal_ball = metal_ball

    # 지형 초기화
    ground_positions = [
        # (x, y, 지형 타입)
        (256, 200, 'plane1'),
        (768, 200, 'plane1'),
        (1280, 200, 'platform'),
        (1792, 200, 'uphill1'),
        (2304, 200, 'bridge'),
        (2816, 200, 'plane2'),
        (3328, 200, 'downhill1'),
        (3840, 200, 'curve1'),
        (4352, 200, 'stair1'),
        (4864, 200, 'start_of_bridge'),
        (4992, 430, 'bridge'),
        (5504, 200, 'plane3'),
        (6016, 686, 'plane1'),
        (6016, 174, 'clean_wall'),
        (6528, 686, 'uphill1'),
        (6528, 174, 'clean_wall'),
        (7296, 686, 'twin'),
        (7296, 174, 'clean_wall'),
        (8064, 686, 'stair1'),
        (8064, 174, 'clean_wall'),
        (8576, 686, 'downhill2'),
        (8576, 174, 'clean_wall'),
        (9088, 686, 'downhill3'),
        (9088, 174, 'clean_wall'),
        (9600, 686, 'plane1'),
        (9600, 174, 'clean_wall'),
        (10112, 686, 'loop'),
        (10112, 174, 'clean_wall'),
        (10624, 686, 'uphill2'),
        (11136, 1198, 'clean_wall'),
        (11136, 174, 'clean_wall'),
        (11136, 686, 'plane4'),
        (11136, 174, 'clean_wall'),
        (11648, 942, 'clean_wall'),
        (11648, 1454, 'clean_wall'),
        (11648, 430, 'wall1'),
        (11648, -82, 'clean_wall'),
        (12160, 1454, 'clean_wall'),
        (12160, 942, 'clean_wall'),
        (12160, 430, 'plane4'),
        (12160, -82, 'clean_wall'),
        (12672, 1224, 'clean_wall'),
        (12672, 712, 'clean_wall'),
        (12672, 200, 'wall1'),
        (13184, 200, 'downhill3'),
        (13696, 200, 'curve1'),
        (14208, 712, 'clean_wall'),
        (14208, 200, 'plane5'),
        (14720, 712, 'clean_wall'),
        (14720, 200, 'plane6'),
        (15232, 712, 'clean_wall'),
        (15232, 200, 'plane7'),
        (15744, 712, 'clean_wall'),
        (15744, 200, 'plane8'),
        (16256, 712, 'clean_wall'),
        (16256, 200, 'stair2'),
        (16768, 712, 'clean_wall'),
        (16768, 200, 'plane4'),
        (17280, 200, 'downhill3'),
        (17792, 200, 'plane1'),
        (18304, 200, 'plane1'),
        (18816, 200, 'plane1'),
        (19328, 200, 'plane1'),
        (18600, 200, 'boss_platform'),
        (19250, 200, 'boss_platform')
    ]
    for x, y, terrain_type in ground_positions:
        ground = Ground(terrain_type)
        ground.x = x
        ground.y = y
        game_world.add_object(ground, 1)
    sonic = Sonic(None)
    sonic.ground = ground

    ring_positions = [
        (640, 250),
        (695, 250),
        (750, 250),
        (1155, 500),
        (1210, 500),
        (1265, 500),
        (1320, 500),
        (1375, 500),
        (1638, 500),
        (2210, 420),
        (2265, 420),
        (2320, 420),
        (2375, 420),
        (2430, 420),
        (3330, 180),
        (3385, 160),
        (3440, 140),
        (3495, 120),
        (3560, 110),
        (3630, 105),
        (3700, 125),
        (3755, 165),
        (4911, 650),
        (4965, 650),
        (5020, 650),
        (5075, 650),
        (6440, 590),
        (6505, 615),
        (6570, 645),
        (6635, 675),
        (6700, 705),
        (7125, 950),
        (7180, 950),
        (7235, 950),
        (7290, 950),
        (8500, 830),
        (8565, 810),
        (8630, 780),
        (8695, 750),
        (8760, 730),
        (9985, 750),
        (10110, 750),
        (10235, 750),
        (12045, 475),
        (12100, 475),
        (12155, 475),
        (12210, 475),
        (12265, 475),
        (15175, 250),
        (15225, 250),
        (15275, 250),
        (15325, 250),
        (15375, 250),
        (15425, 250),
        (17150, 230),
        (17220, 215),
        (17290, 180),
        (17360, 145),
        (17430, 110),
        (17510, 100),
        (17580, 100),
        (17650, 100),
        (17720, 100),
        (17790, 100)
    ]

    rings = [Ring(x, y, sonic) for x, y in ring_positions]
    game_world.add_objects(rings, 3)

    # game_world에 객체 추가
    game_world.add_object(background, 0)
    # game_world.add_object(ground, 1)
    game_world.add_object(sonic, 2)
    game_world.add_objects(crabmeat, 2)
    game_world.add_objects(caterkiller, 2)
    game_world.add_objects(burrobot, 2)
    game_world.add_objects(buzzbomber, 2)
    game_world.add_objects(newtron, 2)
    game_world.add_objects(batbrain, 2)
    # game_world.add_object(boss, 2)
    # game_world.add_object(metal_ball, 2)

    # 충돌 체크 그룹
    for enemy in crabmeat:
        game_world.add_collision_pair(sonic, enemy, 'sonic:crabmeat')

    for enemy in caterkiller:
        game_world.add_collision_pair(sonic, enemy, 'sonic:caterkiller')

    for enemy in burrobot:
        game_world.add_collision_pair(sonic, enemy, 'sonic:burrobot')

    for enemy in buzzbomber:
        game_world.add_collision_pair(sonic, enemy, 'sonic:buzzbomber')

    for enemy in newtron:
        game_world.add_collision_pair(sonic, enemy, 'sonic:newtron')

    for enemy in batbrain:
        game_world.add_collision_pair(sonic, enemy, 'sonic:batbrain')

    # game_world.add_collision_pair(sonic, boss, 'sonic:eggman')
    #
    # game_world.add_collision_pair(sonic, metal_ball, 'sonic:metal_ball')
    for obj in game_world.objects[1]:  # 지형 레이어
        game_world.add_collision_pair(sonic, obj, 'sonic:ground')

    # 배경음악
    bgm = load_music('sound/green_hill_zone_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

    jump_sound = load_wav('sound/jump.mp3')
    jump_sound.set_volume(64)

def finish():
    global lives, score, is_game_over, is_game_clear, boss_spawned
    temp_lives = lives
    temp_score = score
    game_world.clear()
    lives = temp_lives
    score = temp_score
    is_game_over = False
    is_game_clear = False
    boss_spawned = False

def update():
    global camera_x, camera_y, time_elapsed, is_game_over, is_game_clear, is_camera_locked, boss_spawned

    if is_game_over or is_game_clear:
        return

    time_elapsed += game_framework.frame_time

    boss_zone_start = 18925
    boss_spawn_x = 19000

    if not boss_spawned and sonic.x >= boss_spawn_x:
        boss = Eggman(sonic, 18900, 400, 250)
        metal_ball = MetalBall(sonic, boss)
        boss.metal_ball = metal_ball

        game_world.add_object(boss, 2)
        game_world.add_object(metal_ball, 2)
        game_world.add_collision_pair(sonic, boss, 'sonic:eggman')
        game_world.add_collision_pair(sonic, metal_ball, 'sonic:metal_ball')

        boss_spawned = True

    if sonic.x >= boss_zone_start:
        is_camera_locked = True

    if is_camera_locked:
        camera_x = boss_zone_start - 400
        camera_y = max(0, min(camera_y, background.map_height))
    else:
        camera_x = sonic.x - 400
        camera_y = sonic.y - 300

        max_camera_x = background.map_width - 800
        max_camera_y = background.map_height
        camera_x = max(0, min(camera_x, max_camera_x))
        camera_y = max(0, min(camera_y, max_camera_y))

    game_world.handle_collisions()

    game_world.update()

def draw():
    clear_canvas()
    background.draw(camera_x, camera_y)
    game_world.render(camera_x, camera_y)

    if is_game_over:
        draw_game_over()

    if is_game_clear:
        draw_game_clear()

    draw_ui()

    update_canvas()

def draw_game_over():
    global font, font2
    font2.draw(200, 300, "GAME OVER", (255, 0, 0))
    font.draw(200, 250, "PRESS R TO RETURN TO TITLE", (255, 255, 0))

def draw_game_clear():
    global font, font2, score, rings_collected

    time_bonus, ring_bonus = calculate_score()

    final_score = score + time_bonus + ring_bonus

    font2.draw(200, 300, 'GAME CLEAR!', (255, 255, 0))
    font.draw(200, 250, f'Final Score: {final_score}', (255, 255, 255))
    font.draw(200, 200, f'Time Bonus: {time_bonus}', (255, 255, 255))
    font.draw(200, 150, f'Ring Bonus: {ring_bonus}', (255, 255, 255))

def draw_ui():
    global font, score, time_elapsed, rings_collected, life_display

    life_display.draw()

    minutes = int(time_elapsed // 60)
    seconds = int(time_elapsed % 60)
    time_display = f"{minutes}:{seconds:02}"

    font.draw(20, 570, f"SCORE: {score}", (255, 255, 0))            # 점수
    font.draw(20, 540, f"TIME: {time_display}", (255, 255, 0))      # 경과 시간
    font.draw(20, 510, f"RINGS: {rings_collected}", (255, 255, 0))  # 링 개수

def calculate_score():
    global rings_collected, time_elapsed

    time_bonus = max(0, (600 - int(time_elapsed)) * 10)
    ring_bonus = rings_collected * 10

    return time_bonus, ring_bonus

def pause():
    pass

def resume():
    pass

class LifeDisplay:
    def __init__(self, lives):
        self.lives = lives
        self.image = load_image('sprites/life.png')
        self.icon_width = 48
        self.icon_height = 16
        self.number_width = 7
        self.number_height = 7
        self.x = 75
        self.y = 50

    def draw(self):
        num = 0
        if self.lives == 3:
            num = 24
        elif self.lives == 2:
            num = 15
        elif self.lives == 1:
            num = 8
        elif self.lives == 0:
            num = 0
        self.image.clip_draw(0, 9, self.icon_width, self.icon_height, self.x, self.y, 96, 32)
        self.image.clip_draw(num, 0, self.number_width, self.number_height, 100, 40, 14, 14)