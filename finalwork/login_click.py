from selenium import webdriver
import time
import requests
from PIL import Image
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from chaojiying import Chaojiying_Client

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Cookie': '__mta=208960173.1618923731947.1620954535557.1620954542825.14; uuid_n_v=v1; uuid=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; _csrf=d6387db599ead817b92741f3f472f12797e6988f8cdce1735d8e271c8b25ea00; _lxsdk_cuid=178ef5fb81fc8-0285ef215be32f-1f3b6054-13c680-178ef5fb81fc8; _lxsdk=9BF5D7C0A1D811EBA5216760317F62A729C80466D4CF4FFABC5A782E8E7911A6; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1618923731,1620954368; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; __mta=208960173.1618923731947.1619332411045.1620954391121.13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1620954542; _lxsdk_s=1796868c9c9-83a-00-bc7%7C%7C13'
}

username = "15879239734"
password = ""

browser = webdriver.Chrome()
browser.get('https://passport.bilibili.com/login')
browser.implicitly_wait(10)
browser.maximize_window()
time.sleep(1)

login_type = browser.find_element_by_xpath('//div[@class="type-tab"]/span[1]')
login_type.click()

username_input = browser.find_element_by_xpath('//*[@id="login-username"]')
password_input = browser.find_element_by_xpath('//*[@id="login-passwd"]')

username_input.send_keys(username)
password_input.send_keys(password)
time.sleep(3)

login_input = browser.find_element_by_css_selector(
    '#geetest-wrap > div > div.btn-box > a.btn.btn-login')
login_input.click()
time.sleep(3)

code_img_ele = browser.find_element_by_xpath(
    '/html/body/div[2]/div[2]/div[6]/div/div')
img_url = browser.find_element_by_xpath(
    '/html/body/div[2]/div[2]/div[6]/div/div/div[2]/div[1]/div/div[2]/img').get_attribute('src')

img_data = requests.get(url=img_url, headers=header).content
with open('./node.png', 'wb')as fp:
    fp.write(img_data)
i = Image.open('./node.png')
# 将图片缩小并保存，设置宽为172，高为192
small_img = i.resize((172, 192))
small_img.save('./small_node.png')

chaojiying = Chaojiying_Client(
    '15879239734', 'caijiaming', '917691')
im = open('small_node.png', 'rb').read()
# 9004是验证码类型
result = chaojiying.PostPic(im, 9004)['pic_str']

all_list = []  # 要存储即将被点击的点的坐标  [[x1,y1],[x2,y2]]
if '|' in result:
    list_1 = result.split('|')
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(',')[0])
        y = int(list_1[i].split(',')[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(',')[0])
    y = int(result.split(',')[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)

# 遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行点击操作
# x,y坐标乘2和0.8，是由于
for l in all_list:
    x = l[0]
    y = l[1]
    # 将点击操作的参照物移动到指定的模块，
    # 若用方法二获取的验证码图片，要添加下面代码对code_img_ele赋值
    # code_img_ele = bro.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div/div[2]/div[1]/div/div[2]/img')
    ActionChains(browser).move_to_element_with_offset(
        code_img_ele, x, y).click().perform()
    time.sleep(0.1)
    print(all_list)
    print('点击已完成')

# 完成动作链点击操作后，定位确认按钮并点击
browser.find_element_by_xpath(
    '/html/body/div[2]/div[2]/div[6]/div/div/div[3]/a').click()
# browser.close()
