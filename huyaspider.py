import requests
from fake_useragent import UserAgent
from lxml import etree


url = 'https://www.huya.com/l'
headers = {
    'UserAgent': UserAgent().random
}
html = requests.get(url, headers).text
e = etree.HTML(html)
hlist = e.xpath('//ul[@class="live-list clearfix"]/li')
with open('huyaspider.txt', 'a', encoding='utf8') as f:
    f.write('标题' + '\t' + '主播名称' + '\t' + '直播类型' + '\t' + '观看热度' + '\t' + '头像' + '\t' + '直播间路径' + '\n')
    for res in hlist:
        title = res.xpath('a[2]/@title')[0]
        name = res.xpath('span[@class="txt"]/span[1]/i/@title')[0]
        type = res.xpath('span[@class="txt"]/span[2]/a/@title')[0]
        onlinenum = res.xpath('span[@class="txt"]/span[3]/i[2]/text()')[0]
        icon = res.xpath('span[@class="txt"]/span[1]/img/@data-original')[0]
        href = res.xpath('a[1]/@href')[0]
        f.write(title + '\t' + name + '\t' + type + '\t' + onlinenum + '\t' + icon + '\t' + href + '\n')
