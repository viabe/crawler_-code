from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("https://www.naver.com")
time.sleep(5)
browser.save_screenshot("1111.png")