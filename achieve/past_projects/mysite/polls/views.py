from django.http import HttpResponse
from django.template import loader

from .models import Question
import sqlite3

def index(request):
    lql = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in lql])
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'lql': lql,
    # }
    # return HttpResponse(template.render(context, request))
    with sqlite3.connect("tasks.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Task (name) VALUES ('ICT WB')")
        con.commit()
    return HttpResponse(output)

def detail(request, question_id):
    with sqlite3.connect("tasks.db") as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Task")
        con.commit()
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)