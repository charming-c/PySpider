import requests
from bs4 import BeautifulSoup

def request():
  baseurl = 'https://www.bilibili.com/v/popular/rank/all'
  header = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Cookie' : '__mta=208960173.1618923731947.1620954535557.1620954542825.14; uuid_n_v=v1; uuid=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; _csrf=d6387db599ead817b92741f3f472f12797e6988f8cdce1735d8e271c8b25ea00; _lxsdk_cuid=178ef5fb81fc8-0285ef215be32f-1f3b6054-13c680-178ef5fb81fc8; _lxsdk=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1618923731,1620954368; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; __mta=208960173.1618923731947.1619332411045.1620954391121.13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1620954542; _lxsdk_s=1796868c9c9-83a-00-bc7%7C%7C13'
  }
  response = requests.get(baseurl, headers=header)
  if response.status_code == 200:
    # print(response.text)
    return response.text
  else:
    print(response.status_code)
    return None

if __name__ == '__main__':
  html = request()
  res = BeautifulSoup(html,'lxml')
  list = res.find_all('li')
  # print(list)
  data = []
  for item in list:
    map = {}
    if item.find('div',class_='num') == None:
      continue
    # map['No'] = item.find('div',class_='num').string
    # map['Title'] = item.find('a',class_='title').string
    print(item.find('span',class_='data-box up-name'))
    name = item.find('span', class_='data-box up-name')

    data.append(map)
  print(data)
