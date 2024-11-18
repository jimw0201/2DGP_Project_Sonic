from pico2d import load_image

# 지형 클래스
class Ground:
    def __init__(self):
        self.image = load_image('green_hill_ground.png')
        self.width = self.image.w
        self.map_width = 1600
        self.height = 90

    def get_height(self):
        return self.height

    def draw(self, camera_x):
        start_x = -camera_x % self.width
        tile_count = int(self.map_width / self.width) + 2
        for i in range(-1, tile_count):
            self.image.draw(start_x + i * self.width, 45, self.width, 90)

    def update(self):
        pass

# 뒷배경 클래스
class Background:
    def __init__(self):
        self.image = load_image('background.jpg')
        self.map_width = 5000  # 전체 맵 너비
        self.screen_width = 800  # 화면 너비

    def draw(self, camera_x):
        start_x = -camera_x % self.screen_width
        tile_count = int(self.map_width / self.screen_width) + 2
        for i in range(-1, tile_count):
            self.image.draw(start_x + i * self.screen_width, 300, self.screen_width, 600)

    def update(self):
        pass