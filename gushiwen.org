import re
import requests

def parse_page(url):
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
    }
    response = requests.get(url,headers)
    text = response.text
    # re.DOTALL 可以让.匹配\n
    titles = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL,)
    dynasties = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>',text)
    authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?</a>.*?<a.*?>(.*?)</a>',text,re.DOTALL)
    shiwens = re.findall(r'<div\sclass="contson"\s.*?>(.*?)</div>',text,re.DOTALL)
    contents = []
    for shiwen in shiwens:
        x = re.sub(r'<.*?>',"",shiwen)
        contents.append(x.strip())

    poems = []
    for value in zip(titles,dynasties,authors,contents):
        title,dynasty,author,content = value
        poem = {
            'title' : title,
            'dynasty' : dynasty,
            'author' : author,
            'content' : content
        }
        poems.append(poem)
    for poem in poems:
        print(poem)

def main():
    for x in range(1,11):
        url = "https://www.gushiwen.org/default_%s.aspx" % x
        parse_page(url)

if __name__ == '__main__':
    main()
