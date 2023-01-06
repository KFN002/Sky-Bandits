import pygame_menu
from pygame_menu import sound, Theme
import pygame
from pygame import mixer
import game_menu


def check_player(name):
    print(list(name.values()))
    return True


def start_game():
    if check_player(menu.get_input_data()):
        mixer.music.stop()
        menu.close()
        game_menu.start()
    else:
        menu.reset_value()


pygame.init()
pygame.display.set_caption('Sky Bandits')
mixer.music.load('data/music/theme.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)
background = pygame_menu.baseimage.BaseImage('data/background.jpg')
sc_size = width, height = 1200, 600
surface = pygame.display.set_mode(sc_size)
my_theme = Theme(background_color=(0, 0, 0, 0), title_background_color=(4, 47, 126),
                 title_font_shadow=True, title_font=pygame_menu.font.FONT_8BIT,
                 widget_padding=25, widget_font=pygame_menu.font.FONT_8BIT,
                 title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
                 widget_font_color=pygame.Color('white'))
my_theme.background_color = background
menu = pygame_menu.Menu('Sky Bandits', width, height, theme=my_theme)
menu.add.label('Login or Sign up', font_size=20)
menu.add.text_input('', default='Your name', font_size=20)
menu.add.text_input('', default='Your password', font_size=20)
menu.add.button('Play', start_game, font_size=40)
menu.add.button('Quit', pygame_menu.events.EXIT, font_size=30)
menu.center_content()
menu.add.label('Game by KFN001', align=pygame_menu.locals.ALIGN_LEFT,
               font_color=pygame.Color('grey'), font_size=8)
engine = sound.Sound(-1)
engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, 'data/music/button.wav')
engine.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_ADDITION, 'data/music/button.wav')
engine.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_DELETION, 'data/music/button.wav')
menu.set_sound(engine, recursive=True)
menu.mainloop(surface, fps_limit=60)