from threading import Thread
from queue import Queue
from fake_useragent import UserAgent
import requests
from lxml import etree

#PS:只是爬取100部电影信息不按排名排序整理
# 多线程爬虫
class CrawlInfo(Thread):
    def __init__(self, url_queue,html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue


    def run(self):
        headers = {
            "User-Agent": UserAgent().random
        }

        while self.url_queue.empty() == False:
            url = self.url_queue.get()
            resposne = requests.get(url, headers=headers)
            if resposne.status_code == 200:
                self.html_queue.put(resposne.text)


class Parse(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while self.html_queue.empty() == False:
            e = etree.HTML(self.html_queue.get())
            infolist = e.xpath('//div[@class="el-col el-col-18 el-col-offset-3"]/div/div/div')
            with open('top100movies.txt', 'a', encoding='utf-8') as f:
                for info in infolist:
                    pic = info.xpath('div[1]/a/img/@src')[0]
                    title = info.xpath('div[2]/a/h2/text()')[0]
                    place = info.xpath('div[2]/div[2]/span/text()')[0]
                    point = info.xpath('div[3]/p[1]/text()')[0]
                    f.write(title + '\n' + point + '\t' + place + '\t' + pic)




if __name__ == '__main__':
    url_queue = Queue()
    html_queue = Queue()
    base_url = 'https://ssr1.scrape.center/page/{}'
    for i in range(1, 11):
        new_url = base_url.format(i)
        url_queue.put(new_url)

    #创建爬虫
    crawlist = []
    for i in range(0, 3):
        crawl1 = CrawlInfo(url_queue, html_queue)
        crawlist.append(crawl1)
        crawl1.start()


    for crawl1 in crawlist:
        crawl1.join()

    parselist = []
    for i in range(0, 3):
        parse = Parse(html_queue)
        parselist.append(parse)
        parse.start()

    for parse in parselist:
        parse.join()
