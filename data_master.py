import gspread
import sqlite3
from oauth2client.service_account import ServiceAccountCredentials

'''
name = 'Sky Bandits: players'
sheet = client.create(name)
sheet.share('fedotovkirill4000@gmail.com', perm_type='user', role='writer')
sheet.row_values(3)
sheet.col_values(2)
sheet.cell(2, 2).value()
sheet = client.open(name).sheet1
sheet.update_cell(1, 1, "Ivan")
print(sheet.append_row(['Mike'], 2))
print(sheet.get_all_values())
'''


def check_player(name, password):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet_check = client.open('Sky Bandits: players').sheet1
    data = sheet_check.get_all_values()
    players = list(map(lambda x: x[:2], data))
    if [name, password] in players:
        return data[players.index([name, password])]
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    result = cur.execute("""SELECT model from planes""").fetchall()
    con.close()
    planes = int('1' + '0' * (len(list(result)) - 1))
    sheet_check.append_row([name, password, 100, 0, planes])
    return [name, password, 100, 0, planes]


def change_value(price, player_data, plane):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open('Sky Bandits: players').sheet1
    data = sheet.get_all_values()
    players = list(map(lambda x: x[:2], data))
    row = players.index(player_data[:2])
    sheet.update_cell(row + 1, 3, int(sheet.cell(row + 1, 3).value) - int(price))
    all_planes = []
    con = sqlite3.connect('planes.db')
    cur = con.cursor()
    results = cur.execute(f"""SELECT model FROM planes ORDER BY price""").fetchall()
    con.close()
    for elems in results:
        all_planes.append(elems[0])
    bought = all_planes.index(plane)
    new_planes = list(str(player_data[4]))
    new_planes[bought] = 1
    planes_own = ''.join(str(a) for a in new_planes)
    sheet.update_cell(row + 1, 5, int(planes_own))
