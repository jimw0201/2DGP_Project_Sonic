# ground.py

from pico2d import load_image, draw_rectangle



# 지형 클래스
class Ground:
    # 지형 이미지
    TERRAIN_IMAGES = {
        'platform': 'tilemaps/3.png',
        'plane1': 'tilemaps/45.png',
        'plane2': 'tilemaps/16.png',
        'uphill1': 'tilemaps/49.png',
        'downhill1': 'tilemaps/2.png',
        'bridge': 'tilemaps/51.png',
        'curve1': 'tilemaps/7.png',
        'stair1': 'tilemaps/4.png',
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
        'stair2': 'tilemaps/25.png',
    }

    # 지형 너비
    TERRAIN_WIDTHS = {
        'platform': 512,
        'plane1': 512,
        'plane2': 512,
        'uphill1': 512,
        'downhill1': 512,
        'bridge': 512,
        'curve1': 512,
        'stair1': 512,
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
        'stair2': 512,
    }

    # 지형 높이
    TERRAIN_HEIGHTS = {
        'platform': 512,
        'plane1': 512,
        'plane2': 512,
        'uphill1': 512,
        'downhill1': 512,
        'bridge': 512,
        'curve1': 512,
        'stair1': 512,
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
        'stair2': 512,
    }
    def __init__(self, terrain_type='platform'):
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

    def get_height_at_position(self, x):
        bb = self.get_bb()
        temp = []

        for box in bb:
            left, bottom, right, top = box
            if left <= x <= right:
                temp.append(top)
        return temp

    def draw(self, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        self.image.draw(screen_x, screen_y, self.width, self.height)

        # 바운딩 박스를 화면에 그리기
        for bb in self.get_bb():
            left, bottom, right, top = bb
            draw_rectangle(left - camera_x, bottom - camera_y, right - camera_x, top - camera_y)

    def update(self):
        pass

    def handle_collision(self, group, other):
        pass

    def get_uphill1_bb(self, num_segments=20, height_reduction=50, y_offset=0):
        bounding_boxes = []
        segment_width = self.width / num_segments

        left_bottom = (self.x - self.width / 2, self.y - self.height / 2 + y_offset)
        left_top = (self.x - self.width / 2, self.y - 128 + height_reduction + y_offset)
        right_top = (self.x + self.width / 2, self.y + y_offset)
        right_bottom = (self.x + self.width / 2, self.y + self.height / 2 + y_offset)

        for i in range(num_segments):
            # 각 세그먼트의 x 좌표 범위
            seg_left_x = left_bottom[0] + i * segment_width
            seg_right_x = seg_left_x + segment_width

            # 선형 보간을 통해 각 세그먼트의 y 좌표 계산
            y_low_start = left_bottom[1] + (left_top[1] - left_bottom[1]) * (i / num_segments) * 0.8
            y_low_end = left_bottom[1] + (left_top[1] - left_bottom[1]) * ((i + 1) / num_segments) * 0.8

            y_high_start = right_top[1] + (right_bottom[1] - right_top[1]) * (i / num_segments) * 0.8
            y_high_end = right_top[1] + (right_bottom[1] - right_top[1]) * ((i + 1) / num_segments) * 0.8

            # 각 세그먼트의 하단과 상단 y 좌표를 평균하여 사용
            y_low = (y_low_start + y_low_end) / 2
            y_high = (y_high_start + y_high_end) / 2

            # 바운딩 박스 추가
            bounding_boxes.append((
                seg_left_x,
                y_low,
                seg_right_x,
                y_high
            ))

        return bounding_boxes
    def get_uphill2_bb(self, num_segments=20, height_reduction=50, y_offset=0):
        bounding_boxes = []
        segment_width = self.width / num_segments

        left_bottom = (self.x - self.width / 2, self.y - self.height / 2 + y_offset)
        left_top = (self.x - self.width / 2, self.y - 150 + height_reduction + y_offset)
        right_top = (self.x + self.width / 2, self.y + y_offset)
        right_bottom = (self.x + self.width / 2, self.y + self.height / 2 + y_offset)

        for i in range(num_segments):
            # 각 세그먼트의 x 좌표 범위
            seg_left_x = left_bottom[0] + i * segment_width
            seg_right_x = seg_left_x + segment_width

            # 선형 보간을 통해 각 세그먼트의 y 좌표 계산
            y_low_start = left_bottom[1] + (left_top[1] - left_bottom[1]) * (i / num_segments) * 0.8
            y_low_end = left_bottom[1] + (left_top[1] - left_bottom[1]) * ((i + 1) / num_segments) * 0.8

            y_high_start = right_top[1] + (right_bottom[1] - right_top[1]) * (i / num_segments) * 0.65
            y_high_end = right_top[1] + (right_bottom[1] - right_top[1]) * ((i + 1) / num_segments) * 0.65

            # 각 세그먼트의 하단과 상단 y 좌표를 평균하여 사용
            y_low = (y_low_start + y_low_end) / 2
            y_high = (y_high_start + y_high_end) / 2

            # 바운딩 박스 추가
            bounding_boxes.append((
                seg_left_x,
                y_low,
                seg_right_x,
                y_high
            ))

        return bounding_boxes

    def get_downhill1_bb(self, num_segments=20, height_reduction=50, y_offset=0):
        bounding_boxes = []
        segment_width = self.width / num_segments

        left_bottom = (self.x - self.width / 2, self.y + self.height / 2 + y_offset)
        left_top = (self.x - self.width / 2, self.y + 130 - height_reduction + y_offset)
        right_top = (self.x + self.width / 2, self.y + y_offset)
        right_bottom = (self.x + self.width / 2, self.y - self.height / 2 + y_offset)

        for i in range(num_segments):
            # 각 세그먼트의 x 좌표 범위
            seg_left_x = left_bottom[0] + i * segment_width
            seg_right_x = seg_left_x + segment_width

            # 선형 보간을 통해 각 세그먼트의 y 좌표 계산
            y_low_start = left_bottom[1] + (left_top[1] - left_bottom[1]) * (i / num_segments) * 0.8
            y_low_end = left_bottom[1] + (left_top[1] - left_bottom[1]) * ((i + 1) / num_segments) * 0.8

            y_high_start = right_top[1] + (right_bottom[1] - right_top[1]) * (i / num_segments) * 0.8
            y_high_end = right_top[1] + (right_bottom[1] - right_top[1]) * ((i + 1) / num_segments) * 0.8

            # 각 세그먼트의 하단과 상단 y 좌표를 평균하여 사용
            y_low = (y_low_start + y_low_end) / 2
            y_high = (y_high_start + y_high_end) / 2

            # 바운딩 박스 추가
            bounding_boxes.append((
                seg_left_x,
                y_high,
                seg_right_x,
                y_low
            ))

        return bounding_boxes
    def get_downhill2_bb(self, num_segments=20, height_reduction=50, y_offset=0):
        bounding_boxes = []
        segment_width = self.width / num_segments

        left_bottom = (self.x - self.width / 2, self.y + self.height / 2 + y_offset)
        left_top = (self.x - self.width / 2, self.y + 150 - height_reduction + y_offset)
        right_top = (self.x + self.width / 2, self.y + y_offset)
        right_bottom = (self.x + self.width / 2, self.y - self.height / 2 + y_offset)

        for i in range(num_segments):
            # 각 세그먼트의 x 좌표 범위
            seg_left_x = left_bottom[0] + i * segment_width
            seg_right_x = seg_left_x + segment_width

            # 선형 보간을 통해 각 세그먼트의 y 좌표 계산
            y_low_start = left_bottom[1] + (left_top[1] - left_bottom[1]) * (i / num_segments) * 0.8
            y_low_end = left_bottom[1] + (left_top[1] - left_bottom[1]) * ((i + 1) / num_segments) * 0.8

            y_high_start = right_top[1] + (right_bottom[1] - right_top[1]) * (i / num_segments) * 0.8
            y_high_end = right_top[1] + (right_bottom[1] - right_top[1]) * ((i + 1) / num_segments) * 0.8

            # 각 세그먼트의 하단과 상단 y 좌표를 평균하여 사용
            y_low = (y_low_start + y_low_end) / 2
            y_high = (y_high_start + y_high_end) / 2

            # 바운딩 박스 추가
            bounding_boxes.append((
                seg_left_x,
                y_high,
                seg_right_x,
                y_low
            ))

        return bounding_boxes

    def get_downhill3_bb(self, num_segments=20, height_reduction=50, y_offset=0):
        bounding_boxes = []
        segment_width = self.width / num_segments

        left_bottom = (self.x - self.width / 2, self.y + self.height / 2 + y_offset)
        left_top = (self.x - self.width / 2, self.y + 150 - height_reduction + y_offset)
        right_top = (self.x + self.width / 2, self.y + y_offset)
        right_bottom = (self.x + self.width / 2, self.y - self.height / 2 + y_offset)

        for i in range(num_segments):
            # 각 세그먼트의 x 좌표 범위
            seg_left_x = left_bottom[0] + i * segment_width
            seg_right_x = seg_left_x + segment_width

            # 선형 보간을 통해 각 세그먼트의 y 좌표 계산
            y_low_start = left_bottom[1] + (left_top[1] - left_bottom[1]) * (i / num_segments) * 0.9
            y_low_end = left_bottom[1] + (left_top[1] - left_bottom[1]) * ((i + 1) / num_segments) * 0.9

            y_high_start = right_top[1] + (right_bottom[1] - right_top[1]) * (i / num_segments) * 0.6
            y_high_end = right_top[1] + (right_bottom[1] - right_top[1]) * ((i + 1) / num_segments) * 0.6

            # 각 세그먼트의 하단과 상단 y 좌표를 평균하여 사용
            y_low = (y_low_start + y_low_end) / 2
            y_high = (y_high_start + y_high_end) / 2

            # 바운딩 박스 추가
            bounding_boxes.append((
                seg_left_x,
                y_high,
                seg_right_x,
                y_low
            ))

        return bounding_boxes

    def get_curve1_bb(self, num_segments=20, y_offset=0, curve_depth=0.5, dip_amount=75):
        bounding_boxes = []
        segment_width = (self.width // 2) / num_segments  # x축 세그먼트 간 거리

        # 좌측 하단과 우측 상단 좌표
        left_bottom = (self.x - self.width // 2, self.y - self.height // 4 + y_offset)
        right_top = (self.x, self.y + y_offset)

        for i in range(num_segments):
            # 세그먼트의 x 좌표 계산
            seg_left_x = left_bottom[0] + i * segment_width
            seg_right_x = seg_left_x + segment_width

            # t 값 계산 (0 ~ 1)
            t_start = i / num_segments
            t_end = (i + 1) / num_segments

            # 중간에 움푹 파이는 형태 구현 (파라볼라 또는 제곱 함수 적용)
            dip_factor_start = 1 - ((t_start - 0.5) ** 2) * 4  # 중간에서 가장 낮아지도록 조정
            dip_factor_end = 1 - ((t_end - 0.5) ** 2) * 4

            # y 좌표 계산
            y_low_start = left_bottom[1] + (right_top[1] - left_bottom[1]) * (
                        t_start ** curve_depth) - dip_amount * dip_factor_start
            y_low_end = left_bottom[1] + (right_top[1] - left_bottom[1]) * (
                        t_end ** curve_depth) - dip_amount * dip_factor_end

            # 바운딩 박스 추가
            bounding_boxes.append((
                seg_left_x,  # 좌측 x
                y_low_start,  # 하단 y
                seg_right_x,  # 우측 x
                y_low_end  # 상단 y
            ))

        return bounding_boxes

    # def get_loop_bb(self, num_segments=20, radius=200, y_offset=0):
    #     bounding_boxes = []
    #     cx, cy = self.x, self.y + radius + y_offset  # 루프 중심 좌표
    #
    #     for i in range(num_segments):
    #         theta_start = 2 * math.pi * (i / num_segments)
    #         theta_end = 2 * math.pi * ((i + 1) / num_segments)
    #
    #         x1, y1 = cx + radius * math.cos(theta_start), cy + radius * math.sin(theta_start)
    #         x2, y2 = cx + radius * math.cos(theta_end), cy + radius * math.sin(theta_end)
    #
    #         bounding_boxes.append((x1, y1, x2, y2))
    #
    #     return bounding_boxes

    def get_bb(self, y_offset=0):
        # 지형 타입에 따라 충돌 박스 설정
        if self.terrain_type == 'platform':
            return [(self.x - self.width // 2,    # 좌측 하단 x
                    self.y - self.height // 2,    # 좌측 하단 y
                    self.x + self.width // 2,     # 우측 상단 x
                    self.y - 128),                # 우측 상단 y
                    (self.x - 196,
                     self.y + 41,
                     self.x + 189,
                     self.y + 68)
            ]
        elif self.terrain_type == 'plane1':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y - 128)]
        elif self.terrain_type == 'plane2':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y)]
        elif self.terrain_type == 'uphill1':
            return self.get_uphill1_bb(y_offset=y_offset - 200)
        elif self.terrain_type == 'downhill1':
            return self.get_downhill1_bb(y_offset=y_offset - 235)
        elif self.terrain_type == 'bridge':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y - 5)]
        elif self.terrain_type == 'curve1':
            # 기존 박스
            existing_bb = [
                (self.x,
                 self.y - self.height // 2,
                 self.x + self.width // 2,
                 self.y)
            ]
            # 점진적으로 올라가는 바운딩 박스 추가
            new_bb = self.get_curve1_bb(y_offset=y_offset)
            # 기존 박스와 새로운 박스를 합쳐서 반환
            return existing_bb + new_bb
        elif self.terrain_type == 'stair1':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x,
                     self.y),
                    (self.x,
                     self.y - self.height // 2,
                     self.x + 124,
                     self.y + 65),
                    (self.x + 124,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y + 130)]
        elif self.terrain_type == 'start_of_bridge':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x - self.width // 4,
                     self.y + 226)]
        elif self.terrain_type == 'plane3':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y + 226)]
        elif self.terrain_type == 'twin':
            return [(self.x - self.width // 2,
                     self.y + 196,
                     self.x + self.width // 4,
                     self.y + 226),
                    (self.x - self.width // 4,
                     self.y - self.height // 2,
                     self.x,
                     self.y - 42),
                    (self.x,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y - 21),
                    (self.x + self.width // 4,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y)]
        elif self.terrain_type == 'downhill2':
            return self.get_downhill2_bb(y_offset=y_offset - 130)
        elif self.terrain_type == 'downhill3':
            return self.get_downhill3_bb(y_offset=y_offset - 250)
        elif self.terrain_type == 'loop':
            return [
                (self.x - self.width // 2,
                 self.y - self.height // 2,
                 self.x + self.width // 2,
                 self.y - self.height // 4)
            ]
        elif self.terrain_type == 'uphill2':
            return self.get_uphill2_bb(y_offset=y_offset - 150)
        elif self.terrain_type == 'plane4':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y)]
        elif self.terrain_type == 'wall1':
            return []
        elif self.terrain_type == 'plane5':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y)]
        elif self.terrain_type == 'plane6':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y - self.height // 4)]
        elif self.terrain_type == 'plane7':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y - self.height // 4)]
        elif self.terrain_type == 'plane8':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y - self.height // 4)]
        elif self.terrain_type == 'stair2':
            return [(self.x - self.width // 2,
                     self.y - self.height // 2,
                     self.x - 66,
                     self.y - 126),
                    (self.x - 66,
                     self.y - self.height // 2,
                     self.x + 127,
                     self.y - 62),
                    (self.x + 127,
                     self.y - self.height // 2,
                     self.x + self.width // 2,
                     self.y)]
        else:
            return [
                (self.x - self.width // 2,
                 self.y - self.height // 2,
                 self.x + self.width // 2,
                 self.y + self.height // 2)
            ]


# 뒷배경 클래스
class Background:
    def __init__(self):
        self.image = load_image('sprites/background.jpg')
        self.map_width = 19328 # 전체 맵 너비
        self.map_height = 2000
        self.screen_width = 800  # 화면 너비
        self.screen_height = 600

    def draw(self, camera_x, camera_y):
        self.image.draw(self.screen_width // 2, self.screen_height // 2, self.screen_width, self.screen_height)

    def update(self):
        pass