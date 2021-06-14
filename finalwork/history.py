import time
import requests
from bs4 import BeautifulSoup
import re

cookies = "_uuid=F2E037CB-E440-8D01-38BF-44AE2B88C69D25532infoc; buvid3=850CC698-A15D-4728-916C-16ADB89FDB2C58470infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(JY~|lk~)kJ0J'uY|lmlumRm; fingerprint3=d8cba0a319d8ae4d4d70620a5fa6e407; buivd_fp=850CC698-A15D-4728-916C-16ADB89FDB2C58470infoc; buvid_fp_plain=850CC698-A15D-4728-916C-16ADB89FDB2C58470infoc; fingerprint_s=d8daf13363291e7cc71968a6f67561e1; CURRENT_QUALITY=120; buvid_fp=850CC698-A15D-4728-916C-16ADB89FDB2C58470infoc; bp_t_offset_393655428=527265651439099836; DedeUserID=393655428; DedeUserID__ckMd5=4f73a2d258556d63; PVID=2; bsource=search_google; bfe_id=018fcd81e698bbc7e0648e86bdc49e09; fingerprint=b79a6143ddb7d7dc9527336b56442b40; SESSDATA=b770dac9%2C1639242101%2C80dda%2A61; bili_jct=cc3c2b7402fe901348256876ad21bdfc; sid=6un6d6jr; bp_video_offset_393655428=536163651146616019"


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


def getHistory(username, password):
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
        time.sleep(3)
    # print(len(vedio_format_list))
    # print(vedio_format_list)
    return vedio_format_list


def analyseHistoryList():
    # 返回能够拿到的所有历史`
    list = getHistory()


if __name__ == "__main__":
    getHistory('12344', '22323')
