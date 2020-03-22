import requests
from lxml import etree
import re
import os
import urllib.request
import threading
from queue import Queue



class Procuder(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Procuder, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):
        response = requests.get(url,headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt') #获取图片名字
            alt = re.sub(r'[\?？\.，。！!\*]','',alt) #有的图片名字结尾有符号，window请名字不能以他结尾
            img_url = re.sub('!dta','',img_url)
            suffix = os.path.splitext(img_url)[1]
            filename = alt + suffix
            self.img_queue.put((img_url,filename)) #封包

class Cousumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Cousumer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get() #解包
            urllib.request.urlretrieve(img_url,'images/'+filename)
            print(filename+'下载完成！')

def main():
    page_queue = Queue(10)
    img_queue = Queue(100)
    for x in range(1,11):
        url = 'http://www.doutula.com/photo/list/?page=%d' % x
        page_queue.put(url)

    for x in range(5):
        t = Procuder(page_queue,img_queue)
        t.start()

    for x in range(5):
        t = Cousumer(page_queue,img_queue)
        t.start()


if __name__ == '__main__':
    main()
