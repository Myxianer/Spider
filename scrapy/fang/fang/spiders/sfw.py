# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem,ESFHouseItem
# 如果使用redis爬虫，加上下面这一行
from scrapy_redis.spiders import RedisSpider

# 如果使用redis爬虫，类改一下，
# 删除start_url.增加一个redis_key='xxx',例如redis_key="fang:start_urls"
#class SfwSpider(RedisSpider):
class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province = province_text
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # 构建新房url
                # 新的https://anqing.newhouse.fang.com/house/s/
                # 老的https://anqing.fang.com/
                url_module = city_url.split(".")
                first = url_module[0]
                newhouse_url = first + ".newhouse.fang.com/house/s/"
                # 构建二手房url
                # 新的https://anqing.esf.fang.com/
                # 老的https://anqing.fang.com/
                esf_url = first + ".esf.fang.com/"

                #yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={"info": (province, city)})


    def parse_newhouse(self,response):
        province,city = response.meta.get("info")
        lis = response.xpath("//div[@class='nl_con clearfix']/ul/li")
        for li in lis:
            try:
                name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            except:
                pass
            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type_list = list(map(lambda x:re.sub(r"\s","",x),house_type_list))
            rooms = list(filter(lambda x:x.endswith("居"),house_type_list))
            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|-|－|/","",area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            try:
                district = re.search(r".*\[(.+)\].*",district_text).group(1)
                sale = li.xpath(".//div[contains(@class,'fangyuan')]/span/text()").get()
            except:
                pass
            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告","",price)
            try:
                origin_url = "https:" + li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            except:
                pass

            item = NewHouseItem(name=name,rooms=rooms,area=area,address=address,district=district,sale=sale,price=price,origin_url=origin_url,province=province,city=city)
            yield item

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={"info":(province,city)})


    def parse_esf(self,response):
        province,city = response.meta.get("info")
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            item = ESFHouseItem(province=province,city=city)
            item['name'] = dl.xpath(".//p[@class='add_shop']/a/@title").getall()
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x:re.sub(r"\s","",x),infos))
            for info in infos:
                try:
                    if "厅" in info:
                        item['rooms'] = info
                    elif "卧室" in info:
                        item['rooms'] = info
                    elif "㎡" in info:
                        item['area'] = info
                    elif "层" in info:
                        item['floor'] = info
                    elif "叠加" in info:
                        item['floor'] = info
                    elif "双拼" in info:
                        item['floor'] = info
                    elif "独栋" in info:
                        item['floor'] = info
                    elif '向' in info:
                        item['toward'] = info
                    elif '年建' in info:
                        item['year'] = info.replace('年建',"")
                except:
                    pass
                #print(item)
            item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            item['price'] = dl.xpath(".//dd[@class='price_right']/span/b/text()").get()
            try:
                unit = dl.xpath(".//dd[@class='price_right']//span/text()").getall()
                item['unit'] = unit[1]
            except:
                pass
            origin_url = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
            item['origin_url'] = origin_url
        #print(item)
            yield item
        next_url = response.urljoin(response.xpath("//div[@class='page_al']/p/a/@href").get())
        yield scrapy.Request(url=next_url,callback=self.parse_esf,meta={"info":(province,city)})



