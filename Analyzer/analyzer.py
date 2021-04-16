from util import articleSegment
import databaseHelper
import csv
import numpy as np
import jieba
import pandas as pd
from demo import jsonDemo
from enum import Enum


class emotions(Enum):
    joy = 0
    sadness = 1
    anticipation = 2
    fear = 3
    anger = 4
    hopeful = 5
    trust = 6
    disgust = 7
    surprise = 8


def vectorization(time, content):
    """
    :param time: 时间维
    :param content: 文章
    :return: vector(list) n+1维
             失败时返回 [-1,....]
    """
    database = databaseHelper.database()
    seg = articleSegment.segment(content)
    anger, disgust, fear, sadness, surprise, trust, hopeful = 0, 0, 0, 0, 0, 0, 0

    if len(seg) == 0:
        return ["-1", '0', '0', '0', '0', '0', '0', '0']

    for term in seg:
        try:
            # 词典碰撞
            cur = database.select("eLexicon", None, "WHERE word LIKE \"{0}\"".format(term))
            ob = cur.fetchall()

            if ob is None:
                # 词典里没有
                continue
            else:
                for dimension in ob:
                    d_id, type, score, hit = dimension[0], dimension[2], dimension[3], dimension[4] + 1
                    database.update("eLexicon", "hit={}".format(hit), "id={}".format(d_id))
                    print(term, end="")
                    print(type, end="")
                    print(score)
                    if type == 'anger':
                        anger += score
                    elif type == 'disgust':
                        disgust += score
                    elif type == 'fear':
                        fear += score
                    elif type == 'sadness':
                        sadness += score
                    elif type == 'surprise':
                        surprise += score
                    elif type == 'trust':
                        trust += score
                    elif type == 'joy' or type == 'anticipation':
                        hopeful += score / 2
                    elif type == 'hopeful':
                        hopeful += score
                    else:
                        print("Exception")
        except Exception as e:
            print(e)

    database.close()

    if anger == 0 and disgust == 0 and fear == 0 and sadness == 0 and surprise == 0 and trust == 0 and hopeful == 0:
        return ["-1", '0', '0', '0', '0', '0', '0', '0']
    else:
        return list(map(str, [time, anger, disgust, fear, sadness, surprise, trust, hopeful]))


def giveEmotioanlSign(path):
    commentList = jsonDemo.jsonread()  # 读取评论
    cnt1 = len(commentList)
    cnt2 = 0
    edict = {'joy': 0, 'sadness': 1, 'anticipation': 2, 'fear': 3, 'anger': 4, 'hopeful': 5, 'trust': 6, 'disgust': 7,
             'surprise': 8}
    wordfile = csv.reader(open(path, 'r',encoding='utf-8'))
    list1 = []  # list1存放的是关键词及其代表情绪
    for item in wordfile:
        # list1[i][0]=item[1]#第一个存放了keyword
        # list1[i][1]=item[2]#第二个存放了对应情绪
        list1.append([item[1], item[2]])
        cnt2 += 1
    list2 = np.zeros((cnt1, 9))  # list2存放的是每个评论对应的情绪相关词hit的次数
    i = 0
    # for item in wordfile:
    #     print(item)
    #     # list1[i][0]=item[1]#第一个存放了keyword
    #     # list1[i][1]=item[2]#第二个存放了对应情绪
    #     list1.append([item[1], item[2]])
    weightslist=[]
    with open("../newelexicon",'r',encoding='utf-8')as weights:
        for item in weights:
            item = item.replace('[', '')
            item = item.replace(']', '')
            item = item.rstrip()
            weightslist.append(float(item.split(',')[2]))
        weights.close()
    for i in range(0,cnt1):
        for j in range(0, cnt2):
            if list1[j][0] in commentList[i]:
                list2[i][edict[list1[j][1]]] += weightslist[j]

    # list3 = []
    # for i in range(0, cnt1):
    #    maxidx = 0
    #    for j in range(0, 9):
    #        if list2[i][j] > list2[i][max]:
    #            maxidx = j
    #    list3.append(maxidx)

    return list2


def countEmotiontxts():
    commentsWithTag = giveEmotioanlSign("../elexicon.csv")
    emotionComments = np.zeros(9)
    for item in commentsWithTag:
        for i in range(0, 9):
            if item[i] != 0:
                emotionComments[i] += 1
    return emotionComments


if __name__ == '__main__':
    database_o = databaseHelper.database()
    # commentList = database_o.select("keycom", None, "WHERE time BETWEEN 20021000 AND 20021324").fetchall()
    commentList = database_o.select("keycom", None, "").fetchall()

    file = open("../SecondPhase.txt", "a", encoding='utf-8')

    for comment in commentList:
        content = comment[2]
        time = comment[4]
        vector = vectorization(time, content)
        if vector[0] != "-1":
            file.write(";".join(vector) + "\n")
    file.close()
