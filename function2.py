from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import string

alhabet = string.ascii_lowercase


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "key.json", scopes
)  # access the json key you downloaded earlier
file = gspread.authorize(credentials)  # authenticate the JSON key with gspread
sheet = file.open("sheet1")  # open sheet

# replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
sheet = sheet.sheet1

def update(inp):
    all_cells = sheet.range("A1:D10")
    n = 1
    while True:
        v = sheet.acell(f"A{n}").value
        print(v)
        if v == None:
            print(n)
            break
        else:
            n = n + 1

    sheet.update(f"A{n}:{alhabet[len(inp)]}{n}", [inp])

