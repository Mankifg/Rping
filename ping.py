import time
import os
import csv
 
ips = []
file_name = "ips.csv"
n_of_ip = 2

def read_csv_file():
    with open(file_name, encoding='utf-8', newline='') as file:
        return list(csv.reader(file))

raw = read_csv_file()

for i in range(len(raw)):
    ips.append(raw[i][n_of_ip])

def checkforip(c_ip):
    os.system(f"ping {c_ip} -n 4 > tmp.txt")
    with open("tmp.txt", "r") as f:
        ret = f.read()

    if "bytes=32" in ret:
        return True
    else:
        return False

def fromiplisttoonlinecomputers():
    alive = 0
    dead = 0
    for i,ip in enumerate(ips):
        if checkforip(ip):
            alive = alive + 1
        else:
            dead = dead + 1
        

    return alive

fromiplisttoonlinecomputers()