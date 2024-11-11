from flask import Flask, render_template, request, redirect
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


"""
Modules
"""

def IndexGet():
    page=0
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

def IndexPost(response):
    if 'reset' in response:
        with open("reset.txt", 'w') as f:
            f.write(datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%Y-%m-%d %H:%M:%S"))
        reset()
        return redirect('/')
    if 'page' in response:
        page = response['page']
        return redirect('/')
    cont = response['con']
    det = response['det']
    opt = int(response['opt'])
    date = response['date']
    if cont == "":
        cont = "(no name)"
    try:
        para = ()
        if len(date) == 0:
            para = (cont, det, opt)
        else:
            para = (cont, det, opt, datetime.strptime(date, "%Y-%m-%dT%H:%M"))
        if len(date) == 0:
            cur.execute("INSERT INTO Tasks (Name, Details, SID) VALUES (?, ?, ?)", para)
        else:
            cur.execute("INSERT INTO Tasks (Name, Details, SID, DueDate) VALUES (?, ?, ?, ?)", para)
        con.commit()
        tk = raww("SELECT MAX(TID) FROM Tasks")
        tk = tk[0][0]
        for i in response:
            if 'tag' in i:
                cur.execute("INSERT INTO TaskTags (TaskID, TagID) VALUES (?, ?)",(tk, response[i]))
        return redirect('/')
    except:
        return render_template('error.html', s="invalid input")

def UpdatePost(response):
    cont = response['con']
    det = response['det']
    opt = int(response['opt'])
    date = response['date']
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
        for i in response:
            if 'tag' in i:
                cur.execute("INSERT INTO TaskTags (TaskID, TagID) VALUES (?, ?)",(id, response[i]))
        con.commit()
        return redirect('/')
    except:
        return render_template('error.html', s="There was an error")

def UpdateGet():
    item = raww(f"SELECT * FROM Tasks WHERE TID = {id}")
    status = raww("SELECT * FROM Statuses")
    tags = raww("SELECT * FROM Tags")
    tt = raww("SELECT * FROM TaskTags")
    if len(item) == 0:
        return render_template('error.html', s="Task ID invalid")
    item = item[0]
    return render_template('update.html', item=item, status=status, tags=tags,tt=tt)


"""
Interface
"""

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        return IndexPost(request.form)
    else:
        return IndexGet()

@app.route('/delete/<int:id>')
def delete(id):
    query = f"DELETE FROM Tasks WHERE TID = {id}"
    query2 = f"DELETE FROM TaskTags WHERE TaskID = {id}"
    try:
        raw(query)
        raw(query2)
        return redirect('/')
    except:
        return render_template('error.html', s="Task ID invalid")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        return UpdatePost(request.form)
    else:
        return UpdateGet()

@app.errorhandler(HTTPException)
def handleError(err):
    return render_template('error.html', s=str(err.code)+" "+err.name+" "+err.description)



if __name__ == "__main__":
    app.run(debug=True)