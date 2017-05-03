from selenium import webdriver
import time

if __name__ == "__main__":

    driver = webdriver.Ie()
    driver.get('http://www.baidu.com')
    driver.find_element_by_id('kw').send_keys('Selenium')
    driver.find_element_by_id('su').click()

    driver.quit()
    # browser = webdriver.Ie()
    # time.sleep(5)
    # browser.get("http://www.baidu.com")
    # browser.get("http://moni.dhfpp.com/web/login.htm")
    # # time.sleep(30)
    # print(browser.page_source)
    # bidnumber = browser.find_element_by_name("bidnumber")
    # bidnumber.send_keys("12121212")
    # bidpass = browser.find_element_by_name("bidpassword")
    # bidpass.send_keys("1212")
