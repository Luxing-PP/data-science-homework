import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

if __name__ == '__main__':
    # # 1.重点新闻筛选
    # # 读取已手动去除离群点的数据源,
    # data = np.loadtxt(r"../data/data.csv", delimiter=",", usecols=5, dtype="i4")
    #
    # # 绘制原始数据的频率直方图
    # hist, bins = np.histogram(data, 300, normed=True)
    # bins = 0.5 * (bins[1:] + bins[:-1])
    # plt.plot(bins, hist, label="original values")
    #
    # # 拟合并绘制曲线（按卡方分布拟合）
    # df, loc, scale = stats.chi2.fit(data)
    # print("df={} loc={} scale={}".format(df, loc, scale))
    # pdf = stats.chi2.pdf(bins, df=df, loc=loc, scale=scale)
    # plt.plot(bins, pdf, 'g--', label="polyfit values")  # 绿色虚线
    # plt.xlabel("ranks")
    # plt.ylabel("probability")
    # plt.legend(loc=1)
    # plt.title("article-comsum's chi2 polyfit")
    #
    # # 卡方拟合优度检验
    # static, p = stats.kstest(data, lambda x: stats.chi2.cdf(x, df=df, loc=loc, scale=scale))
    # print(p)
    # plt.show()
    #
    # # 在p值大于期望的前提下获取上分位点
    # if p >= 5e-8:
    #     cdf_inv = stats.chi2.isf(0.3, df=df, loc=loc, scale=scale)
    #     print("30%分位点为", end="")
    #     print(cdf_inv)
    # else:
    #     print("拟合的太屑")

    # 2.在重点新闻 30W-->22W  删除0点赞 22W-->11W 筛选字长11W-->6W 拟合点赞量
    #     TODO 以下为数据库语句仅供代码检查参考
    #       DELETE FROM comment WHERE length(content)<=50
    #       DELETE FROM keycom WHERE ranks = 0
    #       DELETE FROM url WHERE comsum <= 88

    # 读取已手动去除离群点(ranks = 0-5 or ranks>8000)的数据源,
    data = np.loadtxt(r"../data/ranks.csv", delimiter=",", usecols=0, dtype="i4")

    # 绘制原始数据的频率直方图
    hist, bins = np.histogram(data, 2000, normed=True)
    bins = 0.5 * (bins[1:] + bins[:-1])
    plt.plot(bins, hist, label="original values")

    # 拟合并绘制曲线（按卡方分布拟合）
    df, loc, scale = stats.chi2.fit(data)
    print("df={} loc={} scale={}".format(df, loc, scale))
    pdf = stats.chi2.pdf(bins, df=df, loc=loc, scale=scale)
    plt.plot(bins, pdf, 'g--', label="polyfit values")  # 绿色虚线
    plt.xlabel("ranks")
    plt.ylabel("probability")
    plt.legend(loc=1)
    plt.title("comment-rank's chi2 polyfit")

    # 卡方拟合优度检验
    static, p = stats.kstest(data, lambda x: stats.chi2.cdf(x, df=df, loc=loc, scale=scale))
    plt.show()

    cdf_inv = stats.chi2.isf(0.6, df=df, loc=loc, scale=scale)
    print("40%分位点为", end="")  # 120
    print(cdf_inv)
