import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import numpy as np
from PIL import Image

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Cookie': '__mta=208960173.1618923731947.1620954535557.1620954542825.14; uuid_n_v=v1; uuid=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; _csrf=d6387db599ead817b92741f3f472f12797e6988f8cdce1735d8e271c8b25ea00; _lxsdk_cuid=178ef5fb81fc8-0285ef215be32f-1f3b6054-13c680-178ef5fb81fc8; _lxsdk=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1618923731,1620954368; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; __mta=208960173.1618923731947.1619332411045.1620954391121.13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1620954542; _lxsdk_s=1796868c9c9-83a-00-bc7%7C%7C13'
}


def getCid(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist'
    param = {
        'bvid': str(bvid),
        'jsonp': 'jsonp'
    }
    response = requests.get(url, headers=header, params=param)
    if response.status_code == 200:
        json = response.json()
        return json['data'][0]['cid']
    else:
        return None


def getDanmu(bvid):
    cid = getCid(bvid)
    url = 'https://api.bilibili.com/x/v2/dm/web/seg.so'
    param = {
        'type': 1,
        'oid': cid,
        'segment_index': 1
    }
    response = requests.get(url, headers=header, params=param)
    if response.status_code == 200:
        list = re.findall(r'.*?:\t?[\x00-\xff]?(.*?)@.*?', response.text)
        return list
    else:
        return None

# b站弹幕有两个接口，这个是远古接口，虽然现在b站新的不用，但任然可以拿到弹幕的详情，很nice


def getDanmu1(bvid):
    cid = getCid(bvid)
    url = 'https://api.bilibili.com/x/v1/dm/list.so'
    param = {
        'type': 1,
        'oid': cid,
        'segment_index': 1
    }
    response = requests.get(url, headers=header, params=param)
    if response.status_code == 200:
        html = BeautifulSoup(response.content, 'lxml')
        list = html.find_all('d')
        data = []
        for item in list:
            data.append(item.string)
        return data
    else:
        return None


def generateCloud(bvid):
    list = getDanmu(bvid)
    res = {}
    for item in list:
        if item in res.keys():
            res[item] += 1
        else:
            res[item] = 1

    wordcloud = WordCloud(
        background_color='white',  # 设置背景颜色  默认是black
        width=1000, height=800,
        max_words=100,            # 词云显示的最大词语数量
        max_font_size=99,         # 设置字体最大值
        min_font_size=16,         # 设置子图最小值
        random_state=100,           # 设置随机生成状态，即多少种配色方案
        font_path="SourceHanSerifK-Light.otf").generate_from_frequencies(res)

    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('wordcloud')
    plt.show()


if __name__ == '__main__':
    # generateCloud('BV1j54y1V7fd')
    getDanmu1('BV1f54y1V7FR')
