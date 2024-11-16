from pico2d import load_image, draw_rectangle
import game_framework

TIME_PER_ROTATE = 0.5
ROTATE_PER_TIME = 1.0 / TIME_PER_ROTATE
FRAMES_PER_ROTATE = 4

class Ring:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('ring.png')
        self.frame = 0

    def draw(self, camera_x):
        self.image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.x - camera_x, self.y, 50, 50)
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ROTATE * ROTATE_PER_TIME * game_framework.frame_time) % 4

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25