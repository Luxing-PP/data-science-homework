# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
def line():
    dic2={"joy":"y","sadness":"black","anger":"r","disgust":"m","hopeful":"orange","anticipation":"g","fear":"grey","surprise":"c","trust":"b"}
    dic = {0: "joy", 1: "sadness", 2: "anticipation", 3: "fear", 4: "anger", 5: "hopeful", 6: "trust", 7: "disgust",
           8: "surprise"}
    emos={}
    plt.figure(figsize=(100, 50))
    for n in range(0,9):
        x=open("每天情绪"+dic[n]+".txt",'r')
        for line in x:
            v = line.strip().split(',')
            emos[v[0]] = v[1]
        a=list(range(0,len(emos.keys())))
        b=list(emos.values())
        b_float = []
        a_day=[]
        # for num in a:
        #     a_day.append(num[2:])
        for num in b:
            b_float.append(float(num))
        # a=[0,1,2,3,4,5,6,8,9,10]
        # b=[0.1,0.5,0.3,0.2,0.1,0.5,0.6,0.45,0.5,0.1]
        # plt.xlabel(emos.keys, fontsize=14)
        # plt.ylabel([0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17],fontsize=14)
        plt.plot(a,b_float,color=dic2[dic[n]],label=dic[n])
        plt.xlabel('day', fontsize=14)
        plt.ylabel('num', fontsize=4)
        # x_major_locator = MultipleLocator(0.1)
        # y_major_locator = MultipleLocator(1)
        # ax = plt.gca()
        # # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)
        # # 把x轴的主刻度设置为1的倍数
        # ax.yaxis.set_major_locator(y_major_locator)
        # plt.savefig(dic[n]+".png")
    plt.legend(loc="best")
    plt.savefig("所有情绪集合"+".png")
    plt.show()
if __name__ == '__main__':
    line()