import os

import yaml


class Config_Reader:

    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__), 'config.yml')
        with open(filename, 'r', encoding="utf-8") as f:
            f = f.read()
            self.yaml_reader = yaml.load(f, Loader=yaml.FullLoader)

    def get_download_login(self):
        return self.yaml_reader.get("login").get("download_login")

    def get_selenium_login(self):
        return self.yaml_reader.get("login").get("selenium_login")

    def get_download_path(self):
        return self.yaml_reader.get("path").get("download_path")

    def get_unzip_path(self):
        return self.yaml_reader.get("path").get("unzip_path")

    def get_max_worker(self):
        return self.yaml_reader.get("thread_pool").get("max_workers")
