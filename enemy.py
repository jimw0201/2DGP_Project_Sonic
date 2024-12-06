# enemy.py

import random
import game_framework

from pico2d import *

import game_world
import play_mode
import pygame

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_CRABMEAT = 3
FRAMES_PER_ACTION_CATERKILLER = 7
FRAMES_PER_ACTION_BURROBOT = 2
FRAMES_PER_ACTION_BUZZBOMBER = 2
FRAMES_PER_ACTION_NEWTRON = 2
FRAMES_PER_ACTION_BATBRAIN = 3

class Crabmeat:
    images = None

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x  # 시작 위치 저장
        self.image = load_image('sprites/enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CRABMEAT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_CRABMEAT
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:crabmeat' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x, camera_y):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 44, 951, 44, 31, self.x - camera_x, self.y - camera_y, 88, 62)
        else:
            self.image.clip_composite_draw(int(self.frame) * 44, 951, 44, 31, 0, 'h', self.x - camera_x, self.y - camera_y, 88, 62)

        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 88 // 2
        height = 62 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]

class Caterkiller:
    images = None

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x
        self.image = load_image('sprites/enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CATERKILLER * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_CATERKILLER
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:caterkiller' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x, camera_y):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 51, 1102, 51, 33, self.x - camera_x, self.y - camera_y, 102, 66)
        else:
            self.image.clip_draw(int(self.frame) * 51, 1070, 51, 33, self.x - camera_x, self.y - camera_y, 102, 66)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 102 // 2
        height = 66 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]

class Burrobot:
    images = None

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x
        self.image = load_image('sprites/enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_BURROBOT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_BURROBOT
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:burrobot' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x, camera_y):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 28, 1329, 28, 35, self.x - camera_x, self.y - camera_y, 56, 70)
        else:
            self.image.clip_draw(int(self.frame) * 28, 1288, 28, 35, self.x - camera_x, self.y - camera_y, 56, 70)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 56 // 2
        height = 70 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]

class BuzzBomber:
    images = None

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x
        self.image = load_image('sprites/enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_BUZZBOMBER * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_BUZZBOMBER
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:buzzbomber' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x, camera_y):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 37, 1172, 37, 35, self.x - camera_x, self.y - camera_y, 74, 70)
        else:
            self.image.clip_draw(int(self.frame) * 37, 1135, 37, 35, self.x - camera_x, self.y - camera_y, 74, 70)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 74 // 2
        height = 70 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]

class Newtron:
    images = None

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x
        self.image = load_image('sprites/enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_NEWTRON * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_NEWTRON
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:newtron' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x, camera_y):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 39, 683, 39, 39, self.x - camera_x, self.y - camera_y, 78, 78)
        else:
            self.image.clip_draw(int(self.frame) * 39, 638, 39, 39, self.x - camera_x, self.y - camera_y, 78, 78)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 78 // 2
        height = 78 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]

class Batbrain:
    images = None

    def __init__(self, sonic, x, y, move_range=100):
        self.x, self.y = x, y
        self.move_range = move_range
        self.initial_x = x
        self.image = load_image('sprites/enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('sound/attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_BATBRAIN * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_BATBRAIN
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if abs(self.x - self.initial_x) > self.move_range:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:batbrain' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x, camera_y):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 35, 30, 35, 38, self.x - camera_x, self.y - camera_y, 70, 76)
        else:
            self.image.clip_composite_draw(int(self.frame) * 35, 30, 35, 38, 0, 'h', self.x - camera_x, self.y - camera_y, 70, 76)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 70 // 2
        height = 76 // 2
        return [(self.x - width, self.y - height, self.x + width, self.y + height)]