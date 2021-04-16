from demo import jsonDemo
from Analyzer import analyzer
import numpy as np
def dailyanalysis():
    timelist = jsonDemo.jsonreadtime()  # 每条评论的时间
    emotionlist = analyzer.giveEmotioanlSign("../elexicon.csv")  # 每条评论的情绪向量
    ret = []

    length1=len(timelist)
    timeemotion=[]
    for i in range(0,length1):
        timeemotion.append([timelist[i],emotionlist[i][0],emotionlist[i][1],emotionlist[i][2],emotionlist[i][3],emotionlist[i][4]
                            ,emotionlist[i][5],emotionlist[i][6],emotionlist[i][7],emotionlist[i][8]])
    timeemotion.sort(key=lambda x:x[0])
    # for item in timeemotion:
    #     print(item)
    #ret=timeemotion
    key=0

    for item in timeemotion :
        if int(item[0])//100>key:
            ret.append(item)
            current = len(ret) - 1
            key=int(item[0])//100
            ret[current][0]=key
        elif int(item[0])//100==key:
            current=len(ret)-1
            for i in range(1,10):
                ret[current][i]+=item[i]

    #这个是每日的情绪分析

    # for i in range(0,len(ret)):
    #     cnt=0
    #     for j in range(1,10):
    #         cnt+=ret[i][j]
    #     if cnt!=0:
    #         for j in range(1,10):
    #             ret[i][j]/=cnt

    #这个是提取每日主要情绪
    #第一个维度是日期第二个是情绪的代号
    dominantemotion=np.zeros((len(ret),2))
    for i in range(0,len(ret)):
        dominantemotion[i][0]=ret[i][0]
        max=1
        for j in range(1,10):
            if ret[i][j]>ret[i][max]:
                max=j
        if ret[i][max]!=0:
            dominantemotion[i][1]=max
        else:
            dominantemotion[i][1]=-1

    return dominantemotion

def dailyemotionsanalysis(emotion):
    timelist = jsonDemo.jsonreadtime()  # 每条评论的时间
    emotionlist = analyzer.giveEmotioanlSign("../elexicon.csv")  # 每条评论的情绪向量
    ret = []

    length1=len(timelist)
    timeemotion=[]
    for i in range(0,length1):
        timeemotion.append([timelist[i],emotionlist[i][0],emotionlist[i][1],emotionlist[i][2],emotionlist[i][3],emotionlist[i][4]
                            ,emotionlist[i][5],emotionlist[i][6],emotionlist[i][7],emotionlist[i][8]])
    timeemotion.sort(key=lambda x:x[0])
    # for item in timeemotion:
    #     print(item)
    #ret=timeemotion
    key=0

    for item in timeemotion :
        if int(item[0])//100>key:
            ret.append(item)
            current = len(ret) - 1
            key=int(item[0])//100
            ret[current][0]=key
        elif int(item[0])//100==key:
            current=len(ret)-1
            for i in range(1,10):
                ret[current][i]+=item[i]

    #这个是每日的情绪分析

    for i in range(0,len(ret)):
        cnt=0
        for j in range(1,10):
            cnt+=ret[i][j]
        if cnt!=0:
            for j in range(1,10):
                ret[i][j]/=cnt
    # for item in ret:
    #     print(item )
    selectedret=np.zeros((len(ret),2))
    for i in range(0,len(ret)):
        selectedret[i][0]=ret[i][0]
        selectedret[i][1]=ret[i][emotion]
    return selectedret
if __name__ == '__main__':
    dic = {0: "joy", 1: "sadness", 2: "anticipation", 3: "fear", 4: "anger", 5: "hopeful", 6: "trust", 7: "disgust",
           8: "surprise"}
    #emotionsanalysis这里传的参数就是情绪代号
    for n in range(0,9):
        list1=dailyemotionsanalysis(n+1)
        x=open("每天情绪"+dic[n]+".txt",'a')
        for item in list1:
            x.write(str(int(item[0]))+','+str(item[1])+"\n")
        print("完成"+dic[n])
