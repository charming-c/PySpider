import requests
from bs4 import BeautifulSoup
import re

# r = requests.get("https://baidu.com")
# print(type(r))
# print(r.status_code)
# print(type(r.text))
# print(r.text, 'UTF-8')
# print(r.cookies)

# params = {
#   "name":"germey",
#   "age":22
# }
# r = requests.get("http://httpbin.org/get",params=params)
# res = r.json()
# print(res["headers"])
# print(res["origin"])
# print(r.text)

# 由于知乎的html返回值已经变了，所以得到的数据是无法正则匹配到正确结果的
# headers = {
#   "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36" 
# }
# r = requests.get("https://www.zhihu.com/explore", headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
# titles = re.findall(pattern, r.text)
# print(r.status_code)
# ret = BeautifulSoup(r.text,'lxml')
# print(ret.find(class="div"))

header = {
  'accept' : "application/vnd.github.v3+json"
}
r2 = requests.get('https://github.com/favicon.ico',headers=header)
print(r2.status_code)
with open("favicon.ico",'wb') as f:
  f.write(r2.content)
  f.close()