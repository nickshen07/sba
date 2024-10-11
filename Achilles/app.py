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

def get_meme():
    url = "https://meme-api.com/gimme"
    res = json.loads(requests.request("GET", url).text)
    return res['url']

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        if 'reset' in request.form:
            reset()
            return redirect('/')
        task_content = request.form['content']
        b = 1 if 'status' in request.form else 0
        query = f"INSERT INTO Tasks (Name, Status) VALUES ('{task_content}', {b})"
        try:
            setup()
            raw(query)
            return redirect('/')
        except:
            return render_template('error.html', s="invalid input")
    else:
        uncom = raww("SELECT * FROM Tasks WHERE Status = 0")
        com = raww("SELECT * FROM Tasks WHERE Status = 1")
        return render_template('index.html', uncom = uncom, com = com, url= get_meme())

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