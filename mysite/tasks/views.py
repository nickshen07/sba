from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .models import Task

import sqlite3
import mysql.connector

class temp:
    name = ""
    label = ""
    status = False
    deadline = ""
    def __init__(self, a, b, c, d):
        self.name = a
        self.label = b
        self.status = c
        self.deadline = d

def home(request):
    query = "SELECT * FROM Task"
    # with connection.cursor() as cur:
    #     cur.execute(query)
    #     results = cur.fetchall()
    # print(type(results))
    
    with sqlite3.connect("tasks.db") as con:
        cur = con.cursor()
        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Task (
            taskid INTEGER PRIMARY KEY AUTOINCREMENT,
            title varchar(255) DEFAULT 'No-title' NOT NULL,
            label varchar(255),
            status BOOLEAN DEFAULT false,
            deadline DATETIME
        )
        """)
        res = cur.execute(query)
        res = res.fetchall()
        con.commit()
    nw = list()
    for i in res:
        l = temp(i[1], i[2],i[3],i[4])
        nw.append(l)
    print(nw)
    return render(request, 'home.html',{'list': res, 'nw':nw})

def add(request):
    if request.method == "POST":
        p = request.POST
        l = [p['title'], p['label'], (True if 'status' in p else False), p['deadline']]
        with sqlite3.connect("tasks.db") as con:
            cur = con.cursor()
            s = f"INSERT INTO Task (title, label, status, deadline) VALUES ('{l[0]}', '{l[1]}', {l[2]}, '{l[3]}')"
            print(s)
            cur.execute(s)
            con.commit()
        return render(request, 'add.html', {})
    else:
        return render(request, 'add.html', {})
    
def redir(request):
    return redirect('http://127.0.0.1:8000/home')

def delete(request):
    with sqlite3.connect("tasks.db") as con:
        cur = con.cursor()
        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Task (
            taskid INTEGER PRIMARY KEY AUTOINCREMENT,
            title varchar(255) DEFAULT 'No-title' NOT NULL,
            label varchar(255),
            status BOOLEAN DEFAULT false,
            deadline DATETIME
        )
        """)
        res = cur.execute("SELECT * FROM Task")
        res = res.fetchall()
        con.commit()
    if request.method == "POST":
        print(request.POST['status'])
        return render(request, 'delete.html', {'all': res})
    else:
        return render(request, 'delete.html', {'all': res})
    
def query(request):
    if request.method == "POST":
        p = request.POST
        l = p['name']
        with sqlite3.connect("tasks.db") as con:
            cur = con.cursor()
            print(l)
            cur.execute(l)
            con.commit()
        return render(request, 'query.html', {})
    else:
        return render(request, 'query.html', {})