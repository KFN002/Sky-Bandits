import sqlite3
import webbrowser


def redirect(plane):
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    web_page = cur.execute(f"""SELECT web_page FROM planes WHERE model = '{plane[0][0]}'""").fetchone()
    con.close()
    webbrowser.open(web_page[0])
