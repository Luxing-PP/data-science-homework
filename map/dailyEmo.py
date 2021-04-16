# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
def rc():
    dic={0:"joy",1:"sadness",2:"anticipation",3:"fear",4:"anger",5:"hopeful",6:"trust",7:"disgust",8:"surprise"}
    labels = dic.values()
    x=open("每天的代表情绪.txt","r",encoding="Utf-8")
    dic = {}
    joy=0
    sadness=0
    anticipation=0
    fear=0
    anger=0
    hopeful=0
    trust=0
    disgust=0
    surprise=0
    for line in x:
        v = line.strip().split(',')
        dic[v[0]] = v[1]
    x.close()
    for k in dic.keys():
        dic[k]=str(int(dic[k])-1)
    for value in dic.values():
        if value == "0":
            joy+=1
        if value == "1":
            sadness += 1
        if value == "2":
            anticipation += 1
        if value == "3":
            fear += 1
        if value == "4":
            anger += 1
        if value == "5":
            hopeful += 1
        if value == "6":
            trust += 1
        if value == "7":
            disgust+=1
        if value == "8":
            surprise+=1
    sizes=[joy,sadness,anticipation,fear,anger,hopeful,trust,disgust,surprise]
    plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
    plt.title("emo in days")
    plt.savefig("主要情绪在每天的占比"+".jpg")

if __name__ == '__main__':
    rc()