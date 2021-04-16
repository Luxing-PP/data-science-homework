# from pyhanlp import *


def segment(article):
    """
    根据词性把需要的词挑出来(n == "n" or n == "v" or n == "a" or n == "vi" or n == 'vn' or n == 'ad')
    todo check 有没有其他词性
    :param article: 待分词的任意 字符串
    :return: res: 一个个词的LIST
    """

    res = []
    seg = HanLP.segment(article)
    for term in seg:
        n = str(term.nature)
        # if nature == "n" or "v" or "a" or "vi":
        if n == "n" or n == "v" or n == "a" or n == "vi" or n == 'vn' or n == 'ad':
            res.append(term.word)
        elif n == "d" or n == "t" or n == "p" or n == "m" or n == "udeng" or n == "ude1":
            # 助词时间等不管
            pass
        else:
            # 别的好像也没有太重要的
            print("Unexpected nature " + n)
            pass
    return res


if __name__ == '__main__':
    res = segment("欢迎新老师生前来就餐")
    print(res)