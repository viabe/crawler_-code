from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess

subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe --remote-debugging-port=9222")
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
browser = webdriver.Chrome(options=chrome_options)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
        {"source" : """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
'''
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(options=options)

browser.get("https://www.naver.com")
time.sleep(5)
input()
browser.close()