from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import get_user
import socket, time, os


def check(request):
    user= get_user(request)
    #유저 정보와 시간 정보 저장 / 문자열 수정
    if user.is_authenticated:
        username=user.get_username()
    else:
        redirect("common:login")
    created_date=time.strftime('%Y-%m-%d-%H-%M-%S')
    # 서버의 IP 주소와 포트 번호 설정
    server_ip = "192.168.0.72"
    server_port = 8080
    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 소켓을 지정한 IP 주소와 포트에 바인딩
    sock.bind((server_ip, server_port))
    print(f"Checking attempted by {username} in {created_date}")
    print(f"Listening for UDP packets on {server_ip}:{server_port}")

    # 데이터 저장 상태
    save_data = False
    data_list = []
    while True:
        # 데이터를 수신
        data, addr = sock.recvfrom(1024)
        decoded_data = data.decode('utf-8')

        if decoded_data == "start":
            save_data = True
            data_list = []  # 리스트 초기화
            continue
        
        if decoded_data == "finish":
            save_data = False
            # 디렉토리를 자동으로 생성하고 측정된 데이터를 파일에 저장
            directory_path = f"Data/{username}"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            with open(f"Data/{username}/EMG_Data+{created_date}.txt", "w") as f:
                for item in data_list:
                    f.write(f"{item}\n")
            print("Check Completed and Data saved.")
            print("Checking Server stopped.")
            sock.close()
            break

        # "start"와 "finish" 사이의 데이터를 data_list에 저장
        if save_data:
            data_list.append(decoded_data)

        print(f"Received data from {addr}: {decoded_data}")




def index(request):
    #측정하는 UDP 서버 실행
    check(request)
    #Data/{username}에 있는 파일을 시간순으로 정렬
    
    #텍스트 읽어서 전송
    txt= open('static/test.txt','r')
    value = txt.readlines() 
    value = list(map(lambda s: float(s.strip()), value))
    txt.close()
    context = {'value':value}
    return render(request,'main/mainpage.html',context)
    


        



    

    
# Create your views here.
