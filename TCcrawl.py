import csv
import requests
import time
from datetime import datetime
from lxml import etree


'https://dongguan.taoche.com/all/?page=2#pagetag'
class TCcrawl():
    '获取淘车页面信息'
    def __init__(self, page):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        self.page = page
        self.time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.count = 1
        TChead = ['序号', '车辆名称', '地址', '购买年份', '公里数', '标价(万)', '链接', '图片链接']
        with open(f"./淘车_{self.time}.csv", "w", newline="", encoding='utf8')as f:
            write = csv.writer(f)
            write.writerow(TChead)

    def tocsv(self, tcdata, w):
        for item in tcdata:
            try:
                title = item.xpath('div[2]/a/@title')[0]
                place = item.xpath('div[2]/p/i[3]/text()')[0].replace(" ", "").replace('\n', '')
                byear = item.xpath('div[2]/p/i[1]/text()')[0]
                mileage = item.xpath('div[2]/p/i[2]/text()')[0]
                price = item.xpath('div[2]/div/i/text()')[0]
                href = item.xpath('div[2]/a/@href')[0]
                pichref = item.xpath('div[1]/div/a/img/@data-src')[0]
            except Exception as e:
                print(f"数据格式出错{e}")
                pass
            try:
                print(self.count, title, place, byear, mileage, price, href, pichref)
                w.writerow([self.count, title, place, byear, mileage, price, href, pichref])
            except Exception as e:
                print(f"-----写入出错-----{e}")
                pass
            self.count += 1  # 序号增量
            time.sleep(0.1)
        del tcdata



    def crawl_info(self):
        with open(f"./淘车_{self.time}.csv", "a", newline="", encoding='utf8')as f:
            w = csv.writer(f)
            try:
                for i in range(int(self.page)):
                    url = f'https://dongguan.taoche.com/all/?page={i+1}#pagetag'
                    res = requests.get(url=url, headers=self.headers)
                    res.content.decode('utf-8')
                    tree = etree.HTML(res.text)
                    tcdata = tree.xpath('//*[@id="container_base"]/ul/li[@data-state = "1"]')
                    self.tocsv(tcdata, w)
                    del res, tree
            except Exception as e:
                print(f"spider crawling error{e}")
                pass





if __name__ == '__main__':
    page = input('请输入你需要爬取的页数页数：')
    tc = TCcrawl(page=page)
    tc.crawl_info()