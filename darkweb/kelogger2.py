from pynput import keyboard #키보드 로깅용 모듈
from datetime import datetime #날짜 시간 함수. 캡처 시에 시간이 필요
import threading #쓰레드 모듈
#키보드 마우스 매크로 제어 모듈
import pyautogui
# 슬랩 함수를 위한 모듈
import time
import pygetwindow

box = pyautogui.locateAllOnScreen(".png")

print(box.left, box.top)

while True:
    print(pyautogui.position())
    print(pyautogui.moveTo(box.left, box.top))
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)

