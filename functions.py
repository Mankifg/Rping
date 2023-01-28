import time
import os
import csv
import json

mode = ""

import platform
operating_system = platform.system()

with open('settings.json') as f:
    data = json.load(f)

file_name = data["ips_path"]
n_of_ip = data["point_of_ip"]

computer = data["power"]["computer"]
not_computer = data["power"]["not_computer"]

if operating_system == "Windows":
    mode = "win"
    ping_cmd = data["mode"][0]["ping"]
    key_word = data["mode"][0]["key_word"]
elif operating_system == "Linux":
    mode = "linux"
    ping_cmd = data["mode"][1]["ping"]
    key_word = data["mode"][1]["key_word"]
else:
    print("[ERROR] Either MacOS or something else\nDo it yourself.")
    exit()

ips = []
is_computer = []

def read_csv_file():
    with open(file_name, encoding='utf-8', newline='') as file:
        return list(csv.reader(file))

raw = read_csv_file()

for i in range(len(raw)):
    ips.append(raw[i][n_of_ip])
    is_computer.append(raw[i][n_of_ip +1])


def naprave():
    return len(ips)

def fromiplisttoonlinecomputers():
    specific = []
    alive = 0
    dead = 0
    for i,ip in enumerate(ips):
        os.system(ping_cmd.format(ip))


        with open("tmp.txt", "r") as f:
            ret = f.read()

        if key_word in ret:
            alive = alive +1
            specific.append(1)
            print(f"[+] {ip}")
        else:
            specific.append(0)
            print(f"[-] {ip}")

    return specific


def get_power(specific_list):
    p = 0

    if not len(specific_list) == len(ips):
        print("[ERROR] List size does not match ip number. Exiting")
        exit()

    for a,b in zip(is_computer,specific_list):
        if int(a) == 1: # prizgan
            if int(b) == 1: # computer
                p = p + computer
            else:
                p = p + not_computer

    return p

def get_table(specific_list):
    c = 0
    for a,b in zip(is_computer,specific_list):
        if int(a) == 0 and int(b) == 1:
            c = c+1

    return c

def get_racunalniki(specific_list):
    c = 0
    for a,b in zip(is_computer,specific_list):
        if int(a) == 1 and int(b) == 1:
            c = c+1

    return c