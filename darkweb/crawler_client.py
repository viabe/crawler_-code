import requests
from bs4 import BeautifulSoup
while True:
    # 1. 클라이언트가 서버의 getOnion 에 접근하여 onion 페이지를 요청한다.
    response = requests.get("http://192.168.0.153:8080/getOnion")
    # 3. 요청 한 네트워크 소켓을 닫느다.
    response.close()
    # 서버의 응답페이지(resposne body)를 html 변수로 담는다.
    onion = response.content.decode("utf-8")
    print(onion)
    # onion 주소가 .onion 으로 끝나거나 http//: 또는 https:// 로 시작하는 경우 크롤링의 대상으로 선정
    if onion.endswith(".onion") and (onion.startswith("http://") or onion.startswith("https://")):
        # 토르 프록시를 설정
        PROXIES = {
            "http" : "socks5h://127.0.0.1:9150",
            "https" : "socks5h://127.0.0.1:9150"    
        }
        # 아래 tmp_list 는 후에 onion 사이트들만 중복되지 않는 값들만 담기위해 리스트를 선언
        tmp_list = []
        # href 를 통해 자식링크들을 구하고 관계를 표현하기 위해 리스트를 선언
        relationship_list = []
        # href 를 통해 파라미터 전체를 포함한 값들을 담기위해 리스트를 선언
        uri_list = []
        # 크롤링을 위한 tor 네트워크로 onion 주소 크롤링
        response = requests.get(onion, proxies= PROXIES)        
        html = response.content
        response.close()
        # 서버의 상태값을 구한다.
        print(response.status_code)
        # html을 Beautifulsoup 을 통해 파싱한다.
        soup = BeautifulSoup(html, "html.parser")
        src = onion
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
                # 파라미터가 있을경우 순수한 onion 주소만 설정
                href_ = href.split(".onion")[0] + ".onion"
                # 만약 onion 사이트가 tmp_list 에 없다면
                if href_ not in tmp_list:
                    # 사이트별 관계를 표현하기 위해 relationship 을 설정
                    relationship = [src, src_title, href_, dst_text]
                    print(src, src_title, href_, dst_text)
                    # tmp_list 에 onion 사이트만 담는다
                    tmp_list.append(href_)
                    # relationship_list 에는 사이트별 관계가 담기게 된다.
                    relationship_list.append(relationship)
            # 아래는 파라미터를 포함한 주소를 저장하기 위함
            if ".onion" in href:
                # 도메인 주소를 구함
                domain = href.split(".onion")[0] + ".onion"
                # 파라미터를 구함
                uri = href.split(".onion")[1]
                # 서버에 전송할 onion_uri 를 uri_list 에 담는다.
                uri_list.append([domain, uri])
        
        #src_url , src_title, dst_onion, dst_onion_text
        # 서버에 전송할 리포트 데이터를 json 형태로 선언        
        d = {
            "onion" : onion,
            "onion_list" : tmp_list,
            "relationship_list" : relationship_list,
            "uri_list" : uri_list
        }
        # 서버에 post 메소드로 json 형태로 리포트 전송
        response = requests.post("http://192.168.0.153:8080/setOnionResult", json = d)
        response.close()
