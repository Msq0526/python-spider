import requests
import time

class spa1:
    # 初始化url和headers参数
    def __init__(self):
        self.url = 'https://spa1.scrape.center/api/movie/?limit=10&offset={}'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
        self.all_movies = list

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
        # print(json_info)
        self.moves_data(json_info)

    # 定义对获取的数据进行处理函数
    def moves_data(self, json_info):
        for move in json_info['results']:
            move_data = {
                'ID': move.get('id'),
                'NAME': move.get('name'),
                'ALIAS': move.get('alias'),
                'COVER': move.get('cover'),
                'CATEGORIES': move.get('categories'),
                'PUBLISHED_AT': move.get('published_at'),
                'MINUTE': move.get('minute'),
                'SCORE': move.get('score'),
                'REGIONS': move.get('regions')
            }
            self.all_movies(move_data)
            print(move_data)
            print(f"已提取电影:{move_data['NAME']}")

if __name__ == "__main__":
    spider=spa1()
    spider.url_update()
    spider.data_info()
    spider.moves_data()
