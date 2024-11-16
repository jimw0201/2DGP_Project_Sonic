from pico2d import load_image, get_events, clear_canvas, update_canvas, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import play_mode


def init():
    global image, bgm
    image = load_image('title.png')

    bgm = load_music('title.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()

def finish():
    global image, bgm
    del image

    bgm.stop()
    del bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass