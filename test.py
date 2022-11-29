import requests
import re

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By

from imgdict import img_dict

headers = {
    'authority': 'www.bz1111.xyz',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'origin': 'https://www.bz1111.xyz',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.bz1111.xyz/home/search',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'PHPSESSID=aq5qkghfkqobqaguea133mprvb; Hm_lvt_56f6ef8da27855c47600c2c17b3e16f7=1644820405; Hm_lpvt_56f6ef8da27855c47600c2c17b3e16f7=1644821283',
}


def format_text(t) -> str:
    m_text = t.replace('<br>', '')
    m_text = m_text.replace('&nbsp;', '')

    def replace_img(match) -> str:
        key = str(match.group(0))
        key = key.replace('<img src="/toimg/data/', '')
        key = key.replace('.png">', '')
        return img_dict[str(key)]

    m_text = re.sub(r'<img src="/toimg/data/.*?\.png">', replace_img, m_text)
    return m_text


every_page_url = "http://www.bz1111.xyz/7/7944/133919_2.html"

browser = webdriver.Edge()
browser.implicitly_wait(5)

browser.minimize_window()
browser.get(every_page_url)

myDynamicElement = browser.find_element(By.XPATH, '//div[@id="ad"]')
text = browser.page_source

content = re.search(r'(?<=<div id="ad">).*?(?=</div>)', text).group()
print(format_text(content))

# print(browser.find_element(By.XPATH('//div[@id="ad"]')).text)
# ('//*[@id="ad"]/text()')


# # 请求文章拿到文章内容，创建文件保存到相应文件夹
# response = requests.get(every_page_url, headers=headers)
# # response.encoding = 'utf-8'  # 编码
# html = etree.HTML(response.text)
# # content = "\n".join(html.xpath('//*[@id="ad"]/text()'))  # 将"\n"作为后面返回内容的拼接
#
# # TODO: 获取后续页无法正确获取到内容
# content = html.xpath('//*[@id="ad"]/text()')
#
# print(content)
#
# for n in content:
#     # 取出来的是个element对象，需要给他转换成字符串
#     string = etree.tostring(n, encoding='utf-8').decode('utf-8')  # 字符串类型
