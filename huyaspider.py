import requests
from queue import Queue
from threading import Thread
import time

class Huya_spider(Thread):

    def __init__(self, data_queue, url):
        Thread.__init__(self)
        self.url = url
        self.data_queue = data_queue


    def run(self):
        self.get_data()
        self.parse()

    def get_data(self):
        while self.url.empty() == False:
            res = requests.get(self.url.get()).json()
            self.data_queue.put(res)
            if res['data']['datas'] == []:
                break
            elif res['data']['datas'] == [] is False:
                continue

    def parse(self):
        with open('huya.txt', 'a', encoding='UTF-8') as fp:
            while self.data_queue.empty() == False:
                res = self.data_queue.get()
                datas = res['data']['datas']
                for data in datas:
                    item = {}
                    item['主播名称'] = data['nick']
                    item['标题'] = data['introduction']
                    item['观看人数'] = data['totalCount']
                    item['直播路径'] = data['gameHostName']
                    item['直播类型'] = data['gameFullName']
                    item['直播间id'] = data['profileRoom']
                    item['主播头像'] = data['avatar180']
                    item['封面'] = data['screenshot']
                    fp.write(str(item))




if __name__ == '__main__':
    start = time.time()#开始时间
    data_queue = Queue()
    url = Queue()
    baseurl = 'https://www.huya.com/cache.php?m=LiveList&page={}'
    for i in range(500):
        url.put(baseurl.format(i))

    crawl = []

    for i in range(4):
        douyu = Huya_spider(data_queue=data_queue, url=url)
        crawl.append(douyu)
        douyu.start()

    for douyu in crawl:
        douyu.join()

    end = time.time()#结束时间
    t = end - start
    print(t, '秒')

"""
item['主播名称'] = x['nick']
item['标题'] = x['introduction']
item['观看人数'] = x['totalCount']
item['直播路径'] = x['gameHostName']
item['直播类型'] = x['gameFullName']
item['直播间id'] = x['profileRoom']
item['主播头像'] = x['avatar180']
item['封面'] = x['screenshot']

"""



