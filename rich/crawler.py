import requests
import datetime
from bs4 import BeautifulSoup
import random
from util import *

class InfoCrawler():

    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list = [
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


    def set_random_user_agent(self):
        user_agent = random.choice(self.user_agent_list)
        self.headers['User-Agent'] = user_agent
        return user_agent

    def set_tor_proxy(self):
        pass

    def get_result_data(self, *args, **kwargs):
        # this method is the goal of class
        # argument should be considered with efficiency
        # if range input is date, date format is 'YYYY/MM/DD'159
        pass


    def parse_page(self, raw_response):
        pass



class YahooFinanceCrawler(InfoCrawler):
    def __init__(self):
            super().__init__()
            self.base_url = "https://query2.finance.yahoo.com/v8/finance/chart/{}?interval=1d&period1={}&period2={}"
            self.set_random_user_agent()

    def get_result_data(self, target_code, from_date_str, to_date_str):
        # [ {ts:INT, open_price:FLOAT, close_price:FLOAT, .....},  {}, {}  ]

        res_list = self.parse_page(target_code, from_date_str, to_date_str)
        return res_list

    def parse_page(self, target_code, from_date_str, to_date_str):
        # parse the json. Check response by network inspector
        from_ts = convert_date_str_to_ts(from_date_str)
        to_ts = convert_date_str_to_ts(to_date_str)
        target_url = self.base_url.format(target_code, from_ts, to_ts)
        res_list = []
        res = requests.get(target_url, headers=self.headers)
        
        res_json = res.json()
        ts_list = res_json["chart"]["result"][0]["timestamp"]
        price_dict =  res_json["chart"]["result"][0]["indicators"]["quote"][0]
        
        open_price_list = price_dict["open"]
        close_price_list = price_dict["close"]
        high_price_list = price_dict["high"], 
        low_price_list = price_dict["low"]

        for ts, open_price, close_price, high_price, low_price in zip(ts_list, open_price_list, close_price_list, high_price_list, low_price_list):
            info_dict = {
                "ts":ts,
                "open_price":open_price,
                "close_price":close_price,
                "high_price":high_price,
                "low_price":low_price,
            }
            res_list.append(info_dict)

        return res_list

class NaverFinanceCrawler(InfoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://finance.naver.com"

    def get_result_data(self, *args, **kwargs):
        pass

    def parse_page(self, raw_response):
        pass

class NaverDiscussionCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = self.base_url + "/item/board.naver"
        self.set_random_user_agent()

    def get_result_data(self, code, from_page, to_page):
        # [ {ts:INT, view_count:INT},  {}, {}  ]

        total_info_list = []
        for page_idx in range(from_page, to_page+1):
            info_list = self.parse_page(code, page_idx)
            total_info_list += info_list

        return total_info_list

    def parse_page(self, code, page_idx):
        info_dict_list = []

        params = {"code":str(code), "page":str(page_idx)}
        res = requests.get(self.base_url, params=params, headers=self.headers)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select(
            'table.type2 tr'
        )

        info_soup_list = [row for row in rows if str(row).find('mouseOut') >= 0]
        date_view_selector = 'td > span.tah'

        for info_soup in info_soup_list:
            date_view_list = info_soup.select(date_view_selector)
            #print(date_view_list)
            
            #time
            date_info_str = date_view_list[0].text

            y,m,d_and_time = date_info_str.split(".")
            d, time_info = d_and_time.split(" ")
            h, minute = time_info.split(":")

            ts = datetime.datetime(int(y),int(m),int(d),int(h),int(minute),0).timestamp()

            #view
            view_count = int(date_view_list[1].text)

            info_dict = {"ts":int(ts), "view_count": view_count}
            info_dict_list.append(info_dict)

        return info_dict_list


class MarketBuyerInfoCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = self.base_url + "/sise/investorDealTrendDay.naver"

    def get_result_data(self, from_page, to_page):
        # [ {ts:INT, ant:FLOAT, inst:FLOAT, foreigner:FLOAT,.....},  {}, {}  ]
        
        total_info_list = []
        for page_idx in range(from_page, to_page+1):
            info_list = self.parse_page(page_idx)
            total_info_list += info_list

        return total_info_list

    def parse_page(self, page_idx):

        info_dict_list = []

        now = datetime.datetime.now()
        y = str(now.year)
        m = str(now.month).rjust(2,"0")
        d = str(now.day).rjust(2,"0")
        date_str = "{0}{1}{2}".format(y,m,d)
        params = {"bizdate": date_str, "page":str(page_idx)}
        res = requests.get(self.base_url, params=params)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select(
            'table.type_1 > tr'
        )

        rows = rows[3:]
        info_soup_list = [row for row in rows if str(row).find("date") >= 0]

        for info_soup in info_soup_list:
            info_array = info_soup.select(
                'td'
            )

            date_dot_string = info_array[0].text
            date_slash_string = date_dot_string.replace(".","/")
            date_slash_string = "20" + date_slash_string
            ts = convert_date_str_to_ts(date_slash_string)

            ant_net_amount = int(info_array[1].text.replace(",",""))
            foreigner_net_amount = int(info_array[2].text.replace(",",""))
            institute_net_amount = int(info_array[3].text.replace(",",""))

            info_dict_list.append({
                "ts":ts,
                "ant_net_amount":ant_net_amount,
                "foreigner_net_amount":foreigner_net_amount,
                "institute_net_amount":institute_net_amount,
            })

        return info_dict_list

if __name__ == "__main__":


    ndc = NaverDiscussionCrawler()
    result_list = ndc.parse_page("086520",1)
    print(result_list)


    '''
    yfc = YahooFinanceCrawler()
    result_list = yfc.parse_page("GC=F", "2023/4/10", "2023/04/12")
    print(result_list)
    mbic = MarketBuyerInfoCrawler()
    result_list = mbic.get_result_data(1,10)
    res = mbic.parse_page(1)
    print(res)


    nfc = NaverFinanceCrawler()
    result_list = nfc.get_result_data(1,3)
    '''