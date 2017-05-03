# *-* utf-8 *-*
from bs4 import BeautifulSoup
import pdbc
from selenium import webdriver
import time

class DestUrlParse:
    def __init__(self, page_source, parse_type="html.parser"):
        self.dbs = BeautifulSoup(page_source, parse_type)

    def inner_dest(self):
        dbs = self.dbs
        try:
            result = []
            inner = dbs.select(".jmp_nopic_2 .left_detail dd a")

            if inner is not None and inner != "":
                for item in inner:
                    inner_map = {}
                    href = item["href"]
                    if href.find("whole") >= 0:
                        continue
                    else:
                        href = "http://vacations.ctrip.com" + href
                    city_name = str(item.text).strip()
                    inner_map["cityName"] = city_name
                    inner_map["cityUrl"] = href
                    result.append(inner_map)
            return result
        except Exception as err:
            print(err)

    def other_dest(self):
        dbs = self.dbs
        try:
            result = []
            other = dbs.select(".destination_col h3 a")
            if other is not None and other != "":
                for item in other:
                    other_map = {}
                    href = item["href"]
                    city_name = str(item.text).strip()
                    if href.find("themetravel") >= 0 or href.find("whole") >= 0:
                        continue
                    else:
                        href = "http://vacations.ctrip.com" + href
                    other_map["cityName"] = city_name
                    other_map["cityUrl"] = href
                    result.append(other_map)
            return result
        except Exception as err:
            print(err)

    def main(self):
        inner = self.inner_dest()
        other = self.other_dest()
        for item in other:
            inner.append(item)
        url_list = []
        for index in inner:
            url_list.append(index["cityUrl"])
        print(len(url_list))
        return inner



if __name__ == "__main__":
    page_code = ""
    with open('page/index.html', 'r', encoding='utf-8') as source_file:
        page_code = source_file.read()
        source_file.close()
    # firefox = webdriver.Firefox()
    # firefox.get("http://vacations.ctrip.com/")
    # time.sleep(5)
    # page_code = firefox.page_source
    # with open('page/index.html','w',encoding='utf-8') as w_file:
    #     w_file.write(page_code)
    #     w_file.close()
    destUrlParse = DestUrlParse(page_code)
    # pdb = pdbc.PDBC()
    result = destUrlParse.main()
    # pdb.insert_dest(result)
