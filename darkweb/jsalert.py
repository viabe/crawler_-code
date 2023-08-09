from selenium import webdriver
import time
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
browser.get("https:/www.naver.com")
browser.implicitly_wait(5)
print(browser.window_handles)
shopping_button = browser.find_element(By.CLASS_NAME, "type_shopping")
shopping_button.click()
browser.implicitly_wait(5)
browser.switch_to.window(browser.window_handles[-1])


browser.find_element(By.CLASS_NAME, "category_image__1FzA8").click()
#print(browser.window_handles)

time.sleep(3)
for br in browser.window_handles:
    browser.switch_to.window(br)
    browser.close()
    time.sleep(2)

input()


browser.close()