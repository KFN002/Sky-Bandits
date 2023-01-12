import pygame
import os


def load_image(file_name, colorkey=None):
    full_name = os.path.join('data', file_name)
    if not os.path.isfile(full_name):
        print(f'No {file_name} file in the directory.')
        exit()
    image = pygame.image.load(full_name)
    if colorkey is None:
        image = image.convert_alpha()
    elif colorkey == -1:
        image.set_colorkey(image.get_at((0, 0)))
    else:
        image.set_colorkey(colorkey)
    return image


'''
if __name__ == "__main__":
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    image = load_image('bomb.png')
    running = True
    screen.fill('white')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        screen.blit(image, (250, 250))
        pygame.display.flip()
    pygame.quit()
'''
