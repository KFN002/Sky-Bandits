import pygame
import pygame_menu
from pygame_menu import Theme
from pygame import mixer
import sqlite3


def draw_background():
    pic = pygame_menu.baseimage.BaseImage('data/planes/f-4c.png')


def buy_plane():
    pass


def game(num):
    pass


def start():
    pygame.init()
    planes = []
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute("""SELECT model, image from planes""").fetchall()
    for i, j in enumerate(result):
        planes.append((j[0], i))
    print(planes)
    money = 100
    con.close()
    pygame.display.set_caption('Sky Bandits')
    mixer.music.load('data/music/arcade_theme.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)
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
    menu.add.label(f'Money {money}', align=pygame_menu.locals.ALIGN_RIGHT)
    menu.add.selector('Select Plane', planes, align=pygame_menu.locals.ALIGN_RIGHT)
    menu.add.button('BUY Plane', buy_plane, align=pygame_menu.locals.ALIGN_RIGHT)
    menu.add.button('Play Sturm', game(1), align=pygame_menu.locals.ALIGN_LEFT)
    menu.add.button('Play War', game(2), align=pygame_menu.locals.ALIGN_LEFT)
    menu.add.button('Play Defend', game(3), align=pygame_menu.locals.ALIGN_LEFT)
    menu.add.button('Play onslaught', game(4), align=pygame_menu.locals.ALIGN_LEFT)
    menu.mainloop(surface, fps_limit=60, bgfun=draw_background)


start()
