### flask 모듈의 Flask 웹 프레임워크와, 클라이언트 요청에 대한 객체 request
###미리 임포트 함
from flask import Flask, request, jsonify
#플라스크 객체 생겅
app = Flask(__name__)

#디렉토리 경로 설정과 허용하고자 하는 메서드를 정의
@app.route("/kisia", methods = ["GET","POST"])
#실제 동작하는 함수
def Kisia():
    #클라이언트의 요청 객체
    print(request.headers)
    print(request.data)
    #리턴 값은 kisia 200 ok
    return "kisia", 200

if __name__ =="__main__":
    #app.run 통해 웹을 구동
    #debug 디버깅 메세지 출력
    #host = 접근허용 아이피 대역 0.0.0.0 모든 아이피 허용 
    #port = 서비스 하고자하는 tcp 80000
    app.run(debug=True,host="0.0.0.0", port=8000)
