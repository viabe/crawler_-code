from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3, random


app = Flask(__name__)

# 클라이언트가 요청 => 나 크롤링 할 onion 사이트를 주세요
# 서버는 요청에 따라 랜덤한 onion 사이트를 리턴

@app.route("/getOnion", methods=["GET"])
def getOnion():
    # 2. 클라이언트가 요청함에 따라 아래에 코드가 동작
    # darkweb10.db 파일을 접근 후 커서를 얻는다.
    con = sqlite3.connect("darkweb10.db")
    cursor = con.cursor()
    # select 구문을 통해 status 가 0인 onion row 를 얻는다.
    # status 0 은 가용할 수 있는 즉, 다른 크롤러가 요청해서 수행중이지 않은 상태를 의미한다.
    cursor.execute("select * from CrawlerTarget where status == 0")
    # 아래 코드는 랜덤한 onion 사이트를 구하는 과정
    rowList = cursor.fetchall()
    if len(rowList) == 0:
        ## 서버의 응답에 onion 을 답해줄수 없을때 404 에러
        return "0", 404
    # 랜덤함수 통해 여러 행중 랜덤한 행을 선택
    row = random.choice(rowList)
    # row 의 각 열에 해당하는 값을 접근
    onion = row[0]
    count = row[1]
    lastdate = row[2]
    status = row[3]
    print(onion, count, lastdate, status)
    # 해당 onion을 다른 크롤러가 선점해서 크롤링 하지 못하게 하기 위해 해당 onion 의 status 값을 1로 셋팅
    cursor.execute("update CrawlerTarget set status = 1 where onion = '%s'" % (onion))
    con.commit()     
    con.close()
    # onion 값을 리턴
    return onion, 200

@app.route("/setOnionResult", methods=["POST"])
def setOnionResult():
    # 클라이언트로 부터 받은 json 데이터를 onion, onion_list, relationship_list, uri_list 로 각각 담게된다.
    onion = request.json["onion"]
    onion_list = request.json["onion_list"]
    relationship_list = request.json["relationship_list"]
    uri_list = request.json["uri_list"]
    # sqlite 파일에 접근
    con = sqlite3.connect("darkweb10.db")
    cursor = con.cursor()
    # 다른 크롤러가 선점하지 못하게 하기 위해 onion 사이트의 status 값을 0으로 하여 다른 사이트가 받을 수 있을 준비를 한다.
    cursor.execute("update CrawlerTarget set status = 0 where onion = '%s'" % (onion))
    # onion_list 에는 순수한 onion 주소로만 되어 있는 데이터들이 존재 그 값들을 각각 CrawlerTarget 에 저장
    for onion_ in onion_list:
        try:
            # 예외처리 하는 이유는 onion 컬럼이 PRIMARY_KEY 상태이기 때문에 중복된 값을 저장할 수 없게 처리 하기 위함
            cursor.execute("INSERT INTO CrawlerTarget values(?, ?, ?, ?)", (onion_, 0, datetime.today(), 0))
        except:
            pass
    # 사이트별 관계도를 저장하기 위해 relationship_list 를 각각 접근
    for relationship in relationship_list:
        # relationship 을 저장하기 위해 각 데이터를 선언
        src = relationship[0]
        src_title = relationship[1]
        href = relationship[2]
        dst_text = relationship[3]
        # 사이트별 관계도를 db 에 저장함
        cursor.execute("INSERT INTO OnionRelationiship values(?, ?, ?, ?)", \
                (src, src_title, href, dst_text))     
    # 파라미터 전체 정보가 담겨진 uri_list 를 각각 접근
    for uri in uri_list:
        # domain 에는 onion 주소가
        domain = uri[0]
        # uri 에는 파라미터가 저장되어있음
        uri_ = uri[1]
        # 파라미터가 담긴 전체데이터를 onionuri 에 저장
        cursor.execute("INSERT INTO OnionUri values(?, ?)", \
                (domain, uri_))
    con.commit()
    con.close()    
    return onion, 200

@app.route("/getOnionUri", methods=["GET"])
def getOnionUri():
    con = sqlite3.connect("darkweb10.db")
    cursor = con.cursor()
    while True:
        cursor.execute("select * from OnionUri")
        rowList = cursor.fetchall()
        if len(rowList) == 0:
            return "0", 404
        row = random.choice(rowList)
        onion = row[0]
        uri = row[1]
        if len(uri) < 2:
            continue
        break
    onion_uri = onion + uri
    con.commit()     
    con.close()
    print(onion_uri)
    return onion_uri, 200




@app.route("/setOnionUriResult", methods=["POST"])
def setOnionUriResult():
    '''
    for key, value in request.json.items():
        print(key, value, type(value))
    '''
    # 파라미터가 포함된 데이터를 onion_uri 에 정의
    onion_uri = request.json["onion_uri"]
    # 데이터 베이스에 접근
    con = sqlite3.connect("darkweb10.db")
    cursor = con.cursor()
    if isinstance(request.json["word_list"], str):
        # word_list 값을 \n 각 라인별로 출력
        for word in request.json["word_list"].split("\n"):
            # 해당 라인을 strip(왼, 오른 공백제거)
            word = word.strip()
            # 해당 word 길이가 0이면 무시
            if len(word) == 0:
                continue
            # 해당 word 를 데이터 베이스에 담는다.
            cursor.execute("INSERT INTO OnionWord values(?, ?)", (onion_uri, word))
    elif isinstance(request.json["word_list"], list):
        for word in request.json["word_list"]:
            continue
    con.commit()
    con.close()
    return "", 200
    onion = request.json["onion"]
    onion_list = request.json["onion_list"]
    relationship_list = request.json["relationship_list"]
    uri_list = request.json["uri_list"]
    con = sqlite3.connect("darkweb10.db")
    cursor = con.cursor()
    cursor.execute("update CrawlerTarget set status = 0 where onion = '%s'" % (onion))
    for onion_ in onion_list:
        try:
            cursor.execute("INSERT INTO CrawlerTarget values(?, ?, ?, ?)", (onion_, 0, datetime.today(), 0))
        except:
            pass
    for relationship in relationship_list:
        src = relationship[0]
        src_title = relationship[1]
        href = relationship[2]
        dst_text = relationship[3]
        cursor.execute("INSERT INTO OnionRelationiship values(?, ?, ?, ?)", \
                (src, src_title, href, dst_text))     
    for uri in uri_list:
        domain = uri[0]
        uri_ = uri[1]
        cursor.execute("INSERT INTO OnionUri values(?, ?)", \
                (domain, uri_))
    con.commit()
    con.close()    
    return onion, 200




    
if __name__ == "__main__":
    con = sqlite3.connect("darkweb10.db")
    cursor = con.cursor()
    cursor.execute("update CrawlerTarget set status = 0")
    con.commit()
    con.close()
        
    app.run(debug=True, host="0.0.0.0", port=8080)