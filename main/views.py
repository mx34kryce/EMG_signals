from django.shortcuts import render
from django.conf import settings
from django.utils import timezone


def index(request):
    txt= open('static/test.txt','r')
    value = txt.readlines() 
    value = list(map(lambda s: float(s.strip()), value))
    txt.close()
    context = {'value':value}
    return render(request,'main/mainpage.html',context)
    


        



    

    
# Create your views here.
