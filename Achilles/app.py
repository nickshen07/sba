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

con = sqlite3.connect('info.db',
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES,check_same_thread=False)
cur = con.cursor()


def get_girl():
    return "https://pic.re/image?max_size=1023"

@app.route('/', methods=['POST', 'GET'])
def index():
    page=0
    if request.method == "POST":
        if 'reset' in request.form:
            with open("reset.txt", 'w') as f:
                f.write(datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%Y-%m-%d %H:%M:%S"))
            reset()
            return redirect('/')
        if 'page' in request.form:
            page = request.form['page']
            return redirect('/')
        print(request.form)
        cont = request.form['con']
        det = request.form['det']
        opt = int(request.form['opt'])
        date = request.form['date']
        if cont == "":
            cont = "(no name)"
        try:
            gg = ()
            if len(date) == 0:
                gg = (cont, det, opt)
            else:
                gg = (cont, det, opt, datetime.strptime(date, "%Y-%m-%dT%H:%M"))
            if len(date) == 0:
                cur.execute("INSERT INTO Tasks (Name, Details, SID) VALUES (?, ?, ?)", gg)
            else:
                cur.execute("INSERT INTO Tasks (Name, Details, SID, DueDate) VALUES (?, ?, ?, ?)", gg)
            con.commit()
            tk = raww("SELECT MAX(TID) FROM Tasks")
            tk = tk[0][0]
            for i in request.form:
                if 'tag' in i:
                    cur.execute("INSERT INTO TaskTags (TaskID, TagID) VALUES (?, ?)",(tk, request.form[i]))
            return redirect('/')
        except:
            return render_template('error.html', s="invalid input")
    else:
        setup()
        init()
        alt = raww("SELECT * FROM Tasks WHERE DueDate BETWEEN datetime('now', 'localtime') AND datetime('now','+7 day','localtime')")
        nstart = raww("SELECT * FROM Tasks WHERE SID = 1")
        doing = raww("SELECT * FROM Tasks WHERE SID = 2")
        com = raww("SELECT * FROM Tasks WHERE SID = 3")
        idk = raww("SELECT * FROM Tasks WHERE SID = 4")
        tags = raww("SELECT * FROM Tags")
        status = raww("SELECT * FROM Statuses")
        tt = raww("SELECT * FROM TaskTags")
        with open("reset.txt", 'r') as f:
            last = f.read()
        return render_template('index.html', alt=alt, nstart = nstart, doing=doing, com = com, idk=idk, url=get_girl(), tags=tags, status=status, last=last, tt=tt, page=page)

@app.route('/delete/<int:id>')
def delete(id):
    query = f"DELETE FROM Tasks WHERE TID = {id}"
    query2 = f"DELETE FROM TaskTags WHERE TID = {id}"
    try:
        raw(query)
        raw(query2)
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
        if cont == "":
            cont = "(no name)"
        try:
            gg = ()
            if len(date) == 0:
                gg = (cont, det, opt, id)
                cur.execute("UPDATE Tasks SET Name = ?, Details = ?, SID = ? WHERE TID = ?", gg)
            else:
                gg = (cont, det, opt, datetime.strptime(date, "%Y-%m-%dT%H:%M"), id)
                cur.execute("UPDATE Tasks SET Name = ?, Details = ?, SID = ?, DueDate = ? WHERE TID = ?", gg)
            cur.execute("DELETE FROM TaskTags WHERE TaskID = ?", (id,))
            for i in request.form:
                if 'tag' in i:
                    cur.execute("INSERT INTO TaskTags (TaskID, TagID) VALUES (?, ?)",(id, request.form[i]))
            con.commit()
            return redirect('/')
        except:
            return render_template('error.html', s="There was an error")
    else:
        item = raww(f"SELECT * FROM Tasks WHERE TID = {id}")
        status = raww("SELECT * FROM Statuses")
        tags = raww("SELECT * FROM Tags")
        tt = raww("SELECT * FROM TaskTags")
        if len(item) == 0:
            return render_template('error.html', s="Task ID invalid")
        item = item[0]
        return render_template('update.html', item=item, status=status, tags=tags,tt=tt)

@app.errorhandler(HTTPException)
def handleError(err):
    return render_template('error.html', s=str(err.code)+" "+err.name+" "+err.description)



if __name__ == "__main__":
    app.run(debug=True)