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

    try:
        last = int(last)
    except ValueError:
        last = 0
        
    n = last + 1

    sheet.update(f"A{n}:{alhabet[len(inp)]}{n}", [inp])

