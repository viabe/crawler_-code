import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
import openpyxl
import os
from konlpy.tag import *
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk-20\\bin"
# 한글 자연어 처리 모듈 선언
kkma = Kkma()
# 웹브라우저 객체 선언
browser = webdriver.Chrome()
# 엑셀 객체 선언
book= openpyxl.Workbook()
# 엑셀 빈 시트 생성
sheet = book.active
# 특정 뉴스 접근
browser.get("https://n.news.naver.com/article/032/0003230938?cds=news_media_pc&type=editn")
# 웹 페이지 렌더링 위한 묵시적 대기 5초
browser.implicitly_wait(5)
# 랜덤 시간 대기
time.sleep(random.randint(3,5))
# 댓글 더보기 무한 클릭
while True:
    try:
        # 댓글 더보기 버튼을 찾은 후 클릭
        u_cbox_btn_more = browser.find_element(By.CLASS_NAME, "u_cbox_btn_more")
        u_cbox_btn_more.click()
        # 네트워크 지연 위한 2초 대기
        time.sleep(2)
    except:
        # 댓글 더보기 버튼을 찾지 못하면 무한 반복 탈출
        break
# 댓글 번호 변수 선언
count = 1
for c_box in browser.find_elements(By.CLASS_NAME, "u_cbox_area"):    
    try:
        # 댓글
        contents = c_box.find_element(By.CLASS_NAME, "u_cbox_contents")
        print(kkma.pos(contents.text))
        input()
        # 사용자 닉네임
        nick = c_box.find_element(By.CLASS_NAME, "u_cbox_nick")
        # 댓글 작성일
        date_ = c_box.find_element(By.CLASS_NAME, "u_cbox_date")
        # 댓글 추천 수
        recomm = c_box.find_element(By.CLASS_NAME, "u_cbox_cnt_recomm")
        # 댓글 비추천 수
        unrecomm = c_box.find_element(By.CLASS_NAME, "u_cbox_cnt_unrecomm")        
        print(count, contents.text, nick.text, date_.text, recomm.text, unrecomm.text)
        # 시트에 댓글번호, 댓글, 작성자닉네임, 작성시각, 추천수, 비추천수
        sheet.append([count, contents.text, nick.text, date_.text, recomm.text, unrecomm.text])
    except Exception as e:
        pass
        
    count += 1
# 댓글 저장한 엑셀 파일 저장
book.save("result.xlsx")
# 엑셀파일 닫기
book.close()
# 브라우저 닫기
browser.close()