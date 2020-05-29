import requests
from lxml import etree
from pyquery import PyQuery as pq
import os
import time

# 站点Url
siteUrl = 'https://www.xsbiquge.com'

# 小说目录页Url
noteUrl = ''

# 小说名
noteName = ''

# 章节页Url
pageUrls = []

# 保存目录
saveDir = ''


def getNoteUrl():
    print('请输入小说目录页地址:', end='')
    url = ''
    try:
        url = input()
        if url[24] != '/':
            exit(0)
    except:
        print('获取错误!')
        exit(0)

    return url


def getNoteName(url):
    r = requests.get(url)
    if r.status_code:
        r.encoding = r.apparent_encoding

    doc = pq(r.text)
    return doc('div #info h1').text()


def getPages(mainUrl, noteUrl):
    r = requests.get(url=noteUrl)
    if r.status_code:
        r.encoding = r.apparent_encoding

    # 获取并完善链接
    html = etree.HTML(r.text)
    Urls = html.xpath('/html/body/div/div[4]/div/dl/dd/a/@href')
    for i in range(len(Urls)):
        Urls[i] = mainUrl+Urls[i]

    return Urls


def mkDir(path):
    try:
        if os.path.exists(path):
            print(path+' 目录已存在！')
        else:
            os.mkdir(path)
            print(path+' 目录创建成功！')
    except:
        print('创建目录失败！')
        exit(0)


def down(url: str):
    r = requests.get(url)
    if r.status_code:
        r.encoding = r.apparent_encoding

    doc = pq(r.text)

    # 标题
    top = doc('div .bookname h1').text().split()

    if len(top) > 1:
        index = top[1].find('（')
        if index != -1:
            top = top[0]+' '+top[1][:index]
        else:
            top = ' '.join(top)
    else:
        top = top[0]

    # 内容
    text = doc('div #content').text()

    # 写入文件
    txtTop = saveDir+top+'.txt'
    try:
        if os.path.exists(txtTop):
            print(top+' 文件已存在！')
        else:
            with open(txtTop, 'w') as f:
                f.write(text)
                print(top+' 写入成功！')
    except:
        print('文件写入错误！')


if __name__ == '__main__':
    # 获取小说目录页Url
    noteUrl = getNoteUrl()
    # 获取小说名
    noteName = getNoteName(noteUrl)
    # 设置保存目录
    saveDir = os.getcwd()+'/'+noteName+'/'
    # 创建主目录
    mkDir(saveDir)
    # 获取章节页链接
    pageUrls = getPages(siteUrl, noteUrl)
    # 下载
    for i in pageUrls:
        down(i)
        time.sleep(0.1)
    print('爬取结束！')
