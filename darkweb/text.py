from bs4 import BeautifulSoup
import requests
def getLinksFromUrl(url, depth):
    headers = {
        "User-Agent" : "Android"
    }
    naver_response = requests.get(url, headers=headers)
    naver_response.close()
    
    soup = BeautifulSoup(naver_response.content, "html.parser")
    links = []
    for text in soup.findAll(text=True):
        
        if len(text) == 1 and (ord(text) == 10 or ord(text) == 32 or ord(text) == 160):
            continue
        print(text.strip(), len(text))
        
getLinksFromUrl("https://www.naver.com", 0)