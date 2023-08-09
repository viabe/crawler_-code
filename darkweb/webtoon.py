from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import random

num = 50
# 셀레니움 브라우저 객체 생성
browser = webdriver.Chrome()

# 이미지 저장을 위한 폴더 생성
if not os.path.exists("images"):
    os.makedirs("images")

# 웹툰을 1화부터 끝까지 찾고자 함
# 웹툰의 끝은 해당 회차를 방문 후 요청환 url과 브라우저상의 current_url을 비교
while True:
    # titleId 웹툰 종류 no 값은 각 회차를 구분
    url = "https://comic.naver.com/webtoon/detail?titleId=796152&no=" + str(num)
    browser.get(url)
    browser.implicitly_wait(5)
    time.sleep(random.randint(3, 5))
    # 웹툰의 마지막화를 찾기 위한 비교
    if browser.current_url != url:
        break

    webtoon_title = browser.find_element(By.ID, "titleName_toolbar")
    title = browser.find_element(By.ID, "subTitle_toolbar")
    for index, a in enumerate(browser.find_elements(By.TAG_NAME, "img")):
        img_src = a.get_attribute("src")
        if not img_src.startswith("https://image-comic."):
            continue

        # 이미지 다운로드
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(img_src, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"이미지 다운로드 실패: {e}")
            continue

        image_name = f"{webtoon_title.text}_{title.text}_{num}_{index+1}.jpg"
        image_path = os.path.join("images", image_name)
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"이미지 저장 완료: {image_path}")

    num += 1

# 셀레니움 브라우저 종료
browser.quit()