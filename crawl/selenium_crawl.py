import time

from selenium import webdriver
import re

from crawl.config import Config_Reader
from crawl.download_apk import Virus_Share_Crawl


class Selenium_Crawl:

    Virus_Share_Url = "http://www.virusshare.com"
    Virus_Share_Login = "http://www.virusshare.com/login"

    def login_virus_share(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')  # 这句一定要加
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.Virus_Share_Login)
        login = Config_Reader().get_selenium_login()
        driver.find_element_by_xpath("//input[@name='username']").send_keys(login.get("username"))
        driver.find_element_by_xpath("//input[@name='password']").send_keys(login.get("password"))
        driver.find_element_by_xpath("//input[@value='Login']").click()
        return driver

    def crawl_apk(self):
        driver = self.login_virus_share()
        driver.find_element_by_xpath("//input[@name='search']").send_keys("android")
        driver.find_element_by_xpath("//input[@value='Search']").click()
        for i in range(20000):
            md5_list = []
            html = driver.page_source
            result = re.findall('</td></tr><tr><td class="lc">MD5</td><td colspan="2">.*</td></tr>', html)
            for res in result:
                md5_list.append(res[53:-10])
            Virus_Share_Crawl().judge_hash_is_apk(md5_list, driver.get_cookies())
            driver.find_element_by_xpath("//input[@value='More Results']").click()
            time.sleep(4)

