import requests
import csv
import time
from datetime import datetime

class spa1:
    # 初始化url和headers参数
    def __init__(self):
        self.url = 'https://spa1.scrape.center/api/movie/?limit=10&offset={}'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
        self.all_movies = []

        self.filename = 'moves.csv'
        # self.headers = ['ID','NAME','ALIAS','COVER','CATEGORIES','PUBLISHED_AT','MINUTE','SCORE','REGIONS']

    # 定义翻页函数url_update
    def url_update(self):
        for page in range(0,100):
            url = self.url.format(page)
            time.sleep(3)
            print(f"现在正在获取此：{url}")
            try:
                json_info = requests.get(url,headers=self.headers).json()
                # print(json_info)
                self.moves_data(json_info['results'])
            except Exception as e:
                print(f"请求失败:{url}, 错误信息:{e}")
                continue


    # 定义对获取的数据进行处理函数moves_data
    def moves_data(self, json_info):
        for move in json_info:
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
            self.all_movies.append(move_data)
            print(f"已收集电影数据:{len(self.all_movies)}")
            # print(f"已提取电影名字:{move_data['NAME']}")
        # print(self.all_movies) 

        self.save_info_cvs(move_data)   
        

    # 定义保存函数save_info_cvs
    def save_info_cvs(self, move_data):
        if not self.all_movies:
            print("没有电影数据")
            return

        # 获取当前时间
        times = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 定义文件名
        # filename = f'data_{times}.csv'  # 采用时间戳命名需把次注释打开
                                        # 采用固定文件命名,在类实例位置添加self.filename = 'movies.csv'
        # 定义表头
        headers = ['ID','NAME','ALIAS','COVER','CATEGORIES','PUBLISHED_AT','MINUTE','SCORE','REGIONS']
        # 写入csv文件
        with open(self.filename,'w',encoding='utf-8',newline='') as f:
            # 创建csv写入对象
            writer = csv.DictWriter(f,fieldnames=headers)
            # 写入表头,且只在第一次写入表头
            if f.tell() == 0:
                writer.writeheader()
            # 写入数据
            for move_data in self.all_movies:
                writer.writerow(move_data)
                print(f"已保存电影:{move_data['NAME']}")

        # 清空列表，准备下一次保存
        # self.all_movies.clear()

        # 注:如果采用时间戳的命名方式保存数据,则会生成N个文件,如果采用固定csv文件名,则只会生成一个文件保存.

if __name__ == "__main__":
    spider=spa1()
    spider.url_update()
    spider.save_info_cvs()

