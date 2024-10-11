from django.shortcuts import render
from django.http import HttpResponse
import requests
import sys
sys.path.insert(1, '/home/student/ICT_SBA/')
import main

# Create your views here.
# request -> response
# request handler
# action

def home_view(request, *args, **kwargs):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
    url = "https://www.dse00.com/"
    s = requests.get(url).text
    s1 = s[s.index("<div class=\"sentence_quote\">"):]
    s1 = s1[28:]
    s1 = s1[:s1.index("</div>")]
    context = {
        'main': main.menu,
        'sentence': s1,
    }
    return render(request, 'home.html',context)

def get_view(request,*args, **kwargs):
    # Pull data from db
    # Transform
    # Send email
    return render(request, 'ai.html',{})
