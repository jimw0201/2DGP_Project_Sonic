from pico2d import load_image

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

        sonic.dir = 0 # 정지 상태이다.
        sonic.frame = 0
        sonic.frame_direction = 1
        pass

    @staticmethod
    def exit(sonic, e):
        pass

    @staticmethod
    def do(sonic):
        if sonic.frame == 4:
            sonic.frame_direction = -1  # 프레임 감소로 방향 전환
        elif sonic.frame == 0:
            sonic.frame_direction = 1  # 프레임 증가로 방향 전환

        sonic.frame += sonic.frame_direction
        pass

    @staticmethod
    def draw(sonic, x, y):
        sonic.image.clip_draw(74 + 30 * sonic.frame, 1030, 29, 38, x, y)
        pass

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

        if sonic.speed > 100:  # 속도 100 넘으면 달리는 모션
            sonic.fast_frame = (sonic.fast_frame + 1) % 4
        if sonic.speed > 180:  # 속도 180 넘으면 더 빨리 달리는 모션
            sonic.super_fast_frame = (sonic.super_fast_frame + 1) % 4
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
        self.image = load_image('sonic_sprite_nbg.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle) # 초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT',event)
        )

    def draw(self, camera_x):
        self.state_machine.draw(self.x - camera_x, self.y)