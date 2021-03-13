# virusshare爬虫
## 爬虫配置填写(config.yml)
### login
```
description:
    要要先在selenium抓取恶意代码的相关md5信息，
    再通过接口下载相关恶意代码包。。
    这里两个步骤就要登录两次。
    因为在virusshare一个账号不能在不同的会话中使用，所以需要申请两个virusshare账号。
    一个保持selenium登录获取md5信息，另一个在下载的时候进行登录。
```
- selenium_login: 给selenium获取md5时候，保持登录状态的账号
- download_login: 在下载的时候登录的账号。

ps： 如果需要更多的配置，建议写在config.yml文件中，然后在config.py获取相关配置，便于配置管理。

### path
1. download_path: 下载apk包的路径
2. unzip_path: 解压apk包的路径，同时在解压的时候，使用apktool进行逆向。[apktool的安装方式](https://ibotpeaches.github.io/Apktool/install/)

## 爬虫的使用姿势
### python 虚拟环境的安装
1. 首先安装virtualvenv：pip3 install virtualenv
2. 创建venv文件： virtualenv venv
3. 进入venv虚拟环境： source venv/bin/activate

### 运行步骤
0. 保证运行的环境之下有chrome
1. [下载chromedriver](https://chromedriver.chromium.org/downloads)
2. 将apk.sh中的路径进行修改，改为你unzip的路径名下
3. 将apk.sh转移到用于解压并逆向的目录路径之下
4. 将下载好的chromedriver 复制到/venv/bin路径下
5. 安装爬虫依赖的包：pip3 install -r requirements.txt
6. 直接使用main文件运行爬虫