import requests
import pymongo
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
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['spa1']['movies']
        # self.headers = ['ID','NAME','ALIAS','COVER','CATEGORIES','PUBLISHED_AT','MINUTE','SCORE','REGIONS']


    # 定义翻页函数url_update
    def url_update(self):
        for page in range(0,100):
            url = self.url.format(page)
            print(f"现在正在获取此：{url}")
            try:
                json_info = requests.get(url, headers=self.headers, timeout=5).json()
                # print(json_info)
                # 判断页面是否为空
                if not json_info['results']:
                    print(f"第{page}页已经没有数据，停止爬取")
                    break
                self.moves_data(json_info['results'])
            except Exception as e:
                print(f"请求失败:{url}, 错误信息:{e}")
                rum = 3
                while rum > 0:
                    try:
                        json_info = requests.get(url, headers=self.headers, timeout=5).json()
                        self.moves_data(json_info['results'])
                        break
                    except:
                        rum -= 1
                        continue


    # 定义对获取的数据进行处理函数moves_data
    def moves_data(self, json_info):
        if not isinstance(json_info, list):
            print(f"获取的数据不是列表类型，请检查数据类型")
            return
        
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
        

    # 定义保存函数save_info_cvs
    def save_info_cvs(self):
        if not self.all_movies:
            print("没有电影数据")
            return
        else:
            print('列表中存在数据，可以开始保存了！！！')

        # 获取当前时间
        times = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 定义文件名
        # filename = f'data_{times}.csv'  # 采用时间戳命名需把次注释打开
                                        # 采用固定文件命名,在类实例位置添加self.filename = 'movies.csv'
        # 定义表头
        try:
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
        except Exception as e:
            print(f"保存文件时错误，错误信息:{e}")

    
    def save_info_mongo(self):
        if not self.all_movies:
            print('无电影数据可以保存！！！')
            return
        else:
            print('列表中存在数据，可以开始保存了！！！')
        
        try:
            # 批量保存数据到MongoDB 
            result = self.db.insert_many(self.all_movies)
            print(f"已保存{len(result.inserted_ids)}条数据")

            # 创建索引
            self.db.create_index([('ID', pymongo.ASCENDING)])
            print("创建索引成功")
        except Exception as e:
            print(f"保存数据到MongoDB时发生错误,错误信息:{e}")

        # 注:如果采用时间戳的命名方式保存数据,则会生成N个文件,如果采用固定csv文件名,则只会生成一个文件保存.

if __name__ == "__main__":
    spider=spa1()
    spider.url_update()
    # spider.save_info_cvs() # 将数据存入cvs表格
    spider.save_info_mongo() # 将数据存入mongodb数据库
