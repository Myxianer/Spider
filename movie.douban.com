import requests
from lxml import etree

#1.将整个网页爬下来
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Host":"chenshukai.life"
}
url = "https://movie.douban.com/cinema/nowplaying/beijing/"
response = requests.get(url, headers=headers)
text = response.text

#2.将抓取下来的数据按一定要求进行提取
html = etree.HTML(text)
ul = html.xpath("//ul[@class='lists']")[0]
# print(etree.tostring(ul, encoding='utf-8'), decode("utf-8"))
lis = ul.xpath("./li")
movies = []
for li in lis:
    title = li.xpath("@data-title")[0]
    score = li.xpath("@data-score")[0]
    duration = li.xpath("@data-duration")[0]
    region = li.xpath("@data-region")[0]
    direcotr = li.xpath("@data-director")[0]
    actors = li.xpath("@data-actors")[0]
    thumbnail = li.xpath(".//img/@src")
    movie = {
        'title': title,
        'score': score,
        'duration': duration,
        'region': region,
        'direcotr': direcotr,
        'actors': actors,
        'thumbnail': thumbnail
    }
    movies.append(movie)

print(movies)
