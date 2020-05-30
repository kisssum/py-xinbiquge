from requests_html import HTMLSession
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
    return HTMLSession().get(url).html.find('#info h1')[0].text


def getPages(mainUrl, noteUrl):
    Urls = []

    # 获取所有a节点
    r = HTMLSession().get(noteUrl).html.find('#list a')

    # 完善链接
    for i in r:
        Urls.append(mainUrl+''.join(i.links))

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
    # 获取网页
    r = HTMLSession().get(url).html

    # 标题
    top = r.find('.bookname h1')[0].text
    top = top.split()
    if len(top) > 1:
        index = top[1].find('（')
        if index != -1:
            top = top[0]+' '+top[1][:index]
        else:
            top = ' '.join(top)
    else:
        top = top[0]

    # 获取内容
    text = r.find('#content')[0].text

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
    # 获取章节页链接
    pageUrls = getPages(siteUrl, noteUrl)
    # 设置保存目录
    saveDir = os.getcwd()+'/'+noteName+'/'
    # 创建主目录
    mkDir(saveDir)
    # 下载
    for i in pageUrls:
        down(i)
        time.sleep(0.1)
    print('爬取结束！')
