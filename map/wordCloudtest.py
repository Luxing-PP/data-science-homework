import matplotlib.pyplot as plt
import jieba
import xlrd
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
class wcd:
    # workBook = xlrd.open_workbook('../data/TagSupplement2.xlsx')

    def beTXT(self):
        global file_handle
        allSheetNames = self.workBook.sheet_names()
        print(allSheetNames)

        # 1.2 按索引号获取sheet的名字（string类型）
        sheet1Name = self.workBook.sheet_names()[0]
        print(sheet1Name)

        # 2. 获取sheet内容
        ## 2.1 法1：按索引号获取sheet内容
        sheet1_content1 = self.workBook.sheet_by_index(0)  # sheet索引从0开始
        for n in range(1,sheet1_content1.nrows):
            x=sheet1_content1.cell(n,1).value
            file_handle = open('wd.txt', mode='a')
            for m in range(0,int(sheet1_content1.cell(n,2).value)):
                file_handle.write(x+" ")
        return file_handle
    def create(self):
        txt=open('../map/wd.txt','r').read()
        mask_pic = Image.open("u=1302885550,4025528368&fm=26&gp=0.png")
        mask_pic_array = np.array(mask_pic)
        plt.figure(figsize=(16, 9))
        stopwords = set(STOPWORDS)
        stopwords.add("美国")
        stopwords.add("说")
        stopwords.add("没")
        stopwords.add("没有")
        wordcloud = WordCloud(font_path="simsun.ttf",
                              mask=mask_pic_array,
                              stopwords=stopwords,
                              collocations=False,
                              background_color="white").generate(txt)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        # plt.savefig('口罩词云.jpg')
        plt.show()

if __name__ == '__main__':
    x = wcd
    x.create(x)
