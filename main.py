from flask import Flask,render_template,url_for,request,redirect, make_response
from flask_apscheduler import APScheduler
import datetime
import random
import functions

app = Flask(__name__)
def update_n():
    specific_list = functions.fromiplisttoonlinecomputers()
    racunalniki = functions.get_racunalniki(specific_list)
    table = functions.get_table(specific_list)
    get_power = functions.get_power(specific_list)
    naprave = functions.naprave()
    r = f"{racunalniki}-{table}-{get_power}-{naprave}"
    print(f"Write to file {r}")
    with open("save.txt","w") as f:
        f.write(r)
    

number = 0
@app.route('/')
def main():
    with open("save.txt","r") as f:
        data = f.read()
    data = data.split("-")
    p_pc = data[0]
    p_table = data[1]
    vse_naprave = 0
    p = 0
    return render_template('index.html',p_pc = p_pc,p_table = p_table,naprave = vse_naprave,power = p)


if (__name__ == "__main__"):
    scheduler = APScheduler()
    scheduler.add_job(func=update_n, trigger='interval', id='job', seconds=10)
    scheduler.start()
    app.run(host="0.0.0.0", port=80, debug=False)

