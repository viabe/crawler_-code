# 셀레니움 웹드라이버 모듈
from selenium import webdriver
# 셀레니움 웹드라이버에서 WebElement 를 찾기위한 객체 By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# 사이트 로딩 후 랜덤시간 기다리기 위한 랜덤 함수
import random, time, pyperclip
# 브라우저 객체 호출
browser = webdriver.Chrome()
# 브라우저를 주소창을 통해 로그인 페이지 접근
browser.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
# 브라우저 묵시적 대기
browser.implicitly_wait(5)
# 랜덤시간 대기
time.sleep(random.randint(3, 5))
# 웹 페이지에서 id, pw 입력창 찾고 kisia 값 입력 후 랜덤시간 대기
id_ = browser.find_element(By.NAME, "id")
#id_.send_keys("kisia_test")
pyperclip.copy("kisia_test")
id_.send_keys(Keys.CONTROL, 'v')
time.sleep(random.randint(1, 2))
pw = browser.find_element(By.ID, "pw")
#pw.send_keys("kisia_test1234")
pyperclip.copy("kisia_test1234")
pw.send_keys(Keys.CONTROL, 'v')
time.sleep(random.randint(1, 2))
# 로그인 버튼을 xpath로 찾고 클릭
login_button = browser.find_element(By.XPATH, '//*[@id="log.login"]')
login_button.click()


input()
browser.close()