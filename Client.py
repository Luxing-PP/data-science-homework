import re

from pymysql import DataError
from ReptileStrategy import LoadMissException
from ReptileStrategy import RequestMissException
import ReptileStrategy
import databaseHelper
from util import Constant
from util import util


# 主程序
def insertComment(database, comment, url):
    # 4.0 准备数据 [urlid, content, time]
    #             [cmnProvince, cmntime, cmn.get('content')]
    oneUrlData = database.select("url", None, "WHERE url LIKE \"{0}\"".format(url)).fetchone()
    urlid = oneUrlData[0]
    # 4.2 插入
    for content in comment[1]:
        try:
            # comment[[cmnProvince, cmntime, cmn.get('content')]
            # INSERT INTO comments (urlid,content,time,province)
            database.insert_comments([urlid, content[2], content[1], content[0]])
        except DataError as e:
            print(content[2])
            print(e)
        except Exception as e:
            # 其他问题强制跳过
            raise e


def makeNewOriginUrl(oriUrl, stime, etime, page=1):
    indexE = oriUrl.find("etime")
    indexS = oriUrl.find("stime")
    oldE = oriUrl[indexE + 6:indexE + 26]
    oldS = oriUrl[indexS + 6:indexS + 26]
    oriUrl = oriUrl.replace(oldE, etime)
    oriUrl = oriUrl.replace(oldS, stime)
    oriUrl = oriUrl[0:oriUrl.find("page=") + 5] + str(page)
    return oriUrl


def startWithUrl(oriURL):
    # 取数据库
    database = databaseHelper.database()
    listReptile = ReptileStrategy.Sina_Strategy(oriURL)
    urlSet = listReptile.getURL()
    stime = oriURL[oriURL.find("stime") + 6:oriURL.find("stime") + 26]
    etime = oriURL[oriURL.find("etime") + 6:oriURL.find("etime") + 26]
    page = int(oriURL[-1])
    isTimeChanged = False

    if len(urlSet) == 0:
        print("oriList is Empty！ " + oriURL)
        if page <= 12:
            page = page+1
            return makeNewOriginUrl(oriURL, stime, etime, page)

    # 永动爬虫机
    try:
        while True:
            # 静态解析做第一轮快速爬取 更新etime
            while len(urlSet) > 0:
                onePageUrl = urlSet.pop()
                # 1. 以静态模式加载网页
                try:
                    onePageReptile = ReptileStrategy.Sina_Strategy(onePageUrl, Constant.constant.MODE_OF_STATIC)
                except Exception as e:
                    print(e)
                    continue

                values = onePageReptile.get_Simple_Content()

                if not etime == values[3]:
                    isTimeChanged = True
                    etime = values[3]

                try:
                    # [[comatd ,comment_sum], comment[[cmnProvince, cmntime, cmn.get('content')]]]
                    comment = onePageReptile.get_Comment_Request()
                except RequestMissException as e:
                    # 记录
                    e.save()
                    continue

                # 2.检查评论是否符合要求 [ [attendance ,comment_sum], comment[cmnProvince, cmntime, content] ]
                if comment[0][1] == 0:
                    # 没评论，营养不存了
                    print("放弃:" + onePageReptile.originalURL)
                    continue
                else:
                    print("接受:" + onePageReptile.originalURL)

                # 3.插入URL
                # 3.1 准备数据 values = [source,time,url,comsum,comatd]
                # 提前因为要更新etime= =
                values.pop()  # 去掉etime
                values.append(comment[0][1])
                values.append(comment[0][0])

                # 3.2 保存URL
                # INSERT INTO url (source,time,url,comsum,comatd)
                flag = database.insert_url(values)
                if flag == -1:
                    print("数据重复")
                    continue

                # 4.插入评论
                try:
                    insertComment(database, comment, values[2])
                except Exception as e:
                    print(e)
                    continue

            # 一个新闻List处理完了，处理下一个新闻List
            nextPage = listReptile.getNextPage()
            oriURL = nextPage
            print("新一页" + oriURL)
            listReptile = ReptileStrategy.Sina_Strategy(oriURL)
            urlSet = listReptile.getURL()

            if len(urlSet) == 0:
                # 一页里找不到文章了
                print("大概爬完了")
                if isTimeChanged:
                    return makeNewOriginUrl(oriURL, stime, etime, 1)
                else:
                    page += 1
                    print("啥也没变= =")
                    return makeNewOriginUrl(oriURL, stime, etime, page)
    finally:
        if database.cur is not None:
            database.close()


if __name__ == '__main__':
    # 起始链接
    # https://search.sina.com.cn/?q=%E8%82%BA%E7%82%8E&range=all&c=news&sort=time
    # https://search.sina.com.cn/?q=%E6%96%B0%E5%86%A0&c=news&range=all&stime=2020-02-10&etime=2020-02-10&time=2020&page=20
    # todo 重试超时
    # todo 试试2019
    Sina_oriURL = ("https://search.sina.com.cn/?"
                   "q=%E6%96%B0%E5%86%A0&"
                   "c=news&"
                   "range=all&"
                   "num=20&"
                   "stime=2020-03-10+00:00:00&"
                   "etime=2020-03-11+16:05:00&"
                   "time=2020&"
                   "page=10"
                   )


    while True:
        print("新起点 " + Sina_oriURL)
        Sina_oriURL = startWithUrl(Sina_oriURL)
