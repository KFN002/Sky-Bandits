import sqlite3
import webbrowser
from random import choice


def redirect(plane):   # запуск браузра с инфой: ссылка в бд
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    web_page = cur.execute(f"""SELECT web_page FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
    con.close()
    webbrowser.open(web_page[0])
    if choice([True, False, False, False, False, False, False, False]):
        webbrowser.open('https://www.youtube.com/watch?v=VE03Lqm3nbI')

