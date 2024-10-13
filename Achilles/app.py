from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from db import *
import sqlite3
import mysql.connector
from werkzeug.exceptions import HTTPException
import json
import requests

app = Flask(__name__)

def get_girl():
    return "https://pic.re/image?max_size=1023"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if 'reset' in request.form:
            reset()
            return redirect('/')
        print(request.form)
        con = request.form['con']
        det = request.form['det']
        opt = request.form['opt']
        date = request.form['date']
        query = f"INSERT INTO Tasks (Name, Details, SID, DDate) VALUES ('{con}', '{det}', {opt}, '{date}')"
        print(query)
        try:
            raw(query)
            return redirect('/')
        except:
            return render_template('error.html', s="invalid input")
    else:
        setup()
        init()
        uncom = raww("SELECT * FROM Tasks WHERE SID <> 2")
        com = raww("SELECT * FROM Tasks WHERE SID = 2")
        tags = raww("SELECT * FROM Tags")
        status = raww("SELECT * FROM Status")
        return render_template('index.html', uncom = uncom, com = com, url=get_girl(), tags=tags, status=status)

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
        b = 1 if 'status' in request.form else 0
        query = f"UPDATE Tasks SET Name = '{request.form['content']}', Status = {b} WHERE TID = {id}"
        try:
            raw(query)
            return redirect('/')
        except:
            return "There was an error"
    else:
        item = raww(f"SELECT * FROM Tasks WHERE TID = {id}")
        if len(item) == 0:
            return render_template('error.html', s="Task ID invalid")
        item = item[0]
        return render_template('update.html', item=item)

@app.errorhandler(HTTPException)
def handleError(err):
    return render_template('error.html', s=str(err.code)+" "+err.name+" "+err.description)



if __name__ == "__main__":
    app.run(debug=True)