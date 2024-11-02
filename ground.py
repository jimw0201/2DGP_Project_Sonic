from pico2d import load_image


class Ground:
    def __init__(self):
        self.image = load_image('green_hill_ground.png')
        self.width = self.image.w

    def draw(self, camera_x):
        start_x = -camera_x % self.width

        for i in range(-1, 10):
            self.image.draw(start_x + i * self.width, 45, self.width, 90)

    def update(self):
        pass

class Background:
    def __init__(self):
        self.image = load_image('background.jpg')

    def draw(self, camera_x):
        for i in range(-1, 10):
            self.image.draw(i * 800, 300, 800, 600)

    def update(self):
        pass