from pico2d import load_image, draw_rectangle, load_wav
import game_framework
import game_world
import play_mode

TIME_PER_ROTATE = 0.5
ROTATE_PER_TIME = 1.0 / TIME_PER_ROTATE
FRAMES_PER_ROTATE = 4

class Ring:
    def __init__(self, x, y, sonic):
        self.x = x
        self.y = y
        self.image = load_image('ring.png')
        self.frame = 0
        self.sonic = sonic

        self.collect_sound = load_wav('ring_collect.mp3')
        self.collect_sound.set_volume(64)

    def draw(self, camera_x):
        self.image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.x - camera_x, self.y, 50, 50)
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ROTATE * ROTATE_PER_TIME * game_framework.frame_time) % 4

        if game_world.collide(self.sonic, self):
            play_mode.rings_collected += 1
            self.collect_sound.play()
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25