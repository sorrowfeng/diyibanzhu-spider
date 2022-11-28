import requests
from lxml import etree
import os
import re
import sys
import time

site_url = "http://www.bz1111.xyz"
search_url = "http://www.bz1111.xyz/s.php"#"https://www.bz1111.xyz/home/search"


# 将两个列表对应组和成一个新的字典
def list_dic(list1, list2):
    '''
    two lists merge a dict,a list as key,other list as value
    :param list1:key
    :param list2:value
    :return:dict
    '''
    dic = dict(map(lambda x, y: [x, y], list1, list2))  # lambda是匿名函数, 冒号前为参数, 后面为返回值, 即传入x, y, 返回[x,y]
    return dic  # map函数, 第一个参数为函数名, 后面为参数, 返回返回一个将 function 应用于 iterable 中每一项并输出其结果的迭代器。


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


class Spider:
    word = ''
    file_name = ''

    def __init__(self, word):
        self.word = word  # 初始化参数

    def start_requests(self):
        # 请求网站拿到数据，抽取小说名创建文件夹，抽取小说链接
        data = {
            'action': 'search',
            'q': self.word
        }
        response = requests.post(search_url, headers=headers, data=data)
        response.encoding = "utf-8"  # 解决了获取到的中文名称乱码的问题
        myhtml = etree.HTML(response.text)  # 解析并返回一个 Element 对象
        print(response.text)

        # 通过xpath定位想要获取的元素
        name_list = myhtml.xpath("//ul/li/div/a/text()")        #("//*[@id='sitebox']/dl/dd[1]/h3/a/text()")
        writer_list = myhtml.xpath("//ul/li/div/p[2]/text()")   #("//*[@id='sitebox']/dl/dd[2]/span[1]/a/text()")
        url_list = myhtml.xpath("//ul/li/div/a/@href")         #("//*[@id='sitebox']/dl/dd[1]/h3/a/@href")
        for i in range(0, len(url_list)):
            url_list[i] = site_url + url_list[i]
        # print(name_list, writer_list, url_list)


        # 将两个列表对应组和成一个新的字典new_dic
        new_dic = list_dic(name_list, url_list)
        # print(new_dic)

        if not new_dic:  # 如果字典为空
            print("没有找到此书")
            os.system('pause')
            return

        num = 0
        find_dic = {}
        print('\n')
        for i in new_dic:
            num += 1
            find_dic[str(num)] = i  # 将找到的结果再放入一个字典内, 方便序号查找
            print(str(num) + '.  ' + i + '\t作者: ' + writer_list[num - 1])
        book_num = input('\n你想下载的是(请输入序号, 输入q重新搜索):')
        if book_num == 'q':
            return

        print('\n\n')
        shu_name = find_dic[book_num]  # 确定书名
        shu_url = new_dic.get(shu_name)  # 从字典中找到对应书名的链接      
        print('正在为你下载书籍:' + shu_name + '\n')

        self.file_name = shu_name + '.txt'  # 写入的文件名
        if os.path.exists(self.file_name):  # 如果文件存在
            os.remove(self.file_name)  # 删除文件

        self.requests_zhang(shu_url)  # 请求每个章节的链接

        print('\n下载完成!存放于' + os.getcwd() + '\\' + self.file_name + '\n')
        print('如要重新搜索')
        os.system('pause')

    def start_requests_for_novel(self, shu_url):
        self.requests_zhang(shu_url)  # 请求每个章节的链接

        print('\n下载完成!存放于' + os.getcwd() + '\\' + self.file_name + '\n')
        print('如要重新搜索')
        os.system('pause')



    def requests_zhang(self, shu_url):
        # 请求小说拿到数据，抽取章名、文章链接
        response = requests.get(shu_url, headers=headers)
        # 乱码 header显示编码格式是ISO-8859-1 内容的格式是utf-8 需要修改代码格式
        # response.encoding = 'utf-8'
        # print(response.encoding) #没定义编码格式的时候，header显示的编码格式
        # print(response.apparent_encoding) #内容实际采用的编码格式
        # print(response.headers) #查看头标签内容
        html = etree.HTML(response.text)
        self.file_name = html.xpath("//div[3]/div[2]/div[1]/div[2]/h1/text()")[0]
        self.file_name = self.file_name + '.txt'  # 写入的文件名
        if os.path.exists(self.file_name):  # 如果文件存在
            os.remove(self.file_name)  # 删除文件

        zhang_name_list = html.xpath('//div[3]/div[7]/div[2]/ul/li/a/text()')  # 获取每章的名称
        zhang_url_list = html.xpath('//div[3]/div[7]/div[2]/ul/li/a/@href')  # 获取每章的链接
        # print(zhang_name_list, zhang_url_list)
        for zhang_name, zhang_url in zip(zhang_name_list, zhang_url_list):  # zip的作用
            # 请求每章的数据, 将每章的章节名与链接传入request_data函数
            self.requests_data(zhang_name, zhang_url)  # >>> x = [1, 2, 3]
            return


    # 请求具体的每章内容
    def requests_data(self, zhang_name, zhang_url):
        print("\n正在下载章节：" + zhang_name)
        with open(self.file_name, "a", encoding='utf-8') as file:  # 使用with语句写入文件, 不管在处理文件过程中是否发生异常, 都能保证 with 语句执行完毕后已经关闭了打开的文件句柄
            file.write('\n\n\n' + str(zhang_name) + '\n\n\n')  # 写入章节名

            # 获取总页数
            page_url = site_url + zhang_url  # 每章的url
            # print(page_url)
            response = requests.get(page_url, headers=headers)
            # response.encoding = 'utf-8'  # 编码
            html = etree.HTML(response.text)
            page_nums_str = str(html.xpath('//center/a[last()]/text()')[0])
            page_nums = int(page_nums_str[1:-1])
            # page_nums = int(re.search(r'(?<=/).*?(?=\))', page_nums_str).group())

            # 第一页
            content = "\n".join(html.xpath('//*[@id="chapterinfo"]/text()'))  # 将"\n"作为后面返回内容的拼接
            content = self.removeOtherContent(content)
            file.write(content)  # 写入正文内容
            self.printSchedule(1/page_nums)

            # 后续页
            for i in range(2, page_nums+1):
                every_page_url = site_url + zhang_url.replace(".html", "") + "_" + str(i) + ".html"
                self.printSchedule(i/page_nums)

                # 请求文章拿到文章内容，创建文件保存到相应文件夹
                response = requests.get(every_page_url, headers=headers)
                # response.encoding = 'utf-8'  # 编码
                html = etree.HTML(response.text)
                # content = "\n".join(html.xpath('//*[@id="ad"]/text()'))  # 将"\n"作为后面返回内容的拼接

                # TODO: 获取后续页无法正确获取到内容
                content = html.xpath('//*[@id="ad"]/text()')
                for n in content:
                    # 取出来的是个element对象，需要给他转换成字符串
                    string = etree.tostring(n, encoding='utf-8').decode('utf-8')     # 字符串类型
                # 转成字符串后中文不能正常显示，需要再对其进行解析
                # name2 = HTMLParser().unescape(name1.decode())
                # content = name2

                # content = self.removeOtherContent(content)
                # file.write(content)  # 写入正文内容

    def removeOtherContent(self, content):
        content = content.replace(" ", "")
        content = content.replace("第一版主;", "")
        return content

    def printSchedule(self, value):
        i = int(value * 100)
        print("\r", end="")
        print("进度: {}%: ".format(i), "▋" * (i // 2), end="")



if __name__ == '__main__':
    while True:
        os.system('cls')
        print('-----------第一版主搜索（输入q退出）-----------')
        word = input('请输入搜索的书名(或作者):')
        if word == 'q':
            break
        spider = Spider(word)
        # spider.start_requests()  # 开始爬取
        spider.start_requests_for_novel(word)
