from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserCreationForm
from django.contrib.auth import get_user
import socket, time, os, asyncio
from asgiref.sync import sync_to_async

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('Start:index')
    else:
        form = UserCreationForm()
    return render(request, 'common/signup.html', {'form': form})

def to_mainpage(request):
    return redirect('main:index')

def to_check_manual(request):
    return render(request, 'common/check_manual.html')

def check(request):
    asyncio.run(check_async(request))
    return redirect("main:index")

@sync_to_async
def mysocket(request):
    user = get_user(request)
    # 유저 정보와 시간 정보 저장 / 문자열 수정
    if user.is_authenticated:
        username = user.get_username()
    else:
        redirect("common:login")
    created_date = time.strftime('%Y-%m-%d-%H-%M-%S')
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
            with open(f"Data/{username}/{created_date}.txt", "w") as f:
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

async def check_async(request):
    await mysocket(request)  # mysocket 비동기 함수를 await로 호출하여 소켓 작업 수행
