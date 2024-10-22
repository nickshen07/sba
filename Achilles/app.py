from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from db import *
import sqlite3
import mysql.connector
from werkzeug.exceptions import HTTPException
import json
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

con = sqlite3.connect("demo.db")
cur = con.cursor()

def get_girl():
    return "https://pic.re/image?max_size=1023"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if 'reset' in request.form:
            with open("reset.txt", 'w') as f:
                f.write(datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%Y-%m-%d %H:%M:%S"))
            reset()
            return redirect('/')
        print(request.form)
        cont = request.form['con']
        det = request.form['det']
        opt = int(request.form['opt'])
        date = request.form['date']
        try:
            gg = (cont, det, opt, datetime.now().strftime("%Y-%m-%d"))
            print(gg)
            cur.execute("INSERT INTO Tasks (Name, Details, SID, DDate) VALUES (?, ?, ?, ?)", gg)
            cur.commit()
            tk = raww("SELECT MAX(TID) FROM Tasks")
            tk = tk[0][0]
            for i in request.form:
                if 'tag' in i:
                    tq = f"INSERT INTO TT (TkID, TgID) VALUES ({tk}, {request.form[i]})"
                    raw(tq)
            return redirect('/')
        except:
            return render_template('error.html', s="invalid input")
    else:
        setup()
        init()
        uncom = raww("SELECT * FROM Tasks WHERE SID = 1")
        doing = raww("SELECT * FROM Tasks WHERE SID = 2")
        com = raww("SELECT * FROM Tasks WHERE SID = 3")
        idk = raww("SELECT * FROM Tasks WHERE SID = 4")
        tags = raww("SELECT * FROM Tags")
        status = raww("SELECT * FROM Status")
        tt = raww("SELECT * FROM TT")
        with open("reset.txt", 'r') as f:
            last = f.read()
        return render_template('index.html', uncom = uncom, doing=doing, com = com, idk=idk, url=get_girl(), tags=tags, status=status, last=last, tt=tt)

@app.route('/delete/<int:id>')
def delete(id):
    query = f"DELETE FROM Tasks WHERE TID = {id}"
    try:
        raw(query)
        return redirect('/')
    except:
        return render_template('error.html', s="Task ID invalid")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        cont = request.form['con']
        det = request.form['det']
        opt = int(request.form['opt'])
        date = request.form['date']
        try:
            with sqlite3.connect("info.db") as con:
                cur = con.cursor()
                gg = (cont, det, opt, datetime.now().strftime("%Y-%m-%d"))
                print(gg)
                cur.execute("UPDATE Tasks SET Name = ?, Details = ?, SID = ?, DDate = ? WHERE TID = ?", gg)
                cur.execute("DELETE FROM TT WHERE TkID = ?", (id,))
                for i in request.form:
                    if 'tag' in i:
                        cur.execute("INSERT INTO TT (TkID, TgID) VALUES (?, ?)",(id, request.form[i]))
                cur.commit()
            return redirect('/')
        except:
            return "There was an error"
    else:
        item = raww(f"SELECT * FROM Tasks WHERE TID = {id}")
        status = raww("SELECT * FROM Status")
        item = item[0]
        tags = raww("SELECT * FROM Tags")
        tt = raww("SELECT * FROM TT")
        if len(item) == 0:
            return render_template('error.html', s="Task ID invalid")
        return render_template('update.html', item=item, status=status, tags=tags,tt=tt)

@app.errorhandler(HTTPException)
def handleError(err):
    return render_template('error.html', s=str(err.code)+" "+err.name+" "+err.description)



if __name__ == "__main__":
    app.run(debug=True)