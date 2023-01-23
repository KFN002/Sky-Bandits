import sqlite3
import pygame_menu
from pygame_menu import sound, Theme
import pygame
from pygame import mixer
import data_master
import game_menu
from data_master import check_player


def start_game(menu):
    player_info = list(menu.get_input_data().values())
    if len(player_info[0]) >= 4 and len(player_info[1]) >= 4:
        data = check_player(*player_info)
        if data is None:
            menu.reset_value()
        else:
            mixer.music.stop()
            menu.close()
            game_menu.start(data)
    else:
        menu.reset_value()


def start_menu():
    pygame.init()
    pygame.display.set_caption('Sky Bandits')
    mixer.music.load('data/music/theme.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)
    background = pygame_menu.baseimage.BaseImage('data/backgrounds/background.jpg')
    sc_size = width, height = 1200, 600
    surface = pygame.display.set_mode(sc_size)
    my_theme = Theme(background_color=(0, 0, 0, 0), title_background_color=(4, 47, 126),
                     title_font_shadow=True, title_font=pygame_menu.font.FONT_8BIT,
                     widget_padding=25, widget_font=pygame_menu.font.FONT_8BIT,
                     title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
                     widget_font_color=pygame.Color('white'))
    my_theme.background_color = background
    menu = pygame_menu.Menu('Sky Bandits', width, height, theme=my_theme)
    menu.add.image('data/logos/game_dev_logo.jpg', load_from_file=True,
                   align=pygame_menu.locals.ALIGN_RIGHT)
    menu.add.label('Login or Sign up', font_size=20)
    menu.add.text_input('Name:', font_size=20)
    menu.add.text_input('Password:', font_size=20)
    play_btn = menu.add.button('Play', start_game(menu), font_size=40)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_size=30)
    menu.center_content()
    menu.add.label('Game by KFN001', align=pygame_menu.locals.ALIGN_LEFT,
                   font_color=pygame.Color('grey'), font_size=8)
    added_planes = menu.add.button('Update planes from DB', font_size=8, align=pygame_menu.locals.ALIGN_LEFT)
    engine = sound.Sound(-1)
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'data/music/button.wav')
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_ADDITION, 'data/music/button.wav')
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_DELETION, 'data/music/button.wav')
    menu.set_sound(engine, recursive=True)
    while True:
        events = pygame.event.get()
        if play_btn.is_selected():
            start_game(menu)
        if added_planes.is_selected():
            con = sqlite3.connect('planes.db')
            cur = con.cursor()
            plane_quantity = cur.execute(f"""SELECT COUNT(*) FROM planes""").fetchone()
            con.close()
            if int(plane_quantity[0]) - 10 >= 1:
                data_master.game_update(int(plane_quantity[0]) - 10)
            else:
                added_planes.hide()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.flip()


start_menu()
