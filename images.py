import pygame
import os


def load_image(file_name, color_key=None):
    full_name = os.path.join('data', file_name)
    if not os.path.isfile(full_name):
        print(f'No {file_name} file in the directory.')
        exit()
    image = pygame.image.load(full_name)
    if color_key is None:
        image = image.convert_alpha()
    elif color_key == -1:
        image.set_colorkey(image.get_at((0, 0)))
    else:
        image.set_colorkey(color_key)
    return image
