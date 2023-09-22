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
            user = authenticate(username=username, password=raw_password)
            if user is not None and user.is_authenticated:
                login(request, user)
            else:
                return render(request, 'common/signup.html', {'form': form})
             # 로그인
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
    server_ip = "http://ec2-15-164-94-66.ap-northeast-2.compute.amazonaws.com"
    server_port = 8080
    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 소켓을 지정한 IP 주소와 포트에 바인딩
    sock.bind((server_ip, server_port))
    print(f"Checking attempted by {username} in {created_date}")
    print(f"Listening for UDP packets on {server_ip}:{server_port}")

    # 데이터 저장 상태
    data_list = []
    count=0 # 루프를 벗어나기 위한 변수 정의

    try:
        while (True):
            # 데이터를 수신
            data, addr = sock.recvfrom(1024)
            decoded_data = data.decode('utf-8')
            if decoded_data == "start":
                data_list = []  # 리스트 초기화
                continue
            elif count>=5:
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
            elif int(decoded_data)>500:
                count+=1
            
            data_list.append(decoded_data)

            print(f"Received data from {addr}: {decoded_data}")

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Stopping the check.")
        sock.close()


async def check_async(request):
    await mysocket(request)
