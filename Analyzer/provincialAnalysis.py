from demo import jsonDemo
from Analyzer import analyzer
import numpy as np


def provincialemotion(mode):
    #default:全阶段 mode==1:第一阶段 2：第二阶段 3：第三阶段 4：第四阶段
    oldprovincelist = jsonDemo.jsonreadprovince()  # 存放了每个评论的省份,总共11619条评论
    timelist=jsonDemo.jsonreadtime()#每条评论的时间
    oldemotionlist = analyzer.giveEmotioanlSign("../elexicon.csv")  # 每条评论的情绪向量
    length1 = len(oldprovincelist)  # 筛选前总条数
    provincelist=[]
    emotionlist=[]
    if mode==1:
        for i in range(0,length1):
            if int(timelist[i])<20012300:
                emotionlist.append(oldemotionlist[i])
                provincelist.append(oldprovincelist[i])
    elif mode==2:
        for i in range(0, length1):
            if 20012300 <= int(timelist[i]) < 20020700:
                emotionlist.append(oldemotionlist[i])
                provincelist.append(oldprovincelist[i])
    elif mode==3:
        for i in range(0, length1):
            if 20020700 <= int(timelist[i]) < 20021300:
                emotionlist.append(oldemotionlist[i])
                provincelist.append(oldprovincelist[i])
    elif mode==4:
        for i in range(0, length1):
            if  int(timelist[i]) >= 20021300:
                emotionlist.append(oldemotionlist[i])
                provincelist.append(oldprovincelist[i])
    else:
        emotionlist=oldemotionlist
        provincelist=oldprovincelist
    # print(len(provincelist))
    # provinces = []
    # for item in provincelist:
    #     if not (item in provinces):
    #         provinces.append(item)
    # length1 = len(provinces)  # 省份数量:34
    # print(length2)
    length2=len(emotionlist)
    provincedict = {'北京': 0, '浙江': 1, '广东': 2, '江苏': 3, '上海': 4, '四川': 5, '湖南': 6, '内蒙': 7, '陕西': 8, '山东': 9, '甘肃': 10,
                    '江西': 11, '河北': 12,
                    '吉林': 13, '安徽': 14, '河南': 15, '山西': 16, '湖北': 17, '重庆': 18, '黑龙': 19, '广西': 20, '辽宁': 21, '天津': 22,
                    '新疆': 23, '海南': 24,
                    '云南': 25, '福建': 26, '贵州': 27, '宁夏': 28, '香港': 29, '青海': 30, '台湾': 31, '西藏': 32, '澳门': 33}
    allprovinces = ['北京', '浙江', '广东', '江苏', '上海', '四川', '湖南', '内蒙', '陕西', '山东', '甘肃', '江西', '河北', '吉林', '安徽', '河南',
                    '山西', '湖北', '重庆', '黑龙', '广西', '辽宁', '天津', '新疆', '海南', '云南', '福建', '贵州', '宁夏', '香港', '青海', '台湾',
                    '西藏', '澳门']
    provinceemotions = np.zeros((34, 9))
    # for item in provinces:
    #     print(item)

    for i in range(0, length2):
        if provincelist[i] in allprovinces:
            for j in range(0, 9):
                provinceemotions[provincedict[provincelist[i]]][j] += emotionlist[i][j]
    #print(provinceemotions[32])
    for i in range(0, 34):
        cnt = 0
        for j in range(0, 9):
            cnt+=provinceemotions[i][j]
        for j in range(0,9):
            if cnt!=0:
                provinceemotions[i][j] /= cnt
    return provinceemotions


if __name__ == '__main__':
    allprovinces = ['北京', '浙江', '广东', '江苏', '上海', '四川', '湖南', '内蒙', '陕西', '山东', '甘肃', '江西', '河北', '吉林', '安徽', '河南',
                    '山西', '湖北', '重庆', '黑龙', '广西', '辽宁', '天津', '新疆', '海南', '云南', '福建', '贵州', '宁夏', '香港', '青海', '台湾',
                    '西藏', '澳门']

    dic={0:"joy",1:"sadness",2:"anticipation",3:"fear",4:"anger",5:"hopeful",6:"trust",7:"disgust",8:"surprise"}
    # for n in range(0,4):
    #     list1 = provincialemotion(n+1)
    #     x=open("第"+str(n+1)+" 阶段"+".txt",'a')
    #     for i in range(0,len(list1)):
    #         x.write(allprovinces[i]+","+str(np.argmax(list1[i]))+".0"+"\n")
    # for n in range(0,4):
    #     list1 = provincialemotion(n+1)
    #     for m in range(0,9):
    #         x=open("第"+str(n+1)+" 阶段"+dic[m]+".txt",'a')
    #         for i in range(0,len(list1)):
    #             x.write(allprovinces[i]+","+str(list1[i][m])+"\n")  #找出每一个阶段每一个省市每一个情绪的值
        # print(allprovinces[i],',',list1[i])
    # list1 = provincialemotion(0)
    # for m in range(0, 9):
    #     x=open("总体阶段"+dic[m]+".txt",'a')
    #     for i in range(0,len(list1)):
    #         x.write(allprovinces[i]+','+str(list1[i][m])+'\n')
    list1 = provincialemotion(0)
    x = open("总体阶段"+ ".txt", 'a')
    for i in range(0,len(list1)):
        x.write(allprovinces[i]+','+str(np.argmax(list1[i]))+".0"+"\n")



    # joy = 0
    # sadness = 1
    # anticipation = 2
    # fear = 3
    # anger = 4
    # hopeful = 5
    # trust = 6
    # disgust = 7
    # surprise = 8