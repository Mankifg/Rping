from flask import Flask, render_template
from flask_apscheduler import APScheduler
import datetime
import functions
import json

app = Flask(__name__)

with open('settings.json') as f:
    data = json.load(f)

time_sleep = data["time_interval"]

def update_n():
    specific_list = functions.fromiplisttoonlinecomputers()
    power = functions.get_power(specific_list)

    prizgani_racunalniki, prizgane_table = functions.get_prizgane(specific_list)

    vsi_racunalniki, vse_table = functions.get_all()
    print(vsi_racunalniki, vse_table)
    r = f"{power}-{prizgani_racunalniki}-{prizgane_table}-{vsi_racunalniki}-{vse_table}"
    functions.save(
        power, prizgani_racunalniki, prizgane_table, vsi_racunalniki, vse_table
    )

    with open("save.txt", "w") as f:
        f.write(r)

    functions.checkfordaily()


@app.route("/")
def main():
    with open("save.txt", "r") as f:
        data = f.read()
    data = data.split("-")
    p_pc = data[1]
    p_table = data[2]
    all_pc = data[3]
    all_table = data[4]
    power = data[0]
    all_napreve = int(all_pc) + int(all_table)
    p_naprave = int(p_pc) + int(p_table)
    return render_template(
        "index.html",
        p_pc=p_pc,
        all_pc=all_pc,
        p_table=p_table,
        all_table=all_table,
        p_all=p_naprave,
        all_naprave=all_napreve,
        power=power,
    )

if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.add_job(func=update_n, trigger="interval", id="job", seconds=time_sleep)
    scheduler.start()
    app.run(host=functions.ip(), port=80, debug=False)