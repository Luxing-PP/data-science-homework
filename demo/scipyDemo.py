import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

'''
Scipy 库的参考代码
'''

if __name__ == '__main__':
    # cdf = stats.norm.cdf(0)  # Cumulative distribution function of the given RV   相当于分位点
    # pdf = stats.norm.pdf(0)  # Probability density function at x of the given RV  概率密度函数

    cdf2 = stats.chi2.cdf(6.635, df=1)  # 6.635 是α为0.01 的上分位点，cdf=0.99 正确
    cdf_inv = stats.chi2.isf(0.01, df=1) # 逆残存6.6XX 正确

    comsum, articleNum = np.loadtxt(r"../data/Count.csv", delimiter=",", usecols=(0, 1), unpack=True, dtype="i4")
    data = np.loadtxt(r"../data/URL.csv", delimiter=",", usecols=5, dtype="i4")

    # 绘制原始数据的频率直方图
    hist, bins = np.histogram(data, 500, normed=True)
    bins = 0.5 * (bins[1:] + bins[:-1])
    plt.plot(bins, hist)

    # 绘制拟合曲线
    df, loc, scale = stats.chi2.fit(data)
    print("df={} loc={} scale={}".format(df, loc, scale))
    pdf = stats.chi2.pdf(bins, df=df, loc=loc, scale=scale)
    plt.plot(bins, pdf, 'g--')  # 红色虚线

    # 卡方拟合优度检验
    outcome = stats.kstest(data, lambda x: stats.chi2.cdf(x, df=df, loc=loc, scale=scale))
    print(outcome)
    plt.show()

    # 近似为获取上分位点

    cdf_inv = stats.chi2.isf(0.3, df=df, loc=loc, scale=scale)
    print("30%分位点为", end="")
    print(cdf_inv)






