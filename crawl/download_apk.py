import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
import requests
import re

from crawl.config import Config_Reader

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


class Virus_Share_Crawl:
    VIRUS_SHARE_SEARCH = "https://virusshare.com/search"
    VIRUS_SHARE_LOGIN = "https://virusshare.com/processlogin"
    Download_Url = "https://virusshare.com/download?"

    def crawl_login(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }
        s = requests.session()
        login = Config_Reader().get_download_login()
        params = {
            "username": login.get("username"),
            "password": login.get("password")
        }
        s.post(url=self.VIRUS_SHARE_LOGIN, headers=headers, data=params)
        cook_value = ""
        for x in s.cookies:
            cook_value += x.name + '=' + x.value + ';'
            cook_value = cook_value[:len(cook_value) - 1]
        return cook_value

    def crawl_hash_data(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
            "Cookie": self.crawl_login()
        }
        resp = requests.get(url="https://virusshare.com/hashfiles/VirusShare_00389.md5", headers=headers)
        res = re.split("^[0-9a-zA-Z]", resp.text)[0].split("\n")
        return res

    def judge_hash_is_apk(self, hash_contain, cookies):
        headers = {
            "Cookie": self.crawl_login(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
        }
        max_workers = Config_Reader().get_max_worker()
        for md5 in hash_contain:
            try:
                params = {"search": md5}
                resp = requests.post(url=self.VIRUS_SHARE_SEARCH, data=params, headers=headers)
                is_apk = re.search("<td class='lc'>Extension</td><td colspan=2>apk</td>", resp.text)
                is_login = re.search("login", resp.text)
                if is_apk:
                    sha256 = re.search("<td class='lc'>SHA256</td><td colspan=2>[0-9a-zA-Z]*", resp.text)
                    executor = ThreadPoolExecutor(max_workers=max_workers)
                    executor.submit(self.download, sha256.group(0)[40:], md5, cookies)
                if not is_apk and is_login:
                    logging.info("======需要重新登录=====")
                time.sleep(5)
            except Exception as e:
                logging.error(e)
        pass

    def download(self, sha256, md5, cookies):
        logging.info("====================download start====================")
        headers = {
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://virusshare.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7",
            "Cookie": "SESSID=" + cookies[0]["value"],
        }
        file = requests.get(url=self.Download_Url + sha256, headers=headers, stream=True)
        download_path = Config_Reader().get_download_path()
        unzip_path = Config_Reader().get_unzip_path()
        with open(download_path + "Virusshare_" + md5 + ".zip", "wb") as apk:
            for chunk in file.iter_content(chunk_size=1024):
                apk.write(chunk)
        os.system("unzip " + " -o -P infected -x " +
                  download_path + "Virusshare_" + md5 + ".zip"
                  + " -d " + unzip_path)
        os.system("mv -f " + unzip_path + sha256 + " " + unzip_path + "Virusshare_" + md5 + ".apk")
        os.system("sh " + unzip_path + "apk.sh " + "Virusshare_" + md5 + ".apk")
        logging.info("====================download finish====================")
