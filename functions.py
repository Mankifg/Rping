import datetime
import os
import csv
import json
os.system("cls")
mode = ""

import platform
operating_system = platform.system()

with open('settings.json') as f:
    data = json.load(f)

file_name = data["ips_path"]
n_of_ip = data["point_of_ip"]
file_out = data["file_out"]


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

def read_csv_file(fdir):
    with open(fdir, encoding='utf-8', newline='') as file:
        return list(csv.reader(file))

def write_to_csv_file(fdir,rows):
    with open(fdir, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(rows) 
 


raw = read_csv_file(file_name)

for i in range(len(raw)):
    ips.append(raw[i][n_of_ip])
    is_computer.append(int(raw[i][n_of_ip +1]))

out = read_csv_file(file_out)

if out == []:
    write_to_csv_file(file_out,["Dan","Ura","Moč","Prizgani_rac","Przigane_table","Vsi_rac","Vse_table"])

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

def get_all():
    print(is_computer)
    return is_computer.count(1),is_computer.count(0)


def get_power(specific_list):
    p = 0

    if not len(specific_list) == len(ips):
        print("[ERROR] List size does not match ip number. Exiting")
        exit()

    for a,b in zip(specific_list,is_computer):
        if int(a) == 1: # prizgan
            if int(b) == 1: # computer
                p = p + computer
            else:
                p = p + not_computer
    return p



def get_prizgane(specific_list):
    pc = 0
    table = 0

    for a,b in zip(specific_list,is_computer):
        if int(a) == 1:  # prizgano
            if int(b) == 1:  # computer
                pc = pc + 1
            else:
                table = table + 1

    return pc, table

def get_ip():
    if mode == "linux":
        return "127.0.0.1"
    else:
        return "0.0.0.0"

def save(power,p_pc,p_table,all_pc,all_table):
    # ["Dan","Ura","Moč","Prizgani_rac","Przigane_table","Vsi_rac","Vse_table"]
    dan = datetime.datetime.now().strftime("%Y-%m-%d")
    hour = datetime.datetime.now().strftime("%H-%M")
    data = [dan,hour,power,p_pc,p_table,all_pc,all_table]
    print(data)
    write_to_csv_file(file_out,data)
      
