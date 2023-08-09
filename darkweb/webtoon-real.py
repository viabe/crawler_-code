from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image

import time
import requests
import os
import random
num = 1
headers ={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
# 셀레니움 브라우저 객체 생성
browser = webdriver.Chrome()
# 웹툰을 1화부터 끝까지 찾고자함
# 웹툰의 끝은 해당 회차를 방문후 요청환 url 과 브라우저상의 current_url을 비교 
while True:
    # titleId 웹툰 종류 no 값은 각 회차를 구분
    url = "https://comic.naver.com/webtoon/detail?titleId=796152&no=" + str(num)
    browser.get(url)    
    browser.implicitly_wait(5)
    time.sleep(random.randint(3,5))
    # 웹툰의 마지막화를 찾기 위한 비교    
    if browser.current_url != url:
        break
    webtoon_title = browser.find_element(By.ID, "titleName_toolbar")
    title = browser.find_element(By.ID, "subTitle_toolbar")
    sub_num = 1
    print(webtoon_title.text, title.text)
    os.mkdir(webtoon_title.text + " " +  title.text)
    for a in browser.find_elements(By.TAG_NAME, "img"):
        img_src = a.get_attribute("src")
        if not img_src.startswith("https://image-comic."):
            continue
        response = requests.get(img_src, headers=headers)
        response.close()
        time.sleep(random.randint(3, 5))
        #print(response.content, response.headers)
        fd = open(".\\" + webtoon_title.text + " " + title.text + "\\" \
            + webtoon_title.text + "_" + title.text + " " + str(sub_num) + ".png", "wb")
        fd.write(response.content)
        fd.close()
        sub_num += 1
    num += 1
    