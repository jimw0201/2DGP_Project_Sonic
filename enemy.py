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

class Crabmeat:
    images = None

    def __init__(self, sonic):
        self.x, self.y = random.randint(500, 1600), 120
        self.image = load_image('enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CRABMEAT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_CRABMEAT
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x <= 50 or self.x >= 19150:
            self.dir *= -1

        if random.random() < 0.01:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:crabmeat' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 44, 951, 44, 31, self.x - camera_x, self.y, 88, 62)
        else:
            self.image.clip_composite_draw(int(self.frame) * 44, 951, 44, 31, 0, 'h', self.x - camera_x, self.y, 88, 62)

        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 88 // 2
        height = 62 // 2
        return self.x - width, self.y - height, self.x + width, self.y + height
    
class Caterkiller:
    images = None

    def __init__(self, sonic):
        self.x, self.y = random.randint(2700, 3800), 120
        self.image = load_image('enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CRABMEAT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_CATERKILLER
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x <= 50 or self.x >= 19150:
            self.dir *= -1

        if random.random() < 0.01:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:caterkiller' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 51, 1102, 51, 33, self.x - camera_x, self.y, 102, 66)
        else:
            self.image.clip_draw(int(self.frame) * 51, 1070, 51, 33, self.x - camera_x, self.y, 102, 66)
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 102 // 2
        height = 66 // 2
        return self.x - width, self.y - height, self.x + width, self.y + height

class Burrobot:
    images = None

    def __init__(self, sonic):
        self.x, self.y = random.randint(1700, 2600), 120
        self.image = load_image('enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CRABMEAT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_BURROBOT
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x <= 50 or self.x >= 19150:
            self.dir *= -1

        if random.random() < 0.01:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:burrobot' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 28, 1329, 28, 35, self.x - camera_x, self.y, 56, 70)
        else:
            self.image.clip_draw(int(self.frame) * 28, 1288, 28, 35, self.x - camera_x, self.y, 56, 70)
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 56 // 2
        height = 70 // 2
        return self.x - width, self.y - height, self.x + width, self.y + height

class BuzzBomber:
    images = None

    def __init__(self, sonic):
        self.x, self.y = random.randint(1700, 2600), 250
        self.image = load_image('enemies_sprite_nbg.png')
        self.frame = 0
        self.dir = random.choice([-1, 1])
        self.sonic = sonic
        self.attack_sound = pygame.mixer.Sound('attack.mp3')
        self.attack_sound.set_volume(0.5)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_CRABMEAT * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_BUZZBOMBER
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x <= 50 or self.x >= 19150:
            self.dir *= -1

        if random.random() < 0.01:
            self.dir *= -1

    def handle_collision(self, group, other):
        if group == 'sonic:buzzbomber' and other.is_jumping:
            self.attack_sound.play()
            game_world.remove_object(self)
            play_mode.score += 100

    def draw(self, camera_x):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 37, 1172, 37, 35, self.x - camera_x, self.y, 74, 70)
        else:
            self.image.clip_draw(int(self.frame) * 37, 1135, 37, 35, self.x - camera_x, self.y, 74, 70)
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def get_bb(self):
        width = 74 // 2
        height = 70 // 2
        return self.x - width, self.y - height, self.x + width, self.y + height