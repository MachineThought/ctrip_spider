# *-* utf-8 *-*
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time


class CtripParse:
    def __init__(self, page_source, parse_type="html.parser"):
        self.cbs = BeautifulSoup(page_source, parse_type)
        self.message = {"result": "success", "data": ""}
        self.data = {"itemId": "", "name": "", "price": "", "score": "", "scoreLevel": "", "commNum": "", "travelNum": "", "service": "",
                     "provider": ""}

    # 临时读取页面的方法,主要用于测试
    def read_file(self, path):
        page_code = ""
        with open(path, 'r', encoding='utf-8') as source_file:
            page_code = source_file.read()
            source_file.close()
        return page_code

    # 初始化解析器
    # def init_parse(self):
    #     page = self.read_file('page/ctrip.html')
    #     cbs = BeautifulSoup(page, "html.parser")
    #     return cbs

    # 校验值合理性
    def check(self, value):
        if value is None or value == "":
            return False
        else:
            return True

    def __item_id(self):
        cbs = self.cbs
        try:
            item_id = cbs.find(id="TrackProductId")
            print(item_id)
            if self.check(item_id):
                item_id = item_id["value"]
                self.data["itemId"] = item_id
        except Exception as err:
            print(err)

    # 解析页面标题
    def __parse_title(self):
        cbs = self.cbs
        try:
            title = cbs.find("h1", {"itemprop": "name"})
            if self.check(title):
                title = str(title.text).strip()
                self.data["name"] = title
            else:
                self.message["result"] = "err"
        except Exception as err:
            print(err)

    # 解析价格,由于价格是动态获取
    def __parse_price(self):
        cbs = self.cbs
        try:
            price = cbs.find("strong", {"class": "total_price"})
            if self.check(price):
                price = str(price.text).strip()
                if price.find("¥") >= 0 and price.find("/"):
                    self.data["price"] = price[price.find("¥") + 1:price.find("/")]
            else:
                self.message["result"] = "retry"
        except Exception as err:
            print(err)

    def __parse_comm(self):
        cbs = self.cbs
        check = self.check
        try:
            # 评分
            score = cbs.find("a", {"class": "score"})
            if check(score):
                score = re.match('[0-9\.]*', str(score.text).strip()).group()
                self.data["score"] = score
                # 评论数
            comment_num = cbs.find("a", {"class": "comment_num"})
            if check(comment_num):
                commNum = re.match('[0-9]*', str(comment_num.text).strip()).group()
                self.data["commNum"] = commNum
            # 评分分布，即从5分到1分的人数分布
            score_level = cbs.select("ul.process span.num")
            score_level_list = ""
            # 评分人数分布
            if check(score_level):
                if len(score_level) == 5:
                    for item in score_level:
                        item = str(item.text)
                        if item.find("(") == 0 and item.find(")") == len(item) - 1:
                            item = item[1:len(item) - 1]
                            score_level_list += item + ","
                    score_level_list = score_level_list[:len(score_level_list) - 1]
                    self.data["scoreLevel"] = score_level_list
                else:
                    print("无评分等信息")
            # 出游人数
            travel_num = cbs.select("div.comment_wrap > span")
            if check(travel_num):
                if len(travel_num) > 0:
                    travel_num = str(travel_num[0].text)
                    travelNum = re.match('[0-9]*', travel_num).group()
                    self.data["travelNum"] = travelNum
        except Exception as err:
            print(err)

    # 解析商品信息
    def __parse_store(self):
        bs = self.cbs
        check = self.check
        try:
            service = bs.select(".service_dl span")
            service_item = ""
            if check(service):
                for item in service:
                    item = str(item.text).strip()
                    service_item += item + " "
                service_item = service_item.strip()
                self.data["service"] = service_item

            provider = bs.find("dl", {"class": "provider_info"})
            if check(provider):
                provider_type = provider.find("dt")
                provider_type = str(provider_type.text).strip()
                provider_info = ""
                if provider_type == "供应商":
                    provider_info = provider.find("a", {"class": "provider_name"}).text
                elif provider_type == "零售商":
                    provider_info = provider.find("a").text
                self.data["provider"] = provider_info
        except Exception as err:
            print(err)

    # main方法，用来测试
    def main(self):
        self.__item_id()
        self.__parse_title()
        self.__parse_price()
        self.__parse_comm()
        self.__parse_store()
        print(self.data)
        return self.data


if __name__ == "__main__":
    page_code = ""
    with open('page/ctrip.html', 'r', encoding='utf-8') as source_file:
        page_code = source_file.read()
        source_file.close()
    # firefox = webdriver.Firefox()
    # firefox.get("http://vacations.ctrip.com/morelinetravel/p17185842s2.html?kwd=%E4%B8%89%E4%BA%9A")
    # time.sleep(1)
    # page_code = firefox.page_source
    # with open('page/ctrip.html', 'w', encoding='utf-8') as w_file:
    #     w_file.write(page_code)
    #     w_file.close()
    # print(page_code)
    ctripParse = CtripParse(page_code)
    ctripParse.main()
