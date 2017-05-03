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


if __name__ == "__main__":
    chrome = webdriver.Chrome()
    # firefox = webdriver.Firefox()
    # firefox.find_element_by_id("").text
    itemParse = ItemParse("http://vacations.ctrip.com/tours/d-kunming-29", chrome)
    page = itemParse.main()
    # itemParse.parse_page(page)
