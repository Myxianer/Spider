import requests
from lxml import etree
import re
import xlwt
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/73.0.3683.86 Safari/537.36',
    'Host': 'nb.lianjia.com',
}

f = xlwt.Workbook(encoding='utf_8')
sheet01 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
sheet01.write(0, 0, '标题')
sheet01.write(0, 1, '地区')
sheet01.write(0, 2, '面积')
sheet01.write(0, 3, '朝向')
sheet01.write(0, 4, '厅室')
sheet01.write(0, 5, '价格')
sheet01.write(0, 6, '标签')
sheet01.write(0, 7, '链接')

num = 1

print("——————————开始——————————")

for x in range(1, 101):
    print("正在爬取第%d页" % x)
    url = 'https://nb.lianjia.com/zufang/pg%d/' % x
    response = requests.get(url, headers=headers)
    result = response.text
    html = etree.HTML(result, etree.HTMLParser())
    divs = html.xpath("//div[@class='content__list--item']")
    title = None
    house_url = None
    local = None
    area = None
    home = None
    price = None
    label = None
    orientation = None
    for div in divs:
        try:
            title = "".join(div.xpath(".//p[contains(@class,'content__list--item--title')]/a/text()")).strip()
            house_url = "https://nb.lianjia.com" + "".join(
                div.xpath(".//p[contains(@class,'content__list--item--title')]/a/@href"))
            info = div.xpath(".//p[@class='content__list--item--des']//text()")
            local = "".join(info[1:4])
            if "/" in local:
                local = "".join(div.xpath(".//p[contains(@class,'content__list--item--brand')]/text()")).strip()
            area = info[6].strip()
            if "㎡" not in area:
                area = info[4].strip()
            orientation = info[8].strip()
            if "室" in orientation or "厅" in orientation:
                orientation = info[6].strip()
            home = info[-1].strip()
            if "室" not in home and "厅" not in home:
                home = info[10].strip()
            price = "".join(div.xpath(".//span[@class='content__list--item-price']//text()")).strip()
            label = "/".join(div.xpath(".//p[contains(@class,'content__list--item--bottom')]//text()")).strip()
            label = re.sub("\s", "", label)
            label = re.sub("//", "/", label)
        except:
            pass
        finally:
            sheet01.write(num, 0, title)
            sheet01.write(num, 1, local)
            sheet01.write(num, 2, area)
            sheet01.write(num, 3, orientation)
            sheet01.write(num, 4, home)
            sheet01.write(num, 5, price)
            sheet01.write(num, 6, label)
            sheet01.write(num, 7, house_url)
            num += 1
    time.sleep(0.5)


print("——————————结束——————————")
f.save('info' + '.xls')
