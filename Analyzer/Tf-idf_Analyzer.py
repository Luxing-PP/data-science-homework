
import jieba
import jieba.analyse
import csv

from typing import Dict
from demo import jsonDemo
import numpy as np
from Analyzer import analyzer


# 思路：评论统计数据文件xxx.csv 每一行对应拥有一个情绪的评论，格式：[emotion],[counts]
#     keywords已经统计出来了，每一行格式[keyword],[counts]
#     计算tfidf然后返回

def caltimes():
    keywordlist = []
    wordfile = csv.reader(open("../elexicon.csv", 'r',encoding='utf-8'))
    for item in wordfile:
        keywordlist.append(item[1])
    commentlist = jsonDemo.jsonread()
    hittimes = np.zeros(len(keywordlist))
    for item in commentlist:
        for i in range(0, len(keywordlist)):
            hittimes[i] += item.count(keywordlist[i])
    return hittimes


def calcomments():
    keywordlist = []
    wordfile = csv.reader(open("../elexicon.csv", 'r',encoding='utf-8'))
    for item in wordfile:
        keywordlist.append(item[1])
    commentlist = jsonDemo.jsonread()
    hittimes = np.zeros(len(keywordlist))
    for item in commentlist:
        for i in range(0, len(keywordlist)):
            if keywordlist[i] in item:
                hittimes[i] += 1
    return hittimes


def tfidfCounter():
    edict = {'joy': 0, 'sadness': 1, 'anticipation': 2, 'fear': 3, 'anger': 4, 'hopeful': 5, 'trust': 6, 'disgust': 7,
             'surprise': 8}
    totalwords = 0
    keywordlist = []
    emotionlist = []
    wordfile = csv.reader(open("../elexicon.csv", 'r',encoding='utf-8'))
    for item in wordfile:
        keywordlist.append(item[1])
        emotionlist.append(item[2])
    commentlist = jsonDemo.jsonread()
    cnt = len(commentlist)

    for item in commentlist:  # 先统计总词频
        keywords = jieba.analyse.extract_tags(item, topK=15)
        totalwords += len(keywordlist)
    tfidflist = []
    freqlist = caltimes()
    hitfilelist = calcomments()

    for i in range(0, len(keywordlist)):
        tfidflist.append(
            (freqlist[i] / totalwords) * np.log(len(commentlist) / (1 + hitfilelist[edict[emotionlist[i]]])))
    return tfidflist
def sorter():
    with open("../weights",'r')as keys:
        list1=[[-1,0]]
        for item in keys:
            list1.append([float(item.rstrip()),0])
        # for item in list1:
        #     print(item)
        n=len(list1)
        list2=np.zeros(n)
        list2[0]=-1
        for i in range(1,n):
            max=0
            for j in range(1,n):
                if list1[j][0]>=list1[max][0] and list1[j][1]==0:
                    max=j
            list1[max][1]=1
            list2[max]=i

    keys.close()
    return list2
def countweigh():
    keywordlist = []
    wordfile = csv.reader(open("../elexicon.csv", 'r', encoding='utf-8'))
    for item in wordfile:
        keywordlist.append([item[1],item[2],0])
    rnklist=[]
    with open("../ranks")as ranks:
        for item in ranks:
            rnk=float(item.rstrip())
            rnklist.append(rnk)
        for i in range(0,len(keywordlist)):
            if rnklist[i]<1195:
                keywordlist[i][2]=1
            elif rnklist[i]<2390:
                keywordlist[i][2]=0.75
            elif rnklist[i]<3585:
                keywordlist[i][2]=0.5
            else:
                keywordlist[i][2]=0.25
        ranks.close()
    return keywordlist
if __name__ == '__main__':
     # list1=tfidfCounter()
     # print(len(list1))
     # print('\n'+'datas\n')
     # for item in list1:
     #     print(item)
     #     #print('\n')
     # list2=sorter()
     # for item in list2:
     #     print(item)
     keywords=countweigh()
     for item in keywords:
         print(item)
