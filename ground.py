# ground.py
from pico2d import load_image, draw_rectangle



# 지형 클래스
class Ground:
    # 지형 이미지
    TERRAIN_IMAGES = {
        'tree': 'tilemaps/1.png',
        'platform': 'tilemaps/3.png',
        'stair': 'tilemaps/4.png',
        'plane1': 'tilemaps/45.png',
        'plane2': 'tilemaps/16.png',
        'uphill': 'tilemaps/49.png',
        'downhill': 'tilemaps/2.png',
        'bridge': 'tilemaps/51.png',
    }

    # 지형 너비
    TERRAIN_WIDTHS = {
        'tree': 512,
        'platform': 512,
        'stair': 512,
        'plane1': 512,
        'plane2': 512,
        'uphill': 512,
        'downhill': 512,
        'bridge': 512,
    }

    # 지형 높이
    TERRAIN_HEIGHTS = {
        'tree': 512,
        'platform': 512,
        'stair': 512,
        'plane1': 512,
        'plane2': 512,
        'uphill': 512,
        'downhill': 512,
        'bridge': 512,
    }
    def __init__(self, terrain_type='tree'):
        if terrain_type not in Ground.TERRAIN_IMAGES:
            raise ValueError(f"Unsupported terrain type: {terrain_type}")
        self.terrain_type = terrain_type  # 지형 타입 저장
        self.image = load_image(Ground.TERRAIN_IMAGES[terrain_type])
        # self.image = load_image('green_hill_ground.png')
        self.width = Ground.TERRAIN_WIDTHS.get(terrain_type, 256)
        self.height = Ground.TERRAIN_HEIGHTS.get(terrain_type, 256)
        self.x = 0
        self.y = 0

    def get_height(self):
        return self.height

    def draw(self, camera_x):
        screen_x = self.x - camera_x
        self.image.draw(screen_x, self.y, self.width, self.height)

        # left, bottom, right, top = self.get_bb()
        # draw_rectangle(left - camera_x, bottom, right - camera_x, top)

    def update(self):
        pass

    def get_bb(self):
        # 지형 타입에 따라 충돌 박스 설정
        if self.terrain_type == 'tree':
            return (self.x - self.width // 2,
                    self.y - self.height // 2,
                    self.x + self.width // 2,
                    self.y + self.height // 2)

# 뒷배경 클래스
class Background:
    def __init__(self):
        self.image = load_image('background.jpg')
        self.map_width = 19200  # 전체 맵 너비
        self.screen_width = 800  # 화면 너비

    def draw(self, camera_x):
        start_x = -camera_x % self.screen_width
        tile_count = int(self.map_width / self.screen_width) + 2
        for i in range(-1, tile_count):
            self.image.draw(start_x + i * self.screen_width, 300, self.screen_width, 600)

    def update(self):
        pass