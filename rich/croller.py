import requests
import datetime
from bs4 import BeautifulSoup
import random


def convert_date_str_to_ts(date_str):
    #date_str format 'YYYY/MM/DD'

    #연도, 달, 날이 배열에 맞춰서 들어가게 됨
    year , month, day = [ int(date_info)  for date_info in date_str.split("/")]
    dtime = datetime.datetime(year,month,day)
    ts = int(dtime.timestamp())
    return ts


#부모 클래스
class InfoCrawler():

    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list =[
            #Chrome
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        	#Firefox
        	'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]

    #랜덤으로 헤더에 리퀘스트 하기
    def set_random_user_agent(self):
        user_agent = random.choice(self.user_agent_list)
        self.headers['User-Agent'] = user_agent
        return user_agent

    #데이터를 가져오는 함수
    def get_result_data(self, *args, **kwargs):
        pass
    
    #페이지 가져오기
    def parse_page(self, raw_response):
        pass



#야후 종목 정보 가져올것
class YahooinanceCrawle(InfoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://query2.finance.yahoo.com/v8/finance/chart/{}?interval=1d&period1={}&period2={}"
        self.set_random_user_agent()
        

    #랜덤으로 헤더에 리퀘스트 하기, 없어도 됨

    #데이터를 가져오는 함수
    def get_result_data(self, target_code, from_data_str, to_data_str):
        from_ts = convert_date_str_to_ts(from_data_str)
        to_ts = convert_date_str_to_ts(to_data_str)
        target_url = self.base_url.format(target_code, from_ts, to_ts)
        res = requests.get(target_url, headers=self.headers)
        res_list = self.parse_page(res)
        return res_list

    def parse_page(self, raw_response):
        #print(raw_response.text)
        
        res_list =[]
        #딕셔너리
        res_json = raw_response.json()
        ts_list = res_json["chart"]["result"][0]["timestamp"] #chart 배열의 result 배열의 timestamp만 나옴
        price_dict = res_json["chart"]["result"][0]["indicators"]["quote"][0]
        #print(price_dict)

#컨트롤 + 알트 아래 방행키 / 쉬프트 + 알트하고 복사하기
        open_price_dict = price_dict["open"]
        close_price_dict= price_dict["close"]
        high_price_dict= price_dict["high"]
        low_price_dict= price_dict["low"]

        for ts, open_price, close_price, high_price,low_price in zip(ts_list, open_price_list, close_price_list, high_price_list, low_price_list):
            info_dict = {
                "ts":ts,
                "open_price": open_price,
                "close_price": close_price,
                "high_price": high_price,
                "low_price": low_price,

            }
            print(info_dict)

            res_list.append(info_dict)
        return res_list




#네이버 종목 정보 가져올것
class NaverinanceCrawler(InfoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://finance.naver.com/"
        

    #랜덤으로 헤더에 리퀘스트 하기
    def set_random_user_agent(self):
        pass

    #데이터를 가져오는 함수
    def get_result_data(self, *args, **kwargs):
        pass

    def parse_page(self, raw_response):
        pass



class MarketBuyerInfoCrawler(NaverinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = ""
        

    #랜덤으로 헤더에 리퀘스트 하기
    def set_random_user_agent(self):
        pass

    #데이터를 가져오는 함수
    def get_result_data(self, *args, **kwargs):
        pass

    def parse_page(self, raw_response):
        pass

#객체
yfc = YahooinanceCrawle()
result_list = yfc.get_result_data("GC=F","2023/4/10","2023/04/12")


#[{ts:INT, open_price:FLOAT, close_price: FLOAT, ....}, {}, {}]
#금의 시세를 대강 보여주는 것

'''
#네이버 증권 시세
nfc = NaverinanceCrawler()
result_list = nfc.get_result_data(1,3)

ts = convert_date_str_to_ts("2023/3/14")
print(ts)
'''
