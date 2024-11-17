import random
import game_framework

from pico2d import *

import game_world
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_CRABMEAT = 3

class Crabmeat:
    images = None

    def __init__(self, sonic):
        self.x, self.y = random.randint(500, 1600), 120
        self.image = load_image('enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CRABMEAT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_CRABMEAT
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x <= 50 or self.x >= 19150:
            self.dir *= -1

        if random.random() < 0.01:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:crabmeat' and other.is_jumping:
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 55, 947, 50, 40, self.x - camera_x, self.y, 88, 80)
        else:
            self.image.clip_composite_draw(int(self.frame) * 55, 947, 50, 40, 0, 'h', self.x - camera_x, self.y, 88, 80)

        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 88 // 2
        height = 80 // 2
        return self.x - width, self.y - height, self.x + width, self.y + height