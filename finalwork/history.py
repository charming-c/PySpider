import requests
from bs4 import BeautifulSoup
import re

cookies = "_uuid=63FE9804-4EAC-2F0B-82E8-96BBCF1A200422552infoc; buvid3=8FC30C23-64E4-4E5E-83C6-B9C853581AD534755infoc; fingerprint=d89efac30b065e08cd50a00b8ef8e4da; buvid_fp_plain=66485397-ACB0-48F1-9DD9-2F117C9385B434781infoc; buvid_fp=11A5B980-3A38-4537-A15C-C9917FB0819013416infoc; SESSDATA=4c1178d4,1638717885,694ea*61; bili_jct=6be88b4d1b391a05b18bb9bb5c70b608; DedeUserID=393655428; DedeUserID__ckMd5=4f73a2d258556d63; sid=a0dkun8s; PVID=3; bfe_id=018fcd81e698bbc7e0648e86bdc49e09"


def vedioFormat(vedio):
    data = []
    for item in vedio:
        elem = {}
        elem['title'] = item['title']
        elem['bvid'] = item['history']['bvid']
        elem['author_mid'] = item['author_mid']
        elem['tag_name'] = item['tag_name']
        data.append(elem)
    return data


def getLaterHistory(param):
    base_url = 'https://api.bilibili.com/x/web-interface/history/cursor'
    headers = {
        'Cookie': cookies
    }
    response = requests.get(url=base_url, params=param, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def getHistory():
    vedio_format_list = []
    session = requests.Session()
    # cookie要放到headers里
    headers = {
        'Cookie': cookies
    }
    list = session.get(
        url='https://api.bilibili.com/x/web-interface/history/cursor?max=0&view_at=0&business=', headers=headers).json()
    # 返回之后的History的参数,以及视频的List
    paramList = list['data']['cursor']
    vedio = list['data']['list']
    vedio_format = vedioFormat(vedio)
    for item in vedio_format:
        vedio_format_list.append(item)
    while getLaterHistory(paramList) != None:
        list = getLaterHistory(paramList)
        if 'data' in list.keys():
            paramList = list['data']['cursor']
            vedio = list['data']['list']
            vedio_format = vedioFormat(vedio)
            # print(vedio_format)
            for item in vedio_format:
                vedio_format_list.append(item)
        else:
            break
    print(vedio_format_list.count)
    return vedio_format_list


def getHistoryList():
    # 返回直接的网络请求的body
    list = getHistory()

    # 返回之后的History的参数,以及视频的List
    paramList = list['data']['cursor']
    vedio = list['data']['list']
    vedio_format = vedioFormat(vedio)
    print(vedio_format)


if __name__ == "__main__":
    getHistory()
