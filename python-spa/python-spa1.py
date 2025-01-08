import requests
import time

class spa1:
    # 初始化url和headers参数
    def __init__(self):
        self.url = 'https://spa1.scrape.center/api/movie/?limit=10&offset={}'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
    # 定义翻页函数url_update
    def url_update(self):
        for page in range(0,100):
            url = self.url.format(page)
            time.sleep(3)
            print(f"现在正在获取此：{url}")
            self.data_info(url)

    # 定义获取数据函数data_info
    def data_info(self, url):
        json_info = requests.get(url,headers=self.headers).json()
        print(json_info)


if __name__ == "__main__":
    spider=spa1()
    spider.url_update()
    spider.data_info()
