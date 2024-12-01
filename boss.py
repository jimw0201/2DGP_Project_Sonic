import math
import random

import pygame
from pico2d import load_image, draw_rectangle

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

FRAMES_PER_ACTION_EGGMAN = 8

class Eggman:
    images = None

    def __init__(self, sonic):
        # 잡몹은 랜덤 위치 생성인데 에그맨은 보스라 스테이지 끝 도달 시 생성되게 해야함. 일단 임시로 랜덤 생성
        self.x, self.y = random.randint(200, 1000), 400
        self.image = load_image('eggman_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('attack_eggman.wav')
        self.attack_sound.set_volume(0.5)

        self.swing_angle = 0
        self.swing_direction = 1

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_EGGMAN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_EGGMAN
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time

        if random.random() < 0.01:
            self.dir *= -1
        if self.x <= 50 or self.x >= 19150:
            self.dir *= -1

        if self.dir == 1:
            self.ball_x = self.x + 25
        else:
            self.ball_x = self.x - 20
        self.ball_y = self.y - 165

        swing_speed = 45
        delta_angle = swing_speed * game_framework.frame_time
        self.swing_angle += self.swing_direction * delta_angle

        if self.swing_angle >= 60:
            self.swing_angle = 60
            self.swing_direction = -1
        elif self.swing_angle <= -60:
            self.swing_angle = -60
            self.swing_direction = 1

    def handle_collision(self, group, other):
        if group == 'sonic:eggman' and other.is_jumping:
            self.attack_sound.play()

        elif group == 'sonic:eggman_ball':
            self.attack_sound.play()

    def draw(self, camera_x):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 77, 374, 77, 53, 0, 'h', self.x - camera_x, self.y, 154, 108)
        else:
            self.image.clip_draw(int(self.frame) * 77, 374, 77, 53, self.x - camera_x, self.y, 154, 108)

        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

        # 쇠구슬
        ball_sprite_x, ball_sprite_y, ball_sprite_width, ball_sprite_height = 0, 0, 48, 232
        self.image.clip_composite_draw(
            ball_sprite_x, ball_sprite_y, ball_sprite_width, ball_sprite_height, math.radians(self.swing_angle), '',
            self.ball_x - camera_x, self.ball_y + 116,
            ball_sprite_width * 2, ball_sprite_height * 2
        )
        left, bottom, right, top = self.get_ball_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 154 // 2
        height = 108 // 2
        return self.x - width, self.y - height, self.x + width, self.y + height

    def get_ball_bb(self):
        angle_rad = math.radians(self.swing_angle)
        offset_x = self.ball_x - self.x
        offset_y = self.ball_y - self.y

        rotated_x = offset_x * math.cos(angle_rad) - offset_y * math.sin(angle_rad)
        rotated_y = offset_x * math.sin(angle_rad) + offset_y * math.cos(angle_rad)

        new_ball_x = self.x + rotated_x
        new_ball_y = self.y + rotated_y - 68

        return new_ball_x - 48, new_ball_y - 48, new_ball_x + 48, new_ball_y + 48