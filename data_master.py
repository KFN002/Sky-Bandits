import gspread
from oauth2client.service_account import ServiceAccountCredentials
import offline
import sqlite3
import pygame_menu
from pygame_menu import sound, Theme
import pygame
from pygame import mixer
import game_menu

'''
name = 'Sky Bandits: players'
sheet = client.create(name)
sheet.share('fedotovkirill4000@gmail.com', perm_type='user', role='writer')
'''


def connect():
    if offline.test_connection():
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(credentials)
        sheet = client.open('Sky Bandits: players').sheet1
        return sheet
    else:
        exit()


def check_player(name, password):
    sheet_check = connect()
    data = sheet_check.get_all_values()
    players = list(map(lambda x: x[:2], data))
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute("""SELECT model from planes""").fetchall()
    con.close()
    if [name, password] in players:
        return data[players.index([name, password])]
    names = list(map(lambda x: x[0], players))
    if name in names and players[names.index(name)][1] != password:
        return None
    planes = int('1' + '0' * (len(list(result)) - 1))
    sheet_check.append_row([name, password, 100, 0, planes])
    return [name, password, 100, 0, planes]


def change_value(price, player_data, plane):
    sheet = connect()
    data = sheet.get_all_values()
    players = list(map(lambda x: x[:2], data))
    row = players.index(player_data[:2])
    if int(sheet.cell(row + 1, 3).value) - int(price) >= 0:
        sheet.update_cell(row + 1, 3, int(sheet.cell(row + 1, 3).value) - int(price))
        all_planes = []
        con = sqlite3.connect('planes.db')
        cur = con.cursor()
        results = cur.execute(f"""SELECT model FROM planes ORDER BY price""").fetchall()
        con.close()
        for elem in results:
            all_planes.append(elem[0])
        bought = all_planes.index(plane[0][0])
        new_planes = list(str(player_data[4]))
        new_planes[bought] = 1
        planes_own = ''.join(str(a) for a in new_planes)
        sheet.update_cell(row + 1, 5, int(planes_own))


def game_update(planes_added):
    sheet = connect()
    for row in range(1, len(sheet.get_all_values())):
        sheet.update_cell(row + 1, 5, int(str(sheet.cell(row + 1, 5).value) + '0' * planes_added))


def change_score_money(player_data, score):
    sheet = connect()
    data = sheet.get_all_values()
    players = list(map(lambda x: x[:2], data))
    row = players.index(player_data[:2])
    sheet.update_cell(row + 1, 3, (int(sheet.cell(row + 1, 3).value) + score))
    if score > int(sheet.cell(row + 1, 4).value):
        sheet.update_cell(row + 1, 4, score)
    show_info(player_data)


def show_info(player_data):
    sheet = connect()
    data = sheet.get_all_values()
    players = list(map(lambda x: (x[0], x[3]), data))[1:]
    players = sorted(players, key=lambda x: int(x[1]), reverse=True)[:10]
    pygame.init()
    pygame.display.set_caption('Results')
    win = mixer.Sound('data/music/win.mp3')
    win.set_volume(0.5)
    win.play()
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
    menu.add.label('Leaderboard')
    table = menu.add.table(font_size=30, border_color=pygame.Color('white'), border_width=3)
    for gamer in players:
        table.add_row(gamer)
    continue_btn = menu.add.button('Continue', font_size=40)
    menu.add.button('Quit', pygame_menu.events.EXIT, font_size=30)
    menu.center_content()
    engine = sound.Sound(-1)
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'data/music/button.wav')
    menu.set_sound(engine, recursive=True)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and continue_btn._mouseover and event.button == 1:
                win.stop()
                game_menu.start(player_data)
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.flip()
