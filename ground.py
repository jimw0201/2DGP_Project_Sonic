# ground.py
from pico2d import load_image, draw_rectangle



# 지형 클래스
class Ground:
    # 지형 이미지
    TERRAIN_IMAGES = {
        'tree': 'tilemaps/1.png',
        'platform': 'tilemaps/3.png',
        'plane1': 'tilemaps/45.png',
        'plane2': 'tilemaps/16.png',
        'uphill1': 'tilemaps/49.png',
        'downhill1': 'tilemaps/2.png',
        'bridge': 'tilemaps/51.png',
        'curve1': 'tilemaps/7.png',
        'stair1': 'tilemaps/4.png',
        'stair2': 'tilemaps/5.png',
        'start_of_bridge': 'tilemaps/43.png',
        'plane3': 'tilemaps/14.png',
        'twin': 'tilemaps/20.png',
        'downhill2': 'tilemaps/35.png',
        'downhill3': 'tilemaps/37.png',
        'loop': 'tilemaps/53.png',
        'uphill2': 'tilemaps/38.png',
        'plane4': 'tilemaps/17.png',
        'wall1': 'tilemaps/30.png',
        'plane5': 'tilemaps/34.png',
        'plane6': 'tilemaps/12.png',
        'plane7': 'tilemaps/13.png',
        'plane8': 'tilemaps/21.png',
        'stair3': 'tilemaps/25.png',
    }

    # 지형 너비
    TERRAIN_WIDTHS = {
        'tree': 512,
        'platform': 512,
        'plane1': 512,
        'plane2': 512,
        'uphill1': 512,
        'downhill1': 512,
        'bridge': 512,
        'curve1': 512,
        'stair1': 512,
        'stair2': 512,
        'start_of_bridge': 512,
        'plane3': 512,
        'twin': 512,
        'downhill2': 512,
        'downhill3': 512,
        'loop': 512,
        'uphill2': 512,
        'plane4': 512,
        'wall1': 512,
        'plane5': 512,
        'plane6': 512,
        'plane7': 512,
        'plane8': 512,
        'stair3': 512,

    }

    # 지형 높이
    TERRAIN_HEIGHTS = {
        'tree': 512,
        'platform': 512,
        'stair': 512,
        'plane1': 512,
        'plane2': 512,
        'uphill1': 512,
        'downhill1': 512,
        'bridge': 512,
        'curve1': 512,
        'start_of_bridge': 512,
        'plane3': 512,
        'twin': 512,
        'downhill2': 512,
        'downhill3': 512,
        'loop': 512,
        'uphill2': 512,
        'plane4': 512,
        'wall1': 512,
        'plane5': 512,
        'plane6': 512,
        'plane7': 512,
        'plane8': 512,
        'stair3': 512,
    }
    def __init__(self, terrain_type='tree'):
        if terrain_type not in Ground.TERRAIN_IMAGES:
            raise ValueError(f"Unsupported terrain type: {terrain_type}")
        self.terrain_type = terrain_type  # 지형 타입 저장
        self.image = load_image(Ground.TERRAIN_IMAGES[terrain_type])
        # self.image = load_image('green_hill_ground.png')
        self.width = Ground.TERRAIN_WIDTHS.get(terrain_type, 512)
        self.height = Ground.TERRAIN_HEIGHTS.get(terrain_type, 512)
        self.x = 0
        self.y = 0

    def get_height(self):
        return self.height

    def draw(self, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        self.image.draw(screen_x, screen_y, self.width, self.height)

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
        self.map_width = 19328 # 전체 맵 너비
        self.map_height = 2000
        self.screen_width = 800  # 화면 너비

    def draw(self, camera_x, camera_y):
        start_x = -camera_x % self.screen_width
        start_y = -camera_y % 600
        tile_count_x = int(self.map_width / self.screen_width) + 2
        tile_count_y = 2 # 일단 임시로 뒷배경 설정

        for i in range(-1, tile_count_x):
            for j in range(-1, tile_count_y):
                self.image.draw(start_x + i * self.screen_width, start_y + j * 600, self.screen_width, 600)

    def update(self):
        pass