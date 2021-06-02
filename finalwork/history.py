import requests
from bs4 import BeautifulSoup
import re
import login

cookie_list = login.task()
cookies = ";".join(
    [item["name"] + "=" + item["value"] + "" for item in cookie_list])
print(cookies)
session = requests.Session()
# cookie要放到headers里
headers = {
    'Cookie': cookies
}
response = session.get(
    url='https://api.bilibili.com/x/web-interface/history/cursor?max=0&view_at=0&business=', headers=headers).json()
print(response)
