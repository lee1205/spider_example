import requests
from fake_useragent import UserAgent

class BdTranslate:
    def __init__(self, input):
        self.headers = {'User-Agent': UserAgent().random}
        self.data = {'kw': input}
        self.url = "https://fanyi.baidu.com/sug"


    def run(self):
        html = requests.post(url=self.url, data=self.data, headers=self.headers).json()
        data = html['data']
        for i in range(0, len(data)):
            basekw = data[i]['k']
            trankw = data[i]['v']
            print(basekw, trankw)


if __name__ == '__main__':
    kw = input("请输入需要翻译的内容")
    bd = BdTranslate(kw)
    bd.run()
