from django.shortcuts import render,redirect
from django.contrib.auth import get_user
import os,natsort


def index(request):
    #텍스트 읽어서 첫번째 데이터 전송
    user=get_user(request)
    username=user.get_username()
    directory_path = f"Data/{username}"
    list=os.listdir(directory_path)
    txt= open(directory_path+'/'+list[-1],'r')
    value = txt.readlines() 
    for i in range(len(value)):
        value[i]=int(value[i].strip())
    txt.close()
    context = {'value':value}
    return render(request,'main/mainpage.html',context)
    


        



    

    
# Create your views here.
