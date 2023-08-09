from selenium import webdriver
from selenium.webdriver.common.by import By
import time,random

options=webdriver.ChromeOptions()
options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
browser=webdriver.Chrome(options=options)
browser.get("https://www.naver.com")
browser.implicitly_wait(5)
time.sleep(random.randint(3,5))
for line in browser.find_element(By.XPATH,"/html/body").text.split("/n"):
    if len(line) ==0:
        continue
    print(line, len(line))
input()