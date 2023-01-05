import pygame
import pygame_menu
from pygame_menu import Theme
from pygame import mixer


def draw_background():
    print('drawing')


pygame.init()
pygame.display.set_caption('Sky Bandits')
mixer.music.load('data/music/arcade_theme.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()
background = pygame_menu.baseimage.BaseImage('data/hangar.png')
sc_size = width, height = 1200, 600
surface = pygame.display.set_mode(sc_size)
my_theme = Theme(background_color=(0, 0, 0, 0), title_background_color=(4, 47, 126),
                 title_font_shadow=True, title_font=pygame_menu.font.FONT_8BIT,
                 widget_padding=25, widget_font=pygame_menu.font.FONT_8BIT,
                 title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
                 widget_font_color=pygame.Color('white'))
my_theme.background_color = background
menu = pygame_menu.Menu('Sky Bandits', width, height, theme=my_theme)
menu.mainloop(surface, fps_limit=60, bgfun=draw_background)