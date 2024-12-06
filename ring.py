# ring.py

from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import play_mode
import pygame

TIME_PER_ROTATE = 0.5
ROTATE_PER_TIME = 1.0 / TIME_PER_ROTATE
FRAMES_PER_ROTATE = 4

pygame.mixer.init()

class Ring:
    def __init__(self, x, y, sonic, is_dropped=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.is_dropped = is_dropped
        self.image = load_image('sprites/ring.png')
        self.frame = 0
        self.sonic = sonic
        self.gravity = -0.5

        self.exist_time = 0

        ground_heights = []
        for ground in game_world.objects[1]:
            heights = ground.get_height_at_position(self.x)
            ground_heights.extend(heights)

        if ground_heights:
            self.ground_height = min(ground_heights, key=lambda h: abs(h - self.y)) + 30
        else:
            self.ground_height = 0 + 30

        self.collect_sound = pygame.mixer.Sound('sound/ring_collect.mp3')
        self.collect_sound.set_volume(0.5)

    def draw(self, camera_x, camera_y):
        self.image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.x - camera_x, self.y - camera_y, 40, 40)
        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)
        # for bb in self.get_bb():
        #     left, bottom, right, top = bb
        #     draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ROTATE * ROTATE_PER_TIME * game_framework.frame_time) % 4

        if self.is_dropped:
            self.exist_time += game_framework.frame_time
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity

            if self.y <= self.ground_height:
                self.y = self.ground_height
                self.vx = 0
                self.vy = 0

            if self.exist_time >= 5.0:
                game_world.remove_object(self)

        if game_world.collide(self.sonic, self):
            play_mode.rings_collected += 1
            self.collect_sound.play()
            game_world.remove_object(self)

    def get_bb(self):
        return [(self.x - 20, self.y - 20, self.x + 20, self.y + 20)]