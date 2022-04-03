import requests
from lxml import etree
from fake_useragent import UserAgent
from queue import Queue


class Gethtml:
    def __init__(self, que_url, que_html):
        self.que_url = que_url
        self.que_html = que_html
        self.headers = {
            'User-Agent': UserAgent().random
        }

    def run(self):
        while self.que_url.empty() == False:
            url = self.que_url.get()
            res = requests.get(url=url, headers=self.headers)
            if res.status_code == 200:
                self.que_html.put(res.text)

#解析类
class Parse:
    def __init__(self, que_html):
        self.que_html = que_html


    def run(self):
        f.write('中文标题' + '\t' + '英文标题' + '\t' + '电影信息' + '\t' + '电影分数' + '\t' + '影评数量' + '\n')
        while self.que_html.empty() == False:
            html = self.que_html.get()
            e = etree.HTML(html)
            plist = e.xpath('//*[@id="content"]/div/div[1]/ol')
            for a in plist:
                cntitle = a.xpath('li/div/div[2]/div[1]/a/span[1]/text()')
                entitle = a.xpath('li/div/div[2]/div[1]/a/span[2]/text()')
                brief = a.xpath('li/div/div[2]/div[2]/p[1]/text()')
                point = a.xpath('li/div/div[2]/div[2]/div/span[2]/text()')
                viewnums = a.xpath('li/div/div[2]/div[2]/div/span[4]/text()')
                for a in range(0, len(cntitle)):
                    f.write(cntitle[a] + '\t' + entitle[a] + '\t' + brief[a] + '\t' + point[a] + '\t' + viewnums[a] + '\n' + '\n')

if __name__ == '__main__':
    que_url = Queue()
    que_html = Queue()
    base_url = "https://movie.douban.com/top250?start={}&filter="
    for i in range(0, 10):
        url = base_url.format(25 * i)
        que_url.put(url)

    get = Gethtml(que_url, que_html)
    get.run()
    par = Parse(que_html)
    with open('豆瓣top250目录爬取.txt', 'a', encoding='utf8') as f:
        par.run()



