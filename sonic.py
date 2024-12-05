# sonic.py

from pico2d import load_image, load_wav, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP

import game_framework
import game_world
import play_mode
import random
import math
from ring import Ring
from state_machine import StateMachine, space_down, right_down, left_up, left_down, right_up, start_event

TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 5
FRAMES_PER_ACTION_RUN_FAST = 4
FRAMES_PER_ACTION_RUN = 8
FRAMES_PER_ACTION_JUMP = 5

class Idle:
    @staticmethod
    def enter(sonic, e):
        if left_up(e) or right_down(e):
            sonic.action = 2
            sonic.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            sonic.action = 3
            sonic.face_dir = 1

        sonic.dir = 0
        sonic.frame = 0
        sonic.frame_direction = 1
        sonic.frame_counter = 0
        sonic.speed = 0

    @staticmethod
    def exit(sonic, e):
        pass

    @staticmethod
    def do(sonic):
        sonic.frame_counter += 1
        if sonic.frame_counter >= 10:
            sonic.frame_counter = 0

            if sonic.frame == 4:
                sonic.frame_direction = -1
            elif sonic.frame == 0:
                sonic.frame_direction = 1

            sonic.frame += sonic.frame_direction * FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time
            sonic.frame = int(sonic.frame)

        # 여러 바운딩 박스에서 소닉의 높이와 가장 가까운 높이를 선택
        ground_heights = []
        for ground in game_world.objects[1]:
            heights = ground.get_height_at_position(sonic.x)
            ground_heights.extend(heights)

        closest_height = min(ground_heights, key=lambda h: abs(h - sonic.y), default=None)

        if closest_height is not None:
            if sonic.y - 40 <= closest_height:
                sonic.y = closest_height + 40
                sonic.fall_speed = 0
            else:
                sonic.fall_speed += sonic.gravity
                sonic.y -= sonic.fall_speed
        else:
            sonic.fall_speed += sonic.gravity
            sonic.y -= sonic.fall_speed

        if sonic.y < 0:
            sonic.y = 0
            sonic.fall_speed = 0

    @staticmethod
    def draw(sonic, x, y):
        if sonic.face_dir == 1:
            sonic.image.clip_draw(74 + 30 * int(sonic.frame), 1030, 29, 38, x, y, 58, 76)
        else:
            sonic.image.clip_composite_draw(74 + 30 * int(sonic.frame), 1030, 29, 38, 0, 'h', x, y, 58, 76)

class Run:
    @staticmethod
    def enter(sonic, e):
        if right_down(e) or left_up(e):
            sonic.dir = 1  # 오른쪽 방향
            sonic.action = 1
        elif left_down(e) or right_up(e):
            sonic.dir = -1
            sonic.action = 0

        sonic.frame = 0
        sonic.fast_frame = 0
        sonic.super_fast_frame = 0

    @staticmethod
    def exit(sonic, e):
        pass

    @staticmethod
    def do(sonic):
        # 여러 바운딩 박스에서 소닉의 높이와 가장 가까운 높이를 선택
        ground_heights = []
        for ground in game_world.objects[1]:
            heights = ground.get_height_at_position(sonic.x)
            ground_heights.extend(heights)

        closest_height = min(ground_heights, key=lambda h: abs(h - sonic.y), default=None)
        if closest_height is not None and sonic.y - 40 <= closest_height:
            sonic.y = closest_height + 40
            sonic.fall_speed = 0
        else:
            sonic.fall_speed += sonic.gravity
            sonic.y -= sonic.fall_speed

            if sonic.y < 0:
                sonic.y = 0
                sonic.fall_speed = 0

        # x 좌표 이동은 y 좌표와 상관없이 처리
        if sonic.dir != 0:
            if closest_height is not None and sonic.y - 40 <= closest_height:
                if sonic.speed < sonic.max_speed:
                    sonic.speed += sonic.acceleration
            else:
                if sonic.speed > 0:
                    sonic.speed -= sonic.acceleration * game_framework.frame_time
                    if sonic.speed < 0:
                        sonic.speed = 0

            sonic.x += sonic.dir * sonic.speed * 0.1

        sonic.frame_counter += 1
        max_frame_count = 10 - int(sonic.speed / 20)  # 속도에 따른 프레임 전환 간격 조절

        if sonic.frame_counter >= max_frame_count:
            sonic.frame_counter = 0
            if sonic.speed > 180:
                sonic.super_fast_frame = (sonic.super_fast_frame + FRAMES_PER_ACTION_RUN_FAST * ACTION_PER_TIME * game_framework.frame_time) % 4
            elif sonic.speed > 100:
                sonic.fast_frame = (sonic.fast_frame + FRAMES_PER_ACTION_RUN_FAST * ACTION_PER_TIME * game_framework.frame_time) % 4
            else:
                sonic.frame = (sonic.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(sonic, x, y):
        if sonic.speed > 180:
            if sonic.dir == 1:
                sonic.image.clip_draw(320 + 42 * int(sonic.super_fast_frame), 735, 41, 35, x, y, 82, 70)
            elif sonic.dir == -1:
                sonic.image.clip_composite_draw(320 + 42 * int(sonic.super_fast_frame), 735, 41, 35, 0, 'h', x, y, 82, 70)

        elif sonic.speed > 100:
            if sonic.dir == 1:
                sonic.image.clip_draw(10 + 35 * int(sonic.fast_frame), 735, 35, 36, x, y, 70, 72)
            elif sonic.dir == -1:
                sonic.image.clip_composite_draw(10 + 35 * int(sonic.fast_frame), 735, 35, 36, 0, 'h', x, y, 70, 72)

        else:
            if sonic.dir == 1:
                sonic.image.clip_draw(203 + 35 * int(sonic.frame), 909, 30, 40, x, y, 60, 80)
            elif sonic.dir == -1:
                sonic.image.clip_composite_draw(203 + 35 * int(sonic.frame), 909, 30, 40, 0, 'h', x, y, 60, 80)


class Jump:
    @staticmethod
    def enter(sonic, e):
        sonic.jump_speed = 20  # 초기 점프 속도
        sonic.jump_dir = sonic.dir  # 현재 달리는 방향을 점프 방향으로
        sonic.jump_x_speed = abs(sonic.speed)  # 현재 달리는 속도를 점프할 때 나아가는 속도에 반영
        sonic.is_jumping = True  # 점프 상태
        sonic.jump_start_y = sonic.y  # 점프 시작 위치 저장
        if sonic.dir != 0:
            sonic.face_dir = sonic.dir

        if hasattr(sonic, 'jump_sound'):
            sonic.jump_sound.play()

    @staticmethod
    def exit(sonic, e):
        sonic.is_jumping = False
        sonic.jump_dir = 0
        sonic.jump_x_speed = 0

    @staticmethod
    def do(sonic):
        sonic.frame = (sonic.frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time) % 5

        if sonic.dir != 0:
            sonic.jump_dir = sonic.dir
            sonic.face_dir = sonic.dir

        # 점프 중 중력 효과 적용
        if sonic.is_jumping:
            sonic.y += sonic.jump_speed
            sonic.jump_speed -= 1
            sonic.x += sonic.jump_dir * sonic.jump_x_speed * 0.1

            # 여러 바운딩 박스에서 소닉의 높이와 가장 가까운 높이를 선택
            ground_heights = []
            for ground in game_world.objects[1]:
                heights = ground.get_height_at_position(sonic.x)
                ground_heights.extend(heights)

            closest_height = min(ground_heights, key=lambda h: abs(h - sonic.y), default=None)

            # 가장 가까운 땅에 착지
            if closest_height is not None and sonic.y - 40 <= closest_height:
                sonic.y = closest_height + 40
                sonic.jump_speed = 0
                sonic.is_jumping = False

                if sonic.dir == 0:
                    sonic.state_machine.add_event(('END_JUMP', 0))
                else:
                    sonic.state_machine.add_event(('RUN', 0))

    @staticmethod
    def draw(sonic, x, y):
        if sonic.face_dir == 1:
            sonic.image.clip_draw(500 + 35 * int(sonic.frame), 971, 34, 34, x, y, 68, 68)
        else:
            sonic.image.clip_composite_draw(500 + 35 * int(sonic.frame), 973, 34, 34, 0, 'h', x, y, 68, 68)

class Sonic:
    def __init__(self, ground):
        self.x, self.y = 50, 110
        self.ground = ground
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.speed = 0
        self.max_speed = 200
        self.acceleration = 1.5
        self.frame_counter = 0
        self.is_jumping = False
        self.gravity = 0.5
        self.fall_speed = 0

        self.keys = {SDLK_LEFT: False, SDLK_RIGHT: False}

        self.jump_sound = load_wav('sound/jump.mp3')
        self.jump_sound.set_volume(64)

        self.ring_loss_sound = load_wav('sound/ring_loss.mp3')
        self.ring_loss_sound.set_volume(64)

        self.image = load_image('sprites/sonic_sprite_nbg.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle) # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Jump},
                Jump: {
                    lambda e: e == ('END_JUMP', 0): Idle,
                    lambda e: e == ('RUN', 0): Run
                }
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
                self.update_dir()

        elif event.type == SDL_KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False
                self.update_dir()

        self.state_machine.add_event(('INPUT', event))

    def update_dir(self):
        # 눌린 방향키 상태에 따라 방향 결정
        if self.keys[SDLK_LEFT] and self.keys[SDLK_RIGHT]:
            self.dir = 0
        elif self.keys[SDLK_LEFT]:
            self.dir = -1
        elif self.keys[SDLK_RIGHT]:
            self.dir = 1
        else:
            self.dir = 0

    def draw(self, camera_x, camera_y):
        self.state_machine.draw(self.x - camera_x, self.y - camera_y)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)
        for bb in self.get_bb():
            left, bottom, right, top = bb
            draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def get_bb(self):
        return [(self.x - 30, self.y - 40, self.x + 30, self.y + 40)]

    def is_on_ground(self):
        ground_heights = []
        for ground in game_world.objects[1]:  # 지형 레이어 탐색
            heights = ground.get_height_at_position(self.x)
            ground_heights.extend(heights)  # 모든 높이를 리스트에 추가

        # 소닉의 높이와 가장 가까운 높이를 선택
        closest_height = min(ground_heights, key=lambda h: abs(h - self.y), default=None)

        if closest_height is not None and self.y - 40 <= closest_height:
            return True
        return False

    def handle_collision(self, group, other):
        if group == 'sonic:ground':
            # 소닉의 바운딩 박스와 지형의 바운딩 박스를 가져옴
            sonic_bb = self.get_bb()[0]
            ground_bb_list = other.get_bb()

            for ground_bb in ground_bb_list:
                if game_world.check_collision(sonic_bb, ground_bb):
                    # 소닉이 지형의 상단에 서 있는 경우
                    if sonic_bb[1] <= ground_bb[3] and sonic_bb[3] > ground_bb[3]:
                        self.y = ground_bb[3] + 40  # 지형 상단에서 위치를 고정
                        self.fall_speed = 0  # 낙하 속도 초기화
                        break

                    # 소닉이 지형의 왼쪽 또는 오른쪽 벽에 부딪힌 경우
                    if sonic_bb[2] > ground_bb[0] and sonic_bb[0] < ground_bb[0] and self.dir > 0:  # 오른쪽 이동 중
                        self.x = ground_bb[0] - 30  # 오른쪽 벽 위치로 고정
                        self.dir = 0
                    elif sonic_bb[0] < ground_bb[2] and sonic_bb[2] > ground_bb[2] and self.dir < 0:  # 왼쪽 이동 중
                        self.x = ground_bb[2] + 30  # 왼쪽 벽 위치로 고정
                        self.dir = 0
                    break

        if group == 'sonic:crabmeat':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

        if group == 'sonic:caterkiller':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

        if group == 'sonic:burrobot':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

        if group == 'sonic:buzzbomber':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

        if group == 'sonic:newtron':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

        if group == 'sonic:batbrain':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

        if group == 'sonic:eggman':
            if self.is_jumping:
                self.jump_speed = 15
                self.is_jumping = True
                self.y += 10
            else:
                self.ring_loss_sound.play()
                self.drop_rings()

    def drop_rings(self):
        drop_count = play_mode.rings_collected
        play_mode.rings_collected = 0

        distance = 200
        for i in range(drop_count):
            angle = i * (180 / drop_count)
            offset_x = distance * math.cos(math.radians(angle))
            offset_y = distance * math.sin(math.radians(angle)) + random.randint(-10, 10)  # 약간의 랜덤성 추가

            speed = 7
            vx = speed * math.cos(math.radians(angle))
            vy = speed * math.sin(math.radians(angle))

            new_ring = Ring(self.x + offset_x, self.y + offset_y, self, is_dropped=True)
            new_ring.vx = vx
            new_ring.vy = vy
            game_world.add_object(new_ring, 3)