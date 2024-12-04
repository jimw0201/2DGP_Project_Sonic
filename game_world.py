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

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

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