import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

# 엑셀 파일 생성
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "댓글"

browser = webdriver.Chrome()
browser.get("https://n.news.naver.com/mnews/article/comment/001/0014006478?sid=100")
browser.implicitly_wait(5)
time.sleep(random.randint(3, 5))

# 댓글 수집
row = 1
for c_box in browser.find_elements(By.CLASS_NAME, "u_cbox_area"):
    contents = c_box.find_element(By.CLASS_NAME, "u_cbox_contents")
    ws.cell(row=row, column=1, value=contents.text)
    row += 1

# 엑셀 파일 저장
wb.save("comments.xlsx")

# 셀레니움 브라우저 종료
browser.quit()