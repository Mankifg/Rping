from flask import Flask,render_template,url_for,request,redirect, make_response
from flask_apscheduler import APScheduler
import datetime
import random
from ping import fromiplisttoonlinecomputers

app = Flask(__name__)

def update_n():
    number = fromiplisttoonlinecomputers()
    with open("save.txt","w") as f:
        f.write(str(number))

number = 0
@app.route('/', methods=["GET", "POST"])
def main():
    with open("save.txt","r") as f:
        number = f.read()

    print(number)
    return render_template('index.html',number = number)


if (__name__ == "__main__"):
    scheduler = APScheduler()
    scheduler.add_job(func=update_n, trigger='interval', id='job', seconds=10)
    scheduler.start()
    app.run(host="0.0.0.0", port=80, debug=False)

