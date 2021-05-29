import requests
import re
from bs4 import BeautifulSoup
import numpy as np

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Cookie': '__mta=208960173.1618923731947.1620954535557.1620954542825.14; uuid_n_v=v1; uuid=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; _csrf=d6387db599ead817b92741f3f472f12797e6988f8cdce1735d8e271c8b25ea00; _lxsdk_cuid=178ef5fb81fc8-0285ef215be32f-1f3b6054-13c680-178ef5fb81fc8; _lxsdk=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1618923731,1620954368; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; __mta=208960173.1618923731947.1619332411045.1620954391121.13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1620954542; _lxsdk_s=1796868c9c9-83a-00-bc7%7C%7C13'
}


def searchUser(name):
    base_url = 'https://search.bilibili.com/upuser'
    param = {
        'keyword': name
    }
    response = requests.get(base_url, params=param, headers=header)
    if response.status_code == 200:
        data = []

        html = BeautifulSoup(response.text, 'lxml')

        text = html.find('p', class_='total-text')
        # count = re.search(
        #     r'.*?class="total-text">.*?共找到([0-9]*?)个用户.*?', str(text), re.DOTALL)
        # data['count'] = int(count.group(1))

        user_list = html.find_all('li', class_="user-item")
        for item in user_list:
            user = {}
            userName = item.find('a', class_="title").string
            result = re.search(
                r'.*?href="(.*?)" target=".*?稿件：(.*?)</span>.*?粉丝：(.*?)</span.*?', str(item), re.DOTALL)
            userPage = result.group(1)
            vedio = result.group(2)
            fans = result.group(3)

            user['username'] = userName
            user['vedio'] = vedio
            user['page'] = userPage
            user['fans'] = fans
            data.append(user)
        return data
    else:
        print('The searchUser request has error!')


if __name__ == '__main__':
    searchUser('老番茄')
