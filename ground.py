from pico2d import load_image


class Ground:
    def __init__(self):
        self.image = load_image('green_hill_ground.png')

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.h, 400, 30, 800, 90)

    def update(self):
        pass
