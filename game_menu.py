import pygame
import pygame_menu
import sqlite3
import game1
import game2
import data_master
from pygame_menu import Theme, sound
from pygame import mixer
from show_info import redirect
from random import choice


def compare_data(plane, planes_available, all_planes):   # проврека наличия самолета в приобритенных
    planes_available = list(str(planes_available))
    all_planes = list(map(lambda x: x[0], all_planes))
    return planes_available[all_planes.index(plane[0][0])]


def draw_background(plane, buy_btn, pic, planes_available, all_planes):  # подгрузка пикчи самолета, покупка
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT hist_pic, hist_text, price FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
    con.close()
    pic.set_image(pygame_menu.baseimage.BaseImage(result[0]))
    if compare_data(plane, planes_available, all_planes) == '1':
        buy_btn.set_title('')
    else:
        buy_btn.set_title(f'Buy {result[2]}')


def start_game(plane_status, plane, player_data):   # запуск уровня, подгрузка данных
    if plane_status.get_title() == '':
        con = sqlite3.connect('planes.db')
        cur = con.cursor()
        plane_data = cur.execute(f"""SELECT * FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
        con.close()
        mixer.stop()
        mixer.music.load('data/music/mission.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)
        if choice([True, False]):
            game1.play(list(plane_data), player_data)
        else:
            game2.play(list(plane_data), player_data)


def buy_plane(plane, player_data, planes_available, all_planes, menu):   # покупка самолета
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT price FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
    con.close()
    if compare_data(plane, planes_available, all_planes) == '0':
        data_master.change_value(result[0], player_data, plane)
        menu.close()
        start(data_master.check_player(*player_data[:2]))


def start(player_data):   # меню с выбором самолета, приобритениием его
    pygame.init()
    planes = []
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute("""SELECT model, hist_pic, hist_text, price from planes ORDER BY price""").fetchall()
    for i, j in enumerate(result):
        planes.append((j[0], i))
    money = player_data[2]
    con.close()
    pygame.display.set_caption('Sky Bandits')
    mixer.music.load('data/music/arcade_theme.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)
    background = pygame_menu.baseimage.BaseImage('data/backgrounds/hangar.png')
    sc_size = width, height = 1200, 650
    surface = pygame.display.set_mode(sc_size)
    my_theme = Theme(background_color=(0, 0, 0, 0), title_background_color=(4, 47, 126),
                     title_font_shadow=True, title_font=pygame_menu.font.FONT_8BIT,
                     widget_padding=25, widget_font=pygame_menu.font.FONT_8BIT,
                     title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
                     widget_font_color=pygame.Color('white'))
    my_theme.background_color = background
    menu = pygame_menu.Menu('Sky Bandits', width, height, theme=my_theme)
    menu.add.label(f'Money {money}', align=pygame_menu.locals.ALIGN_RIGHT, font_size=24)
    current_plane = menu.add.selector('Select Plane', planes, align=pygame_menu.locals.ALIGN_RIGHT, font_size=24)
    pic_place = menu.add.image('data/real_pics/mig-21bis.jpg', load_from_file=True,
                               align=pygame_menu.locals.ALIGN_RIGHT)
    info_btn = menu.add.button('View plane info', align=pygame_menu.locals.ALIGN_RIGHT, font_size=16)
    buy_button = menu.add.button('', buy_plane(current_plane.get_value(),
                                               player_data, player_data[4], planes, menu),
                                 align=pygame_menu.locals.ALIGN_RIGHT, font_size=26)
    start_btn = menu.add.button('Play level', align=pygame_menu.locals.ALIGN_LEFT, font_size=30)
    menu.add.button('Quit', pygame_menu.events.EXIT, align=pygame_menu.locals.ALIGN_RIGHT, font_size=18)
    engine = sound.Sound(-1)
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'data/music/button.wav')
    menu.set_sound(engine, recursive=True)
    running = True
    while running:
        draw_background(current_plane.get_value(), buy_button, pic_place, player_data[4], planes)
        events = pygame.event.get()
        for event in events:  # проверка кнопок: сделанно именно так, тк встроенные функции не полностью удовлетворяли
            # нужному функционалу
            if event.type == pygame.MOUSEBUTTONDOWN and buy_button._mouseover and event.button == 1:
                buy_plane(current_plane.get_value(), player_data, player_data[4], planes, menu)
            if event.type == pygame.MOUSEBUTTONDOWN and start_btn._mouseover and event.button == 1:
                start_game(buy_button, current_plane.get_value(), player_data)
            if event.type == pygame.MOUSEBUTTONDOWN and info_btn._mouseover and event.button == 1:
                redirect(current_plane.get_value())
            if event.type == pygame.QUIT:
                running = False
        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.flip()
    exit()
