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

def rjson():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

def wjson(data):
    with open("data.json", "w") as f:
        json.dump(data,f,indent=4)

def IndexGet():
    init()
    alt = raww("SELECT * FROM Tasks WHERE DueDate BETWEEN datetime('now', 'localtime') AND datetime('now','+7 day','localtime')")
    nstart = raww("SELECT * FROM Tasks WHERE SID = 1")
    doing = raww("SELECT * FROM Tasks WHERE SID = 2")
    com = raww("SELECT * FROM Tasks WHERE SID = 3")
    idk = raww("SELECT * FROM Tasks WHERE SID = 4")
    tags = raww("SELECT * FROM Tags")
    status = raww("SELECT * FROM Statuses")
    tt = raww("SELECT * FROM TaskTags")
    data = rjson()
    last = data["reset"]
    page = data["page"]
    return render_template('index.html', alt=alt, nstart = nstart, doing=doing, com = com, idk=idk, url=get_girl(), tags=tags, status=status, last=last, tt=tt, page=page)

def IndexPost(response):
    if 'reset' in response:
        data = rjson()
        data["reset"] = str(datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%Y-%m-%d %H:%M:%S"))
        wjson(data)
        reset()
        return redirect('/')
    if 'page' in response:
        data = rjson()
        c = response['page']
        print(c)
        if c == "Not started":
            num = 1
        elif c == "On-going":
            num = 2
        elif c == "Completed":
            num = 3
        elif c == "I don't know":
            num = 4
        else:
            num = 0
        data["page"] = num
        wjson(data)
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
                cur.execute("INSERT INTO TaskTags (TaskID, TagID) VALUES (?, ?)",(tk, int(response[i])))
        con.commit()
        return redirect('/')
    except:
        return render_template('error.html', s="invalid input")

def UpdatePost(response, id):
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

def UpdateGet(id):
    item = raww(f"SELECT * FROM Tasks WHERE TID = {id}")
    status = raww("SELECT * FROM Statuses")
    tags = raww("SELECT * FROM Tags")
    tt = raww("SELECT * FROM TaskTags")
    if len(item) == 0:
        return render_template('error.html', s="Task ID invalid")
    item = item[0]
    return render_template('update.html', item=item, status=status, tags=tags,tt=tt)

def TagPost(response):
    try:
        cur.execute("INSERT INTO Tags (Name) VALUES (?)", (response['tagname'],))
        return redirect('/tags')
    except:
        return render_template('error.html', s="There was an error")

def TagGet():
    item = raww("SELECT * FROM Tags")
    return render_template('tags.html', item=item)

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
        return UpdatePost(request.form, id)
    else:
        return UpdateGet(id)

@app.route('/deletetag/<int:id>')
def deletetag(id):
    try:
        raw(f"DELETE FROM Tags WHERE TID = {id}")
        return redirect('/tags')
    except:
        return render_template('error.html', s="Task ID invalid")

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    if request.method == 'POST':
        return TagPost(request.form)
    else:
        return TagGet()

@app.errorhandler(HTTPException)
def handleError(err):
    return render_template('error.html', s=str(err.code)+" "+err.name+" "+err.description)



if __name__ == "__main__":
    app.run(debug=True)