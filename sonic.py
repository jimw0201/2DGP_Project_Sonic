from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP

from state_machine import StateMachine, space_down, right_down, left_up, left_down, right_up, start_event

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

    @staticmethod
    def exit(sonic, e):
        pass

    @staticmethod
    def do(sonic):
        sonic.frame_counter += 1
        if sonic.frame_counter >= 10:
            sonic.frame_counter = 0

            if sonic.frame == 4:
                sonic.frame_direction = -1  # 프레임 감소로 방향 전환
            elif sonic.frame == 0:
                sonic.frame_direction = 1  # 프레임 증가로 방향 전환

            sonic.frame += sonic.frame_direction

    @staticmethod
    def draw(sonic, x, y):
        sonic.image.clip_draw(74 + 30 * sonic.frame, 1030, 29, 38, x, y)

class Run:
    @staticmethod
    def enter(sonic, e):
        if right_down(e) or left_up(e):
            sonic.dir = 1 # 오른쪽 방향
            sonic.action = 1
        elif left_down(e) or right_up(e):
            sonic.dir = -1
            sonic.action = 0

        sonic.frame = 0
        sonic.fast_frame = 0
        sonic.super_fast_frame = 0
        sonic.speed = 0

    @staticmethod
    def exit(sonic, e):
        pass

    @staticmethod
    def do(sonic):
        if sonic.dir != 0:
            if sonic.speed < sonic.max_speed:
                sonic.speed += sonic.acceleration
        else:
            if sonic.speed > 0:
                sonic.speed -= sonic.deceleration
                if sonic.speed < 0:
                    sonic.speed = 0

        sonic.x += sonic.dir * sonic.speed * 0.1

        sonic.frame_counter += 1
        max_frame_count = 10 - int(sonic.speed / 20)  # 속도에 따른 프레임 전환 간격 조절

        if sonic.frame_counter >= max_frame_count:
            sonic.frame_counter = 0
            if sonic.speed > 180:
                sonic.super_fast_frame = (sonic.super_fast_frame + 1) % 4
            elif sonic.speed > 100:
                sonic.fast_frame = (sonic.fast_frame + 1) % 4
            else:
                sonic.frame = (sonic.frame + 1) % 8

    @staticmethod
    def draw(sonic, x, y):
        if sonic.speed > 180:
            if sonic.dir == 1:
                sonic.image.clip_draw(320 + 42 * sonic.super_fast_frame, 735, 41, 35, x, y)
            elif sonic.dir == -1:
                sonic.image.clip_composite_draw(320 + 42 * sonic.super_fast_frame, 735, 41, 35, 0, 'h', x, y, 41, 35)

        elif sonic.speed > 100:
            if sonic.dir == 1:
                sonic.image.clip_draw(10 + 35 * sonic.fast_frame, 735, 35, 36, x, y)
            elif sonic.dir == -1:
                sonic.image.clip_composite_draw(10 + 35 * sonic.fast_frame, 735, 35, 36, 0, 'h', x, y, 35, 36)

        else:
            if sonic.dir == 1:
                sonic.image.clip_draw(203 + 35 * sonic.frame, 909, 30, 40, x, y)
            elif sonic.dir == -1:
                sonic.image.clip_composite_draw(203 + 35 * sonic.frame, 909, 30, 40, 0, 'h', x, y, 30, 40)


class Jump:
    @staticmethod
    def enter(sonic, e):
        sonic.jump_speed = 20  # 초기 점프 속도
        sonic.jump_dir = sonic.dir  # 현재 달리는 방향을 점프 방향으로
        sonic.jump_x_speed = abs(sonic.speed)  # 현재 달리는 속도를 점프할 때 나아가는 속도에 반영
        sonic.is_jumping = True  # 점프 상태
        sonic.jump_start_y = sonic.y  # 점프 시작 위치 저장

    @staticmethod
    def exit(sonic, e):
        sonic.is_jumping = False
        sonic.jump_dir = 0
        sonic.jump_x_speed = 0

    @staticmethod
    def do(sonic):
        # 점프 중 중력 효과 적용
        if sonic.is_jumping:
            sonic.y += sonic.jump_speed
            sonic.jump_speed -= 1
            sonic.x += sonic.jump_dir * sonic.jump_x_speed * 0.1

            if sonic.y <= sonic.jump_start_y:
                sonic.y = sonic.jump_start_y
                sonic.jump_speed = 0
                sonic.is_jumping = False

                if sonic.dir == 0:
                    sonic.state_machine.add_event(('END_JUMP', 0))
                else:
                    sonic.state_machine.add_event(('RUN', 0))

    @staticmethod
    def draw(sonic, x, y):
        sonic.image.clip_draw(203 + 35 * sonic.frame, 909, 30, 40, x, y)

class Sonic:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.speed = 0
        self.max_speed = 200
        self.acceleration = 10
        self.deceleration = 5
        self.frame_counter = 0

        self.image = load_image('sonic_sprite_nbg.png')
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
            if event.key == SDLK_LEFT:
                self.dir = -1
            elif event.key == SDLK_RIGHT:
                self.dir = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                self.dir = 0
        self.state_machine.add_event(('INPUT', event))

    def draw(self, camera_x):
        self.state_machine.draw(self.x - camera_x, self.y)