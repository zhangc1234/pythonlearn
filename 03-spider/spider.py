# -*- coding = utf-8 -*-
# @Time : 2022/3/16 9:01
# @Author : 张晨
# @File : spider.py
# @Software : PyCharm

import re       #正则表达式
from bs4 import BeautifulSoup     #网页解析，获取数据
import urllib.request, urllib.error  #制定URL 获取网页数据
import xlwt     #进行excel操作
import sqlite3  #进行SQLite数据库操作


findlink = re.compile(r'<a href="(.*?)">')         #创建正则表达式规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)         #创建正则表达式规则
findtitle = re.compile(r'<span class="title">(.*)</span>')
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findjudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?) </p>', re.S)

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getdata(baseurl)
    print(datalist)
    savepath = "豆瓣Top250.xls"
    # 3.保存数据
    saveData(datalist, savepath)

    # dbpath = r"G:\test.db"
    # saveData2DB(datalist, dbpath)
    # # askurl(baseurl)



 # 爬取网页
def getdata(baseurl):
    datalist = []
    print("爬取中~~~")
    for i in range(0, 10):       #调用页面10次
        url = baseurl + str(i*25)
        html = askurl(url)      #保存获取的网页源码
        # print(html)

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):           #查找符合要求的
            # print(item)           #测试 查看电影item
            data = []               #保存一步电影的信息
            item = str(item)
            # print(item)
            link = re.findall(findlink, item)[0]     #通过正则表达式查找指定字符串
            data.append(link)

            imgSrc = re.findall(findImgSrc, item)
            # imgSrc = re.sub('\[', "", str(imgSrc))
            data.append(imgSrc)
            # print(data)

            titles = re.findall(findtitle, item)
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("\xa0/\xa0", "")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')
            # print(data)
            rating = re.findall(findrating, item)[0]
            data.append(rating)

            judgeNum = re.findall(findjudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub(r'<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', "", bd)
            bd = re.sub(r'\xa0', "", bd)
            bd = re.sub('\.\.\.', "", bd)
            data.append(bd.strip())

            datalist.append(data)

    # print(datalist)
    print("爬取结束")
    return datalist


def askurl(url):
    # 得到一个指定url的网页内容,
    # 输入 网址 字符串格式；
    # 返回 html格式网页

    # head用户代理 告诉服务器，我们是什么类型机器，浏览器（本质上告诉服务器，可以接受什么水平的反馈）
    head = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=head)

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def saveData(datalist, savepath):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("豆瓣电影Top250", cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价数", "概况", "相关信息")
    print("保存excel中~~~~")
    for i in range(0, 8):
        worksheet.write(0, i, col[i])
    for i in range(0, 250):
        # print("第%d条" % (i+1))
        data = datalist[i]
        # print(type(datalist))
        # print(type(data))
        for j in range(0, 8):
            worksheet.write(i+1, j, data[j])

    workbook.save(savepath)
    print("save完成")


# 保存数据到数据库部分 注释掉
# def saveData2DB(datalist, dbpath):
#     init_db(dbpath)
#     print("存数据库中~~~")
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#     for data in datalist:
#         for index in range(len(data)):
#             # print(data[index])
#             data[index] = '"'+str(data[index])+'"'
#             # print(data[index])
#         sql = '''
#             insert into movie250(
#             info_link, pic_link, cname, ename, score, rated, instroduction,info)
#             values(%s)'''%",".join(data)
#         cur.execute(sql)
#         conn.commit()
#         # print(sql)
#     cur.close()
#     conn.close()
#
#
#
# def init_db(dbpath):
#     conn = sqlite3.connect(dbpath)
#     c = conn.cursor()
#     sql = '''
#         create table movie250
#         (
#         id integer primary key autoincrement,
#         info_link text,
#         pic_link text,
#         cname varchar,
#         ename varchar,
#         score numeric,
#         rated numeric,
#         instroduction text,
#         info text
#         )
#     '''
#     c.execute(sql)
#     conn.commit()
#     conn.close()
#


if __name__ == "__main__":
    main()

