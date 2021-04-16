import ReptileStrategy
import databaseHelper
import Constant
from pymysql import DataError


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
            if len(content) == 4:
                database.insert_keycom([urlid, content[2], content[1], content[0], content[3]])
            else:
                print(content)
        except DataError as e:
            print(content[2])
            print(e)
        except Exception as e:
            # 其他问题强制跳过
            print(content)
            raise e


if __name__ == '__main__':
    # 为了爬出评论的点赞数临时构建的二号Client
    database = databaseHelper.database()
    urlSet = database.select("url", "url", "").fetchall()
    checked = False
    for onePageUrl in urlSet:
        onePageUrl = onePageUrl[0]

        if onePageUrl == "https://news.sina.com.cn/c/2020-04-15/doc-iircuyvh7936923.shtml":
            checked = True
        else:
            print(onePageUrl)

        if checked:
            try:
                onePageReptile = ReptileStrategy.Sina_Strategy(onePageUrl, Constant.constant.MODE_OF_STATIC)
            except Exception as e:
                print(e)
                continue

            values = onePageReptile.get_Simple_Content()

            try:
                # [[comatd ,comment_sum], comment[[cmnProvince, cmntime, cmn.get('content')]]]
                comment = onePageReptile.get_Comment_Request()
            except ReptileStrategy.RequestMissException as e:
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

            # 4.插入评论
            try:
                insertComment(database, comment, values[2])
            except Exception as e:
                print(e)
                continue
