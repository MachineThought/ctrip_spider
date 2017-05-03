# *-* utf-8 *-*
from selenium import webdriver
from bs4 import BeautifulSoup
import cparse
import re
import json
import time


class ItemParse:
    def __init__(self, main_url, web_driver):
        self.url = main_url
        self.driver = web_driver
        self.page_size = -1
        # self.dfile = data_file

    def page_size_parse(self):
        driver = self.driver
        driver.get(self.url)
        page = driver.page_source
        bs = BeautifulSoup(page, "html.parser")
        page_tag = bs.find("span", {"class": "c_page2_numtop"})
        if page_tag is not None and page_tag != "":
            page_text = str(page_tag.text)
            page_size = re.match('[0-9]*', page_text[page_text.find("/") + 1:]).group()
            self.page_size = page_size

    #
    def parse_page(self, page):
        bs = BeautifulSoup(page, 'html.parser')
        textarea = bs.select("textarea")
        item_list = []
        if textarea is not None and textarea != "":
            for item in textarea:
                item = str(item.text).strip()
                if item == "":
                    continue
                item = json.loads(item)
                item_url = item["Url"]
                if item_url.find("/") == 0:
                    continue
                item_list.append(item_url)
        return item_list

    def main(self):
        self.page_size_parse()
        index = 2
        page_list = [self.url]
        while index <= int(self.page_size):
            page_list.append(self.url + "/p" + str(index))
            index += 1
        with open("data/result", 'w', encoding='utf8') as f:
            for page_item in page_list:
                print(page_item)
                self.driver.get(page_item)
                page = self.driver.page_source
                travel_list = self.parse_page(page)
                for travel_item in travel_list:
                    print(travel_item)
                    self.driver.get(travel_item)
                    time.sleep(1)
                    temp = self.driver.find_element_by_id("J_total_price").text
                    print(temp)
                    detail_page = self.driver.page_source
                    cParse = cparse.CtripParse(detail_page)
                    data = cParse.main()
                    if data["price"] == "":
                        data["price"] = temp[temp.find("¥") + 1:temp.find("/")]
                    print(data)
                    f.write(str(data) + "\n")
            f.close()


if __name__ == "__main__":
    dest_url = ['http://vacations.ctrip.com/tours/d-sanya-61', 'http://vacations.ctrip.com/tours/d-haikou-37',
                'http://vacations.ctrip.com/tours/s-sanya-10558612', 'http://vacations.ctrip.com/tours/s-sanya-10558611',
                'http://vacations.ctrip.com/tours/s-sanya-88071', 'http://vacations.ctrip.com/tours/s-sanya-10558614',
                'http://vacations.ctrip.com/tours/s-sanya-10524171', 'http://vacations.ctrip.com/tours/d-xishaqundao-530',
                'http://vacations.ctrip.com/tours/d-xiamen-21', 'http://vacations.ctrip.com/tours/d-fuzhou-164']
    dest_url_2 = ['http://vacations.ctrip.com/tours/d-gulangyu-120058', 'http://vacations.ctrip.com/tours/s-longyan-13293683',
                  'http://vacations.ctrip.com/tours/d-wuyishan-22', 'http://vacations.ctrip.com/tours/s-xiamen-91537',
                  'http://vacations.ctrip.com/tours/s-xiamen-79124', 'http://vacations.ctrip.com/tours/s-najing-90729',
                  'http://vacations.ctrip.com/tours/d-lijiang-32', 'http://vacations.ctrip.com/tours/d-kunming-29',
                  'http://vacations.ctrip.com/tours/d-xianggelila-106', 'http://vacations.ctrip.com/tours/d-xishuangbanna-30',
                  'http://vacations.ctrip.com/tours/d-luguhu-105', 'http://vacations.ctrip.com/tours/d-tengchong-696',
                  'http://vacations.ctrip.com/tours/d-ruili-1213', 'http://vacations.ctrip.com/tours/s-lijiang-75919',
                  'http://vacations.ctrip.com/tours/d-dali-31', 'http://vacations.ctrip.com/tours/d-honghe-512']
    dest_url_3 = ['http://vacations.ctrip.com/tours/d-guilin-28', 'http://vacations.ctrip.com/tours/s-guilin-75898',
                  'http://vacations.ctrip.com/tours/d-beihai-140', 'http://vacations.ctrip.com/tours/d-yangshuo-702',
                  'http://vacations.ctrip.com/tours/d-nanning-166', 'http://vacations.ctrip.com/tours/d-longjititian-970',
                  'http://vacations.ctrip.com/tours/d-weizhouisland-120063', 'http://vacations.ctrip.com/tours/d-jiuzhaigou-25',
                  'http://vacations.ctrip.com/tours/d-chengdu-104', 'http://vacations.ctrip.com/tours/d-emeishan-24',
                  'http://vacations.ctrip.com/tours/d-leshan-103', 'http://vacations.ctrip.com/tours/d-qingchengshan-143879',
                  'http://vacations.ctrip.com/tours/d-hailuogou-705', 'http://vacations.ctrip.com/tours/d-dujiangyan-911',
                  'http://vacations.ctrip.com/tours/d-aba-744', 'http://vacations.ctrip.com/tours/d-danba-704',
                  'http://vacations.ctrip.com/tours/d-daocheng-342', 'http://vacations.ctrip.com/tours/d-xilingxueshan-1484',
                  'http://vacations.ctrip.com/tours/s-beijing-75594', 'http://vacations.ctrip.com/tours/s-beijing-75595',
                  'http://vacations.ctrip.com/tours/s-beijing-75598', 'http://vacations.ctrip.com/tours/s-beijing-10523549',
                  'http://vacations.ctrip.com/tours/s-beijing-75597', 'http://vacations.ctrip.com/tours/s-yanqing-75596',
                  'http://vacations.ctrip.com/tours/s-beijing-76681', 'http://vacations.ctrip.com/tours/s-beijing-75599',
                  'http://vacations.ctrip.com/tours/d-yantai-170', 'http://vacations.ctrip.com/tours/d-weihai-169',
                  'http://vacations.ctrip.com/tours/d-jinan-128', 'http://vacations.ctrip.com/tours/d-qingdao-5',
                  'http://vacations.ctrip.com/tours/d-taishan-6', 'http://vacations.ctrip.com/tours/d-rizhao-622',
                  'http://vacations.ctrip.com/tours/s-qingdao-85745', 'http://vacations.ctrip.com/tours/d-zaozhuang-656',
                  'http://vacations.ctrip.com/tours/d-qufu-129', 'http://vacations.ctrip.com/tours/d-penglai-168',
                  'http://vacations.ctrip.com/tours/d-zaozhuang-143872', 'http://vacations.ctrip.com/tours/d-hangzhou-14',
                  'http://vacations.ctrip.com/tours/d-shanghaidisneyresort-1446916', 'http://vacations.ctrip.com/tours/d-shanghai-2',
                  'http://vacations.ctrip.com/tours/d-qiandaohu-17', 'http://vacations.ctrip.com/tours/d-wuzhen-508',
                  'http://vacations.ctrip.com/tours/d-huangshan-19', 'http://vacations.ctrip.com/tours/d-putuoshan-16',
                  'http://vacations.ctrip.com/tours/d-nanjing-9', 'http://vacations.ctrip.com/tours/d-suzhou-11',
                  'http://vacations.ctrip.com/tours/d-wuxi-10', 'http://vacations.ctrip.com/tours/d-xitang-15',
                  'http://vacations.ctrip.com/tours/d-zhouzhuang-81', 'http://vacations.ctrip.com/tours/d-shaoxing-18',
                  'http://vacations.ctrip.com/tours/d-changbaishan-268', 'http://vacations.ctrip.com/tours/s-dalian-87618',
                  'http://vacations.ctrip.com/tours/d-dalian-4', 'http://vacations.ctrip.com/tours/d-changchun-216',
                  'http://vacations.ctrip.com/tours/d-haerbin-151', 'http://vacations.ctrip.com/tours/d-wudalianchi-857',
                  'http://vacations.ctrip.com/tours/d-yabuli-815', 'http://vacations.ctrip.com/tours/d-jilin-100031']

    dest_url_4 = ['http://vacations.ctrip.com/tours/d-xian-7', 'http://vacations.ctrip.com/tours/d-yanan-423',
                  'http://vacations.ctrip.com/tours/d-huashan-183', 'http://vacations.ctrip.com/tours/s-xian-75682',
                  'http://vacations.ctrip.com/tours/s-fufeng-84611', 'http://vacations.ctrip.com/tours/s-qianxian-84602',
                  'http://vacations.ctrip.com/tours/s-huangling-79231', 'http://vacations.ctrip.com/tours/s-yichuan-79235',
                  'http://vacations.ctrip.com/tours/s-xian-75684', 'http://vacations.ctrip.com/tours/d-wuhan-145',
                  'http://vacations.ctrip.com/tours/d-yichang-313', 'http://vacations.ctrip.com/tours/s-yichang-20361735',
                  'http://vacations.ctrip.com/tours/s-wuhan-77593', 'http://vacations.ctrip.com/tours/d-wudangshan-146',
                  'http://vacations.ctrip.com/tours/d-shennongjia-147', 'http://vacations.ctrip.com/tours/d-enshi-487',
                  'http://vacations.ctrip.com/tours/s-changyang-83949', 'http://vacations.ctrip.com/tours/s-wuhan-10558912',
                  'http://vacations.ctrip.com/tours/d-nanchang-175', 'http://vacations.ctrip.com/tours/d-jingdezhen-405',
                  'http://vacations.ctrip.com/tours/d-lushan-20', 'http://vacations.ctrip.com/tours/d-wuyuan-446',
                  'http://vacations.ctrip.com/tours/d-sanqingshan-159', 'http://vacations.ctrip.com/tours/d-longhushan-160',
                  'http://vacations.ctrip.com/tours/d-jinggangshan-171', 'http://vacations.ctrip.com/tours/d-mingyueshan-752',
                  'http://vacations.ctrip.com/tours/d-yichun-743', 'http://vacations.ctrip.com/tours/d-wugongshan-1445145',
                  'http://vacations.ctrip.com/tours/s-wuyuan-10547759', 'http://vacations.ctrip.com/tours/d-hongkong-38',
                  'http://vacations.ctrip.com/tours/d-macau-39', 'http://vacations.ctrip.com/tours/d-taiwan-100076',
                  'http://vacations.ctrip.com/tours/d-japan-100041', 'http://vacations.ctrip.com/tours/d-mongolia-20391',
                  'http://vacations.ctrip.com/tours/r-dongnanya-110', 'http://vacations.ctrip.com/tours/r-nanya-109',
                  'http://vacations.ctrip.com/tours/r-europe-120002', 'http://vacations.ctrip.com/tours/r-meizhou-102',
                  'http://vacations.ctrip.com/tours/r-axnt-114', 'http://vacations.ctrip.com/tours/r-zhongdongfei-113']
    chrome = webdriver.Chrome()
    # firefox = webdriver.Firefox()
    # firefox.find_element_by_id("").text
    for url in dest_url:
        itemParse = ItemParse(url, chrome)
        itemParse.main()
