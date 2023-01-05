import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
name = input()
'''
sheet = client.create(name)
sheet.share('fedotovkirill4000@gmail.com', perm_type='user', role='writer')
sheet.row_values(3)
sheet.col_values(2)
sheet.cell(2, 2).value
'''
sheet = client.open(name).sheet1
sheet.update_cell(1, 1, "Ivan")
print(sheet.append_row(['Mike'], 2))
print(sheet.get_all_values())