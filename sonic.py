from pico2d import load_image, get_time

from state_machine import StateMachine, time_out, space_down, right_down, left_up, left_down, right_up, start_event

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
        # 현재 시간을 저장
        sonic.start_time = get_time()
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
        if get_time() - sonic.start_time > 3:
            sonic.state_machine.add_event(('TIME_OUT',0))
        pass

    @staticmethod
    def draw(sonic):
        sonic.image.clip_draw(74 + 30 * sonic.frame, 1030, 29, 38, sonic.x, sonic.y)
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

    @staticmethod
    def exit(sonic, e):
        pass

    @staticmethod
    def do(sonic):
        sonic.x += sonic.dir * 30
        sonic.frame = (sonic.frame + 1) % 8
        pass

    @staticmethod
    def draw(sonic):
        if sonic.dir == 1:
            sonic.image.clip_draw(203 + 35 * sonic.frame, 909, 30, 40, sonic.x, sonic.y)
        elif sonic.dir == -1:
            sonic.image.clip_composite_draw(203 + 35 * sonic.frame, 909, 30, 40, 0, 'h', sonic.x, sonic.y, 30, 40)
        pass

class Sonic:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
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

    def draw(self):
        self.state_machine.draw()