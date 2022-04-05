import requests
from lxml import etree
from fake_useragent import UserAgent
import time
from multiprocessing import Process
from tophub热榜 import Xlsx


"""
#按行分
'//*[@id="Sortable"]'#每行四个榜单
#按榜单分
'//*[@id="Sortable"]/div'#每个榜单
#榜单名称
'//*[@id="Sortable"]/div/div/div[1]/div[1]/a/div/span/text()'
#榜单编号
'//*[@id="Sortable"]/div/div/div[2]/div[1]/a/div/span[1]/text()'
#榜单内容
'//*[@id="Sortable"]/div/div/div[2]/div[1]/a/div/span[@class="t"]/text()'
#热度
'//*[@id="Sortable"]/div/div/div[2]/div[1]/a/div/span[@class="e"]/text()'
#路径
'//*[@id="Sortable"]/div/div/div[2]/div[1]/a/@href'
"""

#获取ip
class GetProx:

    def __init__(self):
        self.url = "https://proxypool.scrape.center/random"

    def run(self):
        res = requests.get(self.url)
        self.proxies = {'https': res.text}
        return self.proxies

#保留html代码
class Gethtml:

    def __init__(self, proxies):
        self.proxies = proxies
        self.headers = {
            'User-Agent': UserAgent().random
            }
        self.g_url = "https://tophub.today/"
        self.t = time.strftime("%Y-%m-%d")


    def run(self):
        print(self.proxies)
        try:
            response = requests.get(url=self.g_url, proxies=self.proxies, headers=self.headers)
            if response.status_code == 200:
                with open('{}.txt'.format(self.t), 'a', encoding='utf8')as f:
                    f.write(response.text)
        except Exception:
            print(Exception)



#解析html代码
class Parse(Process):
    def __init__(self):
        Process.__init__(self)
        self.xl = Xlsx()
        self.t = time.strftime("%Y-%m-%d")

    def run(self):
        with open('{}.txt'.format(self.t), 'r', encoding='utf-8')as f:
            text = f.read()
        e = etree.HTML(text)
        tlist = e.xpath('//*[@id="Sortable"]/div/@id')
        for i in tlist:
            name = e.xpath('//div/div[@id="{}"]/div/div[1]/div[1]/a/div/span/text()'.format(i))
            index = e.xpath('//div/div[@id="{}"]/div/div[2]/div[1]/a/div/span[1]/text()'.format(i))
            content = e.xpath('//div/div[@id="{}"]/div/div[2]/div[1]/a/div/span[@class="t"]/text()'.format(i))
            nums = e.xpath('//div/div[@id="{}"]/div/div[2]/div[1]/a/div/span[@class="e"]/text()'.format(i))
            href = e.xpath('//div/div[@id="{}"]/div/div[2]/div[1]/a/@href'.format(i))
            for i in name:
                c = self.xl.wb.create_sheet(i)
                c.append(index)
                c.append(content)
                c.append(nums)
                c.append(href)
        self.xl.wb.save('{}.xlsx'.format(self.t))

if __name__ == '__main__':
    prox = GetProx()
    proxies = prox.run()
    crawl = Gethtml(proxies)
    crawl.run()
    parse = Parse()
    parse.start()






