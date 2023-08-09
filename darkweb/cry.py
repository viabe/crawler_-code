from cryptos import *
c = Bitcoin()
### 지갑 설정
### 기억하기 쉬은 단어를 통해 지갑 주소를 만든다
import hashlib
#개인키
priv = hashlib.sha256('kisia 2023-06-02'.encode('utf-8')).hexdigest()
#공개키
pub = c.privtopub(priv)
#지갑 주소
addr = c.pubtoaddr(pub)
print(addr)