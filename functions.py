from datetime import datetime
import os
import csv
import json
import platform
import function2

mode = ""
operating_system = platform.system()

with open("settings.json") as f:
    data = json.load(f)

file_name = data["ips_path"]
n_of_ip = data["point_of_ip"]
file_out = data["file_out"]
daily_path = data["file_day"]
finish_time = data["finish_time"]

computer = data["power"]["computer"]
not_computer = data["power"]["not_computer"]

if operating_system == "Windows":
    mode = "win"
    ping_cmd = data["mode"][0]["ping"]
    key_word = data["mode"][0]["key_word"]
    os.system("cls")
elif operating_system == "Linux":
    mode = "linux"
    ping_cmd = data["mode"][1]["ping"]
    key_word = data["mode"][1]["key_word"]
    os.system("clear")
else:
    print("[ERROR] Either MacOS or something else\nDo it yourself.")
    exit()

ips = []
is_computer = []
place = []

with open("./save.txt","w") as f:
    f.write("-1|-1|-1|-1|-1")
with open("./tmp.txt","w") as f:
    pass

def read_csv_file(fdir):
    with open(fdir, encoding="utf-8", newline="") as file:
        return list(csv.reader(file))


def write_to_csv_file(fdir, rows):
    with open(fdir, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(rows)


raw = read_csv_file(file_name)

for i in range(len(raw)):
    place.append(raw[i][n_of_ip-1])
    ips.append(raw[i][n_of_ip])
    is_computer.append(int(raw[i][n_of_ip + 1]))

# Very IMP:
is_computer.append(0)

out = read_csv_file(file_out)
daily = read_csv_file(file_out)

if out == []:
    write_to_csv_file(
        file_out,
        [
            "N",
            "Dan",
            "Ura",
            "Moč",
            "Prizgani_rac",
            "Przigane_table",
            "Vsi_rac",
            "Vse_table",
        ],
    )

if daily == []:
    write_to_csv_file(daily_path, ["Dan","Čas","Moč"])

def get_table(specific_list):

    with open("out.txt","r") as f:
        d = f.read().splitlines()

    last_ele = int(d[-1])

    print(last_ele)

    if last_ele > 5:
        specific_list.append(1)
    else:
        specific_list.append(0)

    return specific_list


def fromiplisttoonlinecomputers():
    specific = []
    alive = 0
    dead = 0
    for i, ip in enumerate(ips):
        try:
            os.system(ping_cmd.format(ip))

            with open("tmp.txt", "r") as f:
                ret = f.read()

            pl = place[ips.index(ip)]
            if key_word in ret:
                alive = alive + 1
                specific.append(1)
                print(f"[+] {ip} - {pl}")
            else:
                specific.append(0)
                print(f"[-] {ip} - {pl}")
        except KeyboardInterrupt:
            print("keyboard")

    specific = get_table(specific)
    return specific


def get_all():
    return is_computer.count(1), is_computer.count(0)


def get_power(specific_list):
    p = 0



    for a, b in zip(specific_list, is_computer):
        if int(a) == 1:  # prizgan
            if int(b) == 1:  # computer
                p = p + computer
            else:
                p = p + not_computer
    return p


def get_prizgane(specific_list):
    pc = 0
    table = 0

    for a, b in zip(specific_list, is_computer):
        if int(a) == 1:  # prizgano
            if int(b) == 1:  # computer
                pc = pc + 1
            else:
                table = table + 1

    return pc, table


def ip():
    if mode == "linux":
        ip = input("Enter your's ip >")
        return ip
    else:
        return "0.0.0.0"


def save(power, p_pc, p_table, all_pc, all_table):
    # [n,"Dan","Ura","Moč","Prizgani_rac","Prizgane_table","Vsi_rac","Vse_table"]
    last = read_csv_file(file_out)
    last = last[-1][0]

    try:
        last = int(last)
    except ValueError:
        last = 0

    last = last + 1

    dan = datetime.now().strftime("%d.%m.%Y")
    hour = datetime.now().strftime("%H:%M:%S")
    data = [last, dan, hour, power, p_pc, p_table, all_pc, all_table]
    write_to_csv_file(file_out, data)
    function2.update(data)


def fromhour_to_seconds(t):
    t = t.split(":")
    t1 = int(t[0]) * 60 * 60 + int(t[1]) * 60 + int(t[2])
    return t1


def calculate_power(day):
    data = read_csv_file(file_out)
    data.pop(0)

    f = 0
    for i, v in enumerate(data):
        if v[1] == day:  # same day
            time1 = v[2]
            try:
                time2 = data[i + 1][2]
            except IndexError:
                time2 = v[2]

            time1_s = fromhour_to_seconds(time1)
            time2_s = fromhour_to_seconds(time2)

            diff = time2_s - time1_s
            diff_h = diff / 60 / 60

            p = int(v[3])
            kp = p / 1000

            kwh = diff_h * kp
            f = f + kwh

    return f


# Todo
def checkfordaily():
    dan = datetime.now().strftime("%d. %m. %Y")
    time = datetime.now().strftime("%H:%M:%S")

    #! if (time == finish_time):
    if True:
        pp = calculate_power(dan)
        pp = round(pp,5)
        write_to_csv_file(daily_path, [dan,time,pp])