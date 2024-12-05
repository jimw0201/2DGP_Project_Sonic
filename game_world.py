objects = [[] for _ in range(4)]
collision_pairs = {}

def add_object(o, depth=0):
    objects[depth].append(o)

def add_objects(ol, depth=0):
    objects[depth] += ol

def update():
    for layer in objects:
        for o in layer:
            o.update()

def render(camera_x=0, camera_y=0):
    for layer in objects:
        for o in layer:
            o.draw(camera_x, camera_y)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non-existing object')

def clear():
    global objects
    objects = [[] for _ in range(4)]

def check_collision(A, B):
    print(f"Checking collision: A={A}, B={B}")  # 디버깅용 출력
    Ax1, Ay1, Ax2, Ay2 = A
    Bx1, By1, Bx2, By2 = B

    if not (Ax2 < Bx1 or Ax1 > Bx2 or Ay1 > By2 or Ay2 < By1):
        return True  # 충돌함
    return False  # 충돌하지 않음

def collide(a, b):
    a_bb_list = a.get_bb()
    b_bb_list = b.get_bb()

    print(f"a_bb_list: {a_bb_list}, b_bb_list: {b_bb_list}")  # 디버깅용 출력

    for a in a_bb_list:
        for b in b_bb_list:
            if check_collision(a, b):
                return True
    return False


def add_collision_pair(a, b, group):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if isinstance(a, list):
        collision_pairs[group][0].extend(a)
    else:
        collision_pairs[group][0].append(a)
    if isinstance(b, list):
        collision_pairs[group][1].extend(b)
    else:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)