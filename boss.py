# boss.py

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

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x
        self.image = load_image('sprites/eggman_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack_eggman.wav')
        self.attack_sound.set_volume(0.5)
        self.is_invincible = False
        self.invincible_time = 0
        self.max_invincible_duration = 2.0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_EGGMAN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_EGGMAN
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time

        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

        if self.is_invincible:
            self.invincible_time += game_framework.frame_time
            if self.invincible_time >= self.max_invincible_duration:
                self.is_invincible = False
                self.invincible_time = 0

    def handle_collision(self, group, other):
        if group == 'sonic:eggman' and other.is_jumping and not self.is_invincible:
            self.attack_sound.play()
            self.is_invincible = True

    def draw(self, camera_x, camera_y):
        if not self.is_invincible or int(self.invincible_time * 10) % 2 == 0:  # 깜빡임 효과
            if self.dir == 1:
                self.image.clip_composite_draw(int(self.frame) * 77, 374, 77, 53, 0, 'h', self.x - camera_x,
                                               self.y - camera_y, 154, 108)
            else:
                self.image.clip_draw(int(self.frame) * 77, 374, 77, 53, self.x - camera_x, self.y - camera_y, 154, 108)

    def get_bb(self):
        width = 154 // 2
        height = 108 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]

class MetalBall:
    images = None

    def __init__(self, sonic, eggman):
        self.image = load_image('sprites/eggman_sprite_nbg.png')
        self.dir = eggman.dir
        self.sonic = sonic
        self.eggman = eggman
        self.ball_x = 0
        self.ball_y = 0
        self.swing_angle = 0
        self.swing_direction = 1
        self.attack_sound = pygame.mixer.Sound('sound/attack_eggman.wav')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.dir = self.eggman.dir
        if self.dir == 1:
            self.ball_x = self.eggman.x + 25
        else:
            self.ball_x = self.eggman.x - 20
        self.ball_y = self.eggman.y - 165

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
        if group == 'sonic:metal_ball':
            self.attack_sound.play()

    def draw(self, camera_x, camera_y):
        # 쇠구슬
        ball_sprite_x, ball_sprite_y, ball_sprite_width, ball_sprite_height = 0, 0, 48, 232
        self.image.clip_composite_draw(
            ball_sprite_x, ball_sprite_y, ball_sprite_width, ball_sprite_height, math.radians(self.swing_angle), '',
            self.ball_x - camera_x, self.ball_y - camera_y + 116,
            ball_sprite_width * 2, ball_sprite_height * 2
        )

    def get_bb(self):
        angle_rad = math.radians(self.swing_angle)
        offset_x = self.ball_x - self.eggman.x
        offset_y = self.ball_y - self.eggman.y

        rotated_x = offset_x * math.cos(angle_rad) - offset_y * math.sin(angle_rad)
        rotated_y = offset_x * math.sin(angle_rad) + offset_y * math.cos(angle_rad)

        new_ball_x = self.eggman.x + rotated_x
        new_ball_y = self.eggman.y + rotated_y - 68

        return [(new_ball_x - 48, new_ball_y - 48, new_ball_x + 48, new_ball_y + 48)]
