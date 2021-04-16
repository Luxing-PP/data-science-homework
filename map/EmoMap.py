import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import shapefile
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
import random
from enum import Enum

from Analyzer.analyzer import emotions


class Emomap:
    dic = {"a": "b"}
    EM = ""
    plt.figure(figsize=(16, 8))
    m = Basemap(llcrnrlon=77,
                llcrnrlat=14,
                urcrnrlon=140,
                urcrnrlat=51,
                projection='lcc',
                lat_1=33,
                lat_2=45,
                lon_0=100)
    m.readshapefile('china-shapefiles\shapefiles\china', 'china', drawbounds=True)

    # m.drawcoastlines()
    def __init__(self, dic, EM):
        self.dic = dic
        self.EM = EM

    def color(emo, name):
        # a=set()
        # for state, info in zip(x.m.china, x.m.china_info):
        #     a.add(info['OWNER'])
        # if emo in a:
        #     return random.choice(['g', 'r', 'c', 'm', 'y', 'k'])
        # return 'r'

        e = emotions
        a = emo
        b = 0.0
        for each in dic.keys():
            if each == name:
                b = float(dic[each])
                break
        a=str(b)
        if a == "0.0":  # joy"yellow"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "ivory"
            # if 0.1 <= b < 0.2:
            #     return "lightyellow"
            # if 0.2 <= b < 0.3:
            #     return "yellow"
            # if 0.3 <= b < 0.4:
            #     return "y"
            # else:
            #     return "olive"
            return "yellow"
        if a == "1.0":  # sadness"black"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "whitesmoke"
            # if 0.1 <= b < 0.2:
            #     return "lightgrey"
            # if 0.2 <= b < 0.3:
            #     return "darkgrey"
            # if 0.3 <= b < 0.4:
            #     return "dimgrey"
            # else:
                 return "black"
        if a == "4.0":  # anger"r"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "mistyrose"
            # if 0.1 <= b < 0.2:
            #     return "salmon"
            # if 0.2 <= b < 0.3:
            #     return "r"
            # if 0.3 <= b < 0.4:
            #     return "firebrick"
            # else:
            #     return "darkred"
            return "r"
        if a == "7.0":  # disgust"m"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "pink"
            # if 0.1 <= b < 0.2:
            #     return "hotpink"
            # if 0.2 <= b < 0.3:
            #     return "orchid"
            # if 0.3 <= b < 0.4:
            #     return "m"
            # else:
            #     return "darkmagenta"
            return "m"
        if a == "5.0":  # hopeful"orange"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "lemonchiffon"
            # if 0.1 <= b < 0.2:
            #     return "khaki"
            # if 0.2 <= b < 0.3:
            #     return "gold"
            # if 0.3 <= b < 0.4:
            #     return "orange"
            # else:
            #     return "goldenrod"
            return "orange"
        if a == "2.0":  # anticipation"g"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "mintcream"
            # if 0.1 <= b < 0.2:
            #     return "lightgreen"
            # if 0.2 <= b < 0.3:
            #     return "limegreen"
            # if 0.3 <= b < 0.4:
            #     return "lime"
            # else:
                 return "g"
        if a == "3.0":  # fear"grey"
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "whitesmoke"
            # if 0.1 <= b < 0.2:
            #     return "lightgrey"
            # if 0.2 <= b < 0.3:
            #     return "darkgrey"
            # if 0.3 <= b < 0.4:
            #     return "dimgrey"
            # else:
            #     return "black"
            return "grey"
        if a == "8.0":  # surprise
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "azure"
            # if 0.1 <= b < 0.2:
            #     return "lightcyan"
            # if 0.2 <= b < 0.3:
            #     return "paleturquoise"
            # if 0.3 <= b < 0.4:
            #     return "cyan"
            # else:
            #     return "darkcyan"
            return "c"
        if a == "6.0":  # trust
            # if b == 0:
            #     return "w"
            # if b < 0.1:
            #     return "lavender"
            # if 0.1 <= b < 0.2:
            #     return "cornflowerblue"
            # if 0.2 <= b < 0.3:
            #     return "royalblue"
            # if 0.3 <= b < 0.4:
            #     return "b"
            # else:
            #     return 'darkblue'
            return "b"

    def draw(self,n,m,emos):
        ax = plt.gca()
        for state, info in zip(self.m.china, self.m.china_info):
            name = info['OWNER'][:2]  # 用来对应省份
            # poly = Polygon(state, facecolor=Emomap.color(self.EM, name), edgecolor=Emomap.color(self.EM, name))
            poly = Polygon(state, facecolor=Emomap.color(self.EM,name), edgecolor=Emomap.color(self.EM,name))
            ax.add_patch(poly)
        plt.savefig("总体阶段"+".jpg")
        # plt.savefig("第"+str(n+1)+" 阶段" + ".jpg")
        # plt.show()
    # provinces = set()
    # for shapedict in m.china_info:
    #     statename = shapedict['OWNER']
    #     provinces.add(statename.replace("\x00",""))
    # print(provinces)


if __name__ == '__main__':
    emos = {0: "joy", 1: "sadness", 2: "anticipation", 3: "fear", 4: "anger", 5: "hopeful", 6: "trust", 7: "disgust",
            8: "surprise"}

    # for n in range(0,4):
    # for m in range(0, 9):
    x = open("总体阶段"+".txt", encoding='ansi')
    dic = {}
    keys = []  # 用来存储读取的顺序
    for line in x:
        v = line.strip().split(',')
        dic[v[0]] = v[1]
        keys.append(v[0])
    x.close()
    x = Emomap(dic,"-1")
    x.draw(0,0,emos)
    print("完成" + "总体阶段")
# a=set()
# for state,info in zip(x.m.china,x.m.china_info):
#     a.add(info['OWNER'].replace("\x00",""))
# print(a)
