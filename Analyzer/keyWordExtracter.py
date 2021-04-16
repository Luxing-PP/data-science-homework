import databaseHelper
from pyhanlp import *

if __name__ == '__main__':
    database = databaseHelper.database()
    keyArticle = database.select("url", "*", "WHERE comsum>='88'")
    articles = keyArticle.fetchall()

    for article in articles:
        article_id = article[0]
        comments = database.select("comments", "*", "WHERE urlid = {}".format(article_id)).fetchall()
        for comment in comments:
            num = (len(comment) // 10) + 1
            keywords = HanLP.extractKeyword(comment[2], num)
            for keyword in keywords:
                try:
                    flag = database.insert_keyword(keyword)
                    if flag == -1:
                        k_id, word, time = database.select("keyword", "*", "WHERE word='{}'".format(keyword)).fetchone()
                        time = time + 1
                        database.update("keyword", "times={}".format(time), "id={}".format(k_id))
                        print("关键词 {} 次数{}".format(keyword, time))
                        continue
                    elif flag == -2:
                        print("Interesting")
                        continue
                except Exception as e:
                    continue
    database.close()
