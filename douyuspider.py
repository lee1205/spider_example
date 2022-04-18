import requests
from queue import Queue
from threading import Thread
import time

class Douyu_spider(Thread):

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
            if res['data']['rl'] == []:
                break
            elif res['data']['rl'] == [] is False:
                continue

    def parse(self):
        with open('douyu.txt', 'a',encoding='utf-8') as f:
            while self.data_queue.empty() == False:
                res = self.data_queue.get()
                datas = res['data']['rl']
                for data in datas:
                    item = {}
                    item['房间id'] = data['rid']
                    item['主播名称'] = data['nn']
                    item['直播间标题'] = data['rn']
                    item['主播用户id'] = data['uid']
                    item['主播热度'] = data['ol']
                    item['主播认证'] = data['od']
                    f.write(str(item))




if __name__ == '__main__':
    start = time.time()#开始时间
    data_queue = Queue()
    url = Queue()
    baseurl = 'https://www.douyu.com/gapi/rkc/directory/mixList/0_0/{}'
    for i in range(1000):
        url.put(baseurl.format(i))

    crawl = []

    for i in range(4):
        douyu = Douyu_spider(data_queue=data_queue, url=url)
        crawl.append(douyu)
        douyu.start()

    for douyu in crawl:
        douyu.join()

    end = time.time()#结束时间
    t = end - start
    print(t, '秒')



