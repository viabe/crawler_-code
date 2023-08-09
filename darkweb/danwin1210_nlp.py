
from stem.control import Controller
from stem import Signal
import requests, time, sqlite3, os, time
from bs4 import BeautifulSoup
import nltk
from datetime import datetime
from nltk.tokenize import word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
PROXIES = {
        "http" : "socks5h://127.0.0.1:9150",
        "https" : "socks5h://127.0.0.1:9150"    
}
# 데이터베이스 이름
DB_PATH = "darkweb9.db"
     
    
def getTorIp():
    # 토르 네트워킹을 위한 프록시 설정, protocol은 
    # socks5 - 로컬 이름 확인이 있는 SOCKS5를 의미합니다.
    # socks5h - 프록시 이름이 확인되는 SOCKS5를 의미합니다.
    # https://jung-max.github.io/2022/02/09/Linux-libcurl%20Proxies/
    # 현재 토르 네트워크의 아이피를 확인하기 위한 코드
    r = requests.get("http://ip-api.com/line", proxies = PROXIES)
    r.close()
    print(r.content.decode("utf-8").split("\n"))
    return r.content.decode("utf-8").split("\n")[-2].strip()
    
def torIpReset(before_ip):
    count = 1
    while True:
        ### 토르네트워크의 제어포트를 통해 tor network 리셋을 하여 ip를 다시 받는다.
        controller = Controller.from_port(port = 9151)
        controller.authenticate(password="1234")
        controller.signal(Signal.NEWNYM)        
        # 아이피가 바뀌였는지 여부를 다시 확인
        current_ip = getTorIp()
        print(count, before_ip, current_ip)
        if before_ip == current_ip:
            count += 1
            time.sleep(count)
            continue
        return current_ip

def getALinks(html, url):
    # 디비 파일에 접근
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    if ".onion" in url:        
        onion, uri = url.split(".onion")
        onion = onion + ".onion"
    else:
        onion = url.split("/")[2]
        uri = url.split("/")[-1]        
    datetime_ = datetime.now()
    print(onion, uri)
    # html 은 렌더링할 페잊
    # url 은 현재 요청한 페이지
    links = []
    # 뷰티풀숩을 이용하여 html을 분석
    soup = BeautifulSoup(html, "html.parser")    
    ### 해당 웹 페이지의 원소들을 전부 접근
    for element in soup.findAll():
        try:
            # 해당 원소에 텍스트 값을 추출
            text = element.text.strip()
            # 텍스트 길이가 0일 경우 다른 원소 접근
            if len(text) == 0:
                continue
            #print(word_tokenize(text))            
            # 해당 텍스트를 자연어처리
            for result in nltk.pos_tag(word_tokenize(text)):
                # 자연어 처리 결과를 데이터 베이스에 저장
                word, word_type = result
                if len(word) < 2:
                    continue
                sw = True
                for word_type_ in ["``", ":", "'", "$"]:
                    if word_type == word_type_:
                        sw = False
                if not sw:
                    continue
                if "/" in word:
                    for word_ in word.split("/"):
                        cursor.execute("INSERT INTO OnionPageWord values(?, ?, ?, ?, ?)", \
                                                        (onion, uri, word_, word_type, datetime_))
                else:
                    cursor.execute("INSERT INTO OnionPageWord values(?, ?, ?, ?, ?)", \
                                                        (onion, uri, word, word_type, datetime_))
        except Exception as e:
            print(e)
            pass
        
    src = url
    try:
        # 방문한 웹페이지의 title 을 src_title 에 저장합니다.
        src_title = soup.select_one('title').text    
    except:
        src_title = ""
    # HTML 에서 자식 링크들이 있는 A 태그들을 전부 요청합니다 
    for a in soup.find_all("a"):
        try:
            # href 변수에 A 태그의 href 속성값 즉 링크를 저장합니다.
            href = a["href"]
        except:
            continue
        # dst_text 는 링크의 text 값입니다
        dst_text = a.text
        if len(dst_text) == 0:
            dst_text = ""
        # 해당 href 가 onion 사이트이면 
        if href.endswith(".onion") or ".onion/" in href:
            print(src, src_title, href, dst_text)
            # OnionRelationship 테이블에 저장합니다.
            # 1. 요청한 URL 2. 요청한 URL의 TITLE 3. ONION 주소 4. ONION 주소의 TEXT
            cursor.execute("INSERT INTO OnionRelationiship values(?, ?, ?, ?)", \
                (src, src_title, href, dst_text))
            try:                
                # 또한 3. ONION 주소를 한번더 CrawlerTarget 에 저장합니다.
                # 예외처리를 한 이유는 기존 데이터베이스 테이블에 중복값이 있으며
                # 기본키 설정 때문에 중복된 값이 저장되지 않습니다.
                if ".onion" in href:
                    href_ = href.split(".onion")[0] + ".onion"                
                    cursor.execute("INSERT INTO CrawlerTarget values(?);", (href_,))
            except Exception as e:
                print(e)
                pass
            # 자식링크를 links 변수에 추가합니다.
            links.append(href)
        time.sleep(1)
    # 데이터베이스를 저장합니다.
    con.commit()
    con.close()
    return links

def getHTML(url, before_ip):
    print(url)
    while True:
        try:
            # 요청한 페이지를 방문
            r = requests.get(url, proxies = PROXIES)
            r.close()
            time.sleep(1)
            break
        except:
            # 토르 네트워크로 요청한 페이지를 방문하여 실패 했을 시 아이피를 변동 후 다시 토르 페이지를 방문
            before_ip = torIpReset(before_ip)
            
            continue
    ## 요청한 페이지의 HTML 을 분석하여 자식링크(href)들을 구하려고 아래의 getAlink 함수를 호출
    links = getALinks(r.content, url)
    print("\t", links)
    # 자식링크들(onion 주소들)을 반복 접근합니다.
    for link in links:
        while True:
            try:
                r_ = requests.get(link, proxies=PROXIES)
                r_.close()
                break
            except:
                before_ip = torIpReset(before_ip)
                continue
        
        links_ = getALinks(r_.content, link)
    
    
    
    # 요청된 html 파일을 저장합니다.
    file_name = url.split("?")[-1]
    fd = open(".\\html\\" + file_name + ".html", "wb")
    fd.write(r.content)
    fd.close()
    

def dbInit():
    # 데잍터베이스를 초기화
    # 기존 데이터베이스 파일이 존재하면 삭제
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    # sqlite3 용 데이터베이스를 생성
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    # 테이블을 생성
    # 1. CrawlerTarget 오니언 사이트만 담게됨
    # PRIMARY KEY 설정으로 중복된 값을 가질수 없음
    # 후에 이 테이블은 모니터링 대상이 되는 onion 사이트들만 담게 됨
    cursor.execute("CREATE TABLE CrawlerTarget(onion Text PRIMARY KEY);")
    # 2. OnionRelationship 테이블은 각 사이트별로 자식링크(a 태그의 href)를 구한 뒤
    # 요청된 페이지와 href 값의 관계를 저장하여 각 oninon 사이트별로 관계모델을 시각화 하고자 함
    # 후 graphviz 를 통해 시각화할 예정
    cursor.execute("CREATE TABLE OnionRelationiship(src Text, src_title Text, dst Text, dst_text Text);")
    # 3. OnionPageWord
    # 요청 후 해당 사이트에 있는 단어들을 추출 후 디비에 저장
    # onion 은 해당 사이트 나머지 주소와 파라미티러를 uri 에 저장, 단어는 word 에 저장
    cursor.execute("CREATE TABLE OnionPageWord(onion Text, uri Text, word Text, type Text, timestamp DATETIME);")
    
    con.close()    
    
# 여기에서 코드시작
dbInit()
before_ip = getTorIp()        
cat = 1 
while True:
    # danin1210.de 사이트를 cat 값을 21번이 되기까지 해당 페이지에 방문
    url = "https://onions.danwin1210.de/?cat=" + str(cat) + "&pg=0"
    # getHTML 을 cat 1~21 까지 접근
    getHTML(url, before_ip)
    cat += 1
    if cat > 21:
        break