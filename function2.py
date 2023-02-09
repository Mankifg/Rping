from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import string
import csv

def read_csv_file(fdir):
    with open(fdir, encoding="utf-8", newline="") as file:
        return list(csv.reader(file))

alhabet = string.ascii_lowercase
file_out = "./data/out.csv"

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

    last = read_csv_file(file_out)
    last = last[-1][0]
    print(last)

    try:
        last = int(last)
    except ValueError:
        last = 0

    last = last + 1

    n = last - 2

    if n < 1:
        n = 1
    while True:
        v = sheet.acell(f"A{n}").value
        if v == None:
            print(n)
            break
        else:
            n = n + 1

    sheet.update(f"A{n}:{alhabet[len(inp)]}{n}", [inp])

