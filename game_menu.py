import pygame
import pygame_menu
from pygame_menu import Theme, sound
from pygame import mixer
import sqlite3


def draw_background(plane, menu_dr, pic):
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT hist_pic, hist_text FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
    print(result)
    pic.set_image(pygame_menu.baseimage.BaseImage(result[0]))
    '''
    with open(result[1], 'rt', encoding='utf-8', newline='\r\n') as data:
        text = data.read()
        print(text)
        info.set_title(text)
    con.close()
    '''


def buy_plane(plane):
    pass
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT price FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
    print(result[0])
    con.close()


def game(num):
    pass


def show_info():
    pass


def start():
    pygame.init()
    planes = []
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute("""SELECT model, hist_pic, hist_text from planes""").fetchall()
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
    menu.add.label(f'Money {money}', align=pygame_menu.locals.ALIGN_RIGHT, font_size=18)
    current_plane = menu.add.selector('Select Plane', planes, align=pygame_menu.locals.ALIGN_RIGHT, font_size=24)
    '''
    plane_info = menu.add.label('plane info', align=pygame_menu.locals.ALIGN_RIGHT, font_size=8)
    '''
    pic_place = menu.add.image('data/real_pics/mig-21bis.jpg', load_from_file=True,
                               align=pygame_menu.locals.ALIGN_RIGHT)
    buy_button = menu.add.button('BUY Plane', buy_plane(current_plane.get_value()),
                                 align=pygame_menu.locals.ALIGN_RIGHT, font_size=20)
    menu.add.button('Play Sturm', game(1), align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
    menu.add.button('Play War', game(2), align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
    menu.add.button('Play Onslaught', game(3), align=pygame_menu.locals.ALIGN_LEFT, font_size=28)
    menu.add.button('Quit', pygame_menu.events.EXIT, align=pygame_menu.locals.ALIGN_RIGHT, font_size=18)
    engine = sound.Sound(-1)
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'data/music/button.wav')
    menu.set_sound(engine, recursive=True)
    while True:
        draw_background(current_plane.get_value(), menu, pic_place)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.flip()


start()

