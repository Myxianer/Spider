import requests
import json
import re
import time

import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def jd_spider():
    for i in range(0, 25):
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2041&productId=100005603836&score=0&sortType=6&page='+ str(i)+'&pageSize=10&isShadowSku=0&fold=1'
        headers = {
            "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer":"https://item.jd.com/100005603836.html"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            # 截取json数据字符串
            response_json_str = response.text[26:-2]
            # 字符串转json对象
            response_json_obj = json.loads(response_json_str)
            # 获取评论列表数据
            response_json_comments = response_json_obj['comments']
            # 写入前先清空之前的数据
            # if os.path.exists(comment_file_path):
            #     os.remove(comment_file_path)
            # 遍历评论对象列表
            for response_json_comment in response_json_comments:
                # 获取评论对象中的评论内容
                response_json_comment['content'] = re.sub(r'此用户未填写评价内容', "", response_json_comment['content'])
                # 以追加模式黄行写入每条评价
                with open("content.txt", 'a', encoding='utf-8') as f:
                    f.write((response_json_comment['content']) + '\n')
                # 打印评论对象中的评论内容
                print(response_json_comment['content'])
            time.sleep(1)
        except:
            print("爬取失败")


def cut_word():
    with open("content.txt", encoding='utf-8') as f:
        comment_txt = f.read()
        wordlist = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(wordlist)
        print(wl)
        return wl


def create_word_cloud():
    # 设置图云形状
    coloring = np.array(Image.open('jd.jpg'))
    # 设置一些词云设置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=coloring, scale=4, max_font_size=50, random_state=42, font_path='C:\Windows\Fonts\AdobeSongStd-Light.otf')

    # 生成词云
    wc.generate(cut_word())

    # 在只设置mask的情况下，您将会获得一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()


if __name__ == '__main__':
    jd_spider()
    cut_word()
    create_word_cloud()
