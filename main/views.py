from django.shortcuts import render,redirect
from django.contrib.auth import get_user
import os,time


def index(request):
    #텍스트 읽어서 첫번째 데이터 읽고 전송
    username=get_user(request).get_username()
    directory_path = f"Data/{username}"
    # 디렉토리가 없다면 측정페이지로 리디렉트
    if not os.path.exists(directory_path):
        return redirect('common:to_check')
    else:
        file_list=os.listdir(directory_path)
        txt= open(directory_path+'/'+file_list[-1],'r')
        value = txt.readlines() 
        for i in range(len(value)):
            value[i]=int(value[i].strip())
        txt.close()
        ## 두번째 데이터 전송
        val_list=[]
        if len(file_list)<5:
            file_list_size=len(file_list)
        else:
            file_list_size=5
        for i in range(file_list_size):
            txt = open(directory_path + '/' + file_list[-1*(i+1)],'r')
            value2 = txt.readlines() 
            for i in range(len(value2)):
                value2[i]=int(value2[i].strip())
            sum=0
            for i in range(5):
                max_val=max(value2)
                sum+=max_val
                value2.remove(max_val)
                avg = sum / 5
            val_list.append(avg)
        val_list=val_list[::-1] # 리스트 슬라이싱으로 순서 뒤집기

        context = {'value':value,'value2':val_list,'file_list':file_list[-6:-1]}
        return render(request,'main/mainpage.html',context)
    


        



    

    
# Create your views here.
