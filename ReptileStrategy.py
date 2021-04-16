import os
import re
import urllib
import urllib.request
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup


class ReptileStrategy:
    MODE_OF_STATIC = 0
    MODE_OF_DYNAMIC = 1
    MODE_OF_FAST_DYNAMIC = 2

    def __init__(self, URL, mode=MODE_OF_STATIC, e_id=""):
        # 默认爬静态页面
        os.environ['http_proxy'] = ''
        # 保留URL
        self.originalURL = URL
        self.mode = mode
        # 设置driver或bsObj
        if mode == self.MODE_OF_STATIC:
            # 设置Request信息 获取Html文本
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            req = urllib.request.Request(url=URL, headers=headers)
            html = urllib.request.urlopen(req)
            self.bsObj = BeautifulSoup(html, features="html.parser")
        elif mode == self.MODE_OF_DYNAMIC:
            # timeA = time.time()
            self.bsObj = self.driverInit()
            # timeB = time.time()
            # print("Normal", timeB-timeA)
        elif mode == self.MODE_OF_FAST_DYNAMIC:
            timeA = time.time()
            self.bsObj = self.driverInit_Fast(e_id)
            timeB = time.time()
            print("Fast", timeB - timeA)

    def driverInit(self):
        """
        use driver to resolve JS
        and then close it
        :return prepared bsObj
        """

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        driver.set_page_load_timeout(40)
        try:
            # 无限循环
            driver.get(self.originalURL)
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        except Exception as e:
            print(e)
            driver.close()
            return self.driverInit()

        bsObj = BeautifulSoup(driver.page_source, features="html.parser")
        time.sleep(2)
        driver.close()
        return bsObj

    def driverInit_Fast(self, e_id):
        # 不是这方法跑的比那个还慢= =
        # 配置一个参数，就是页面加载策略，系统默认是等待，就是等他加载完，直接设置成none，就是不等待，这样就是get操作完后直接就是结束了
        desired_capabilities = DesiredCapabilities.PHANTOMJS
        desired_capabilities["pageLoadStrategy"] = "none"

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

        try:
            driver.get(self.originalURL)
            wait = WebDriverWait(driver, 40, 0.5)
            wait.until(lambda d: d.find_element_by_id('bottom_sina_comment'))
            # wait.until(lambda d: d.find_element_by_class_name('hd clearfix'))
            time.sleep(3)
        except Exception as e:
            print(e)
            return self.__init__(self.originalURL, self.MODE_OF_STATIC)
        # bs 时间忽略不计
        bsObj = BeautifulSoup(driver.page_source, features="html.parser")
        driver.close()
        return bsObj

    def get_Title(self):
        pass

    def get_Content(self):
        pass

    def get_URL(self):
        pass


class Jsty_Strategy(ReptileStrategy):
    # 荔枝网 时间戳可以从URL看出了，感觉不用特地读
    # 按助教的意思好像是，通过这几个网站来反向筛选 信息源？
    def __init__(self, URL):
        super.__init__(URL)

    def get_Title(self):
        return self.bsObj.head.title.get_text()

    def get_Content(self):
        # 好坑啊 get_text是个方法不是个属性
        info = self.bsObj.find("p", {"class": "info fL"})
        time = info.find("span", {"class": "time"}).get_text()
        source = info.find("span", {"class": "source"}).get_text()
        content = self.bsObj.find("div", {"class": "content"}).findAll("p")

        file = open("testArticle.txt", "a", encoding='utf-8')
        file.write("标题： " + self.get_Title() + "\n")
        file.write("时间： " + time + "\n")
        file.write("来源:  " + source + "\n")

        for p in content:
            file.write(p.get_text() + "\n")
        file.write("-----------END-------------\n")
        file.close()


class Sina_Strategy(ReptileStrategy):
    # https://search.sina.com.cn/?q=%E6%96%B0%E5%86%A0&c=news&range=all&stime=2020-01-01&etime=2020-06-01&time=2020&page=2
    # https://search.sina.com.cn/?q=%E6%96%B0%E5%86%A0&c=news&range=all&time=2020&stime=2020-01-01%2000:00:00&etime=2020-06-01%2023:59:59&num=20
    # 我不会爬JS 只能URL分析法了= =   （查询内容的UTF编码（此处为新冠））          （年份）

    def get_Title(self):
        return self.bsObj.find("h1", {"class": "main-title"}).get_text()

    # 第一次入库用 只记录来源 时间 url
    def get_Simple_Content(self):
        time = self.bsObj.find("span", {"class": "date"}).get_text()
        # time = time[0:4]+time[5:7]+time[8:10] # 20200601 年月日
        # '2020-01-22+99:00:00&'
        etime = time[0:4] + "-" + time[5:7] + "-" + time[8:10] + "+" + time[12:18] + ":00&"
        time = time[2:4] + time[5:7] + time[8:10] + time[12:14]  # 20 年 06 月 01日 23时
        try:
            source = self.bsObj.find("a", {"class": "source"}).get_text()
        except AttributeError as e:
            print(e)
            source = "来源不明"

        url = self.originalURL

        # 还能这么弄
        res = [source, time, url, etime]
        return res

    # include time article source
    def get_Content(self):
        article = self.bsObj.find("div", {"id": "article"}).findAll("p")
        time = self.bsObj.find("span", {"class": "date"}).get_text()
        source = self.bsObj.find("a", {"class": "source"}).get_text()

        file = open("testArticle.txt", "a", encoding='utf-8')
        file.write("标题： " + self.get_Title() + "\n")
        file.write("时间： " + time + "\n")
        file.write("来源:  " + source + "\n")

        for p in article:
            file.write(p.get_text() + "\n")
        file.write("-----------END-------------\n")
        file.close()

    def get_Comment_Resolve(self):
        assert self.mode == self.MODE_OF_DYNAMIC
        hd_clearfix = self.bsObj.find("div", {"id": "bottom_sina_comment"})
        comment_s_a = hd_clearfix.find("a", {"data-sudaclick": "comment_sum_p"})

        if comment_s_a is None:
            # 加载错误
            raise LoadMissException(self.originalURL)

        # comment_url = comment_s_a.attrs['href']

        comment = []
        # 1. 爬取最热评论
        comment_div = hd_clearfix.find("div", {"comment-type": "hotList"}).findAll("div", {"class": "item clearfix"})
        for div in comment_div:
            comment.append(div.find("div", {"class": "txt"}).get_text())

        # 2. 爬取最新评论
        try:
            # todo Something wrong
            comment_div = hd_clearfix.find("div", {"comment-type": "latestList"}).findAll("div",
                                                                                          {"class": "item clearfix"})
            for div in comment_div:
                comment.append(div.find("div", {"class": "txt"}).get_text())
        except Exception as e:
            print("sina_getcomment" + e)

        comment_sum = int(comment_s_a.get_text())
        return [comment_sum, comment]

    def get_Comment_Request(self):
        """
        :return:[[attendance ,comment_sum], comment[[cmnProvince, cmntime, cmn.get('content')]]]
        """
        assert self.mode == self.MODE_OF_STATIC
        sina_comment_server = "http://comment5.news.sina.com.cn/page/info?"

        newsid = self.getNewsID()
        channel = self.getChannel()

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        param = {
            "format": 'json',
            'channel': channel,
            'newsid': newsid,
            'page': '1'
        }

        for i in range(5):
            response = requests.get(sina_comment_server, params=param, headers=headers)

            res = response.json()['result']
            # 从JSON 格式中获取所需内容
            try:
                comment_sum = res['count'].get("show")
                comment_attendance = res['count'].get('total')
                comment = []
                break
            except Exception as e:
                if i <= 3:
                    print("小歇一下-PhaseA")
                    time.sleep(0.5)
                    continue
                else:
                    file = open("../Log/runTimeExceptionUrls.txt", "a+")
                    file.writelines(self.originalURL + "\n")
                    print(e, end="")
                    print(self.originalURL)

        if not res.get('cmntlist'):
            raise RequestMissException(self.originalURL)
            # return [0, []]

        cmntlist = res['cmntlist']
        for cmn in cmntlist:
            cmntime = cmn.get('time').replace("-", "").replace(" ", "")
            cmntime = cmntime[2:10]
            cmnProvince = cmn.get('area')[0:2]
            # todo 可能有bug
            rank = cmn.get('rank')
            comment.append([cmnProvince, cmntime, cmn.get('content'), rank])

        # Many Pages
        if comment_sum >= 20:
            for i in range(2, int(comment_sum / 20)):
                for j in range(0, 4):
                    param['page'] = str(i)
                    response = requests.get(sina_comment_server, params=param, headers=headers)
                    res = response.json()['result']

                    # 从JSON 格式中获取所需内容
                    try:
                        # res = response.json()['result']
                        res['count'].get("show")
                        break
                    except Exception as e:
                        if j <= 3:
                            print("Sleep:PhaseB For page " + str(i) + " For time " + str(j))
                            time.sleep(0.5)
                            continue
                        else:
                            print(e, end="")
                            print(self.originalURL)

                try:
                    cmntlist = res['cmntlist']
                    for cmn in cmntlist:
                        cmntime = cmn.get('time').replace("-", "").replace(" ", "")
                        cmntime = cmntime[2:10]
                        cmnProvince = cmn.get('area')[0:2]
                        # todo 可能有bug
                        rank = cmn.get('rank')
                        comment.append([cmnProvince, cmntime, cmn.get('content'), rank])
                except Exception as e:
                    print(e, end="")
                    print("这里不应该有问题", end="")
                    print(self.originalURL)

        # 简单的数据清洗

        return [[comment_attendance, comment_sum], comment]

    def getURL(self):
        urlSet = set()
        res = self.bsObj.findAll("div", {"class": "box-result clearfix"})
        for div in res:
            # oneUrl = div.find("h2").find("a", {"href": re.compile("https://news\.sina\.com(.*)")})
            oneUrl = div.find("h2").find("a", {"href": re.compile("https://news\.sina\.com\.cn/(c|o|zx|gov|w|s)(.*)")})

            if oneUrl is not None:
                oneUrl = oneUrl.attrs['href']
            else:
                continue

            if oneUrl not in urlSet:
                urlSet.add(oneUrl)

        return urlSet

    # 通过url page+1
    def getNextPage(self):
        res = self.originalURL
        index = self.originalURL.find("page=")
        page_num = res[index + 5:]
        next_page_num = str(int(page_num) + 1)
        res = res[0:index + 5] + next_page_num
        return res

    def getNewsID(self):
        matchObj = re.search(r"doc-i(.+?)\.shtml", self.originalURL, re.M | re.I)
        return "comos-" + matchObj.group(1)

    def getChannel(self):
        pattern = re.compile(r"var SINA_TEXT_PAGE_INFO = (.*?);$", re.MULTILINE | re.DOTALL)
        script = self.bsObj.find("script", text=pattern).contents[0]
        matchObj = re.search(r"channel: '(.*?)',", script, re.M | re.I)
        m = matchObj.group(1)
        return m


class Zhihu_Strategy(ReptileStrategy):
    def __init__(self, URL):
        super().__init__(URL)

    def get_Content(self):
        content = self.bsObj.find("div", {"class": "RichContent-inner"})
        content = content.find("span")

        s = str(content)  # 转换成字符串
        s_replace = s.replace('<br/>', "\n")  # 用换行符替换'<br/>'

        title = self.bsObj.find("h1", {"class": "QuestionHeader-title"}).get_text()

        file = open(title + ".txt", "a", encoding='utf-8')
        file.write("标题： " + title + "\n")

        file.write(s_replace + "\n")
        file.write("-----------END-------------\n")
        file.close()


class LoadMissException(Exception):
    """
    不知道为什么加载出了div 但是没有 comment
    """

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "加载错误 " + self.url


class RequestMissException(Exception):
    """
    不能用Request的部分网页
    """

    def __init__(self, url):
        self.url = url

    def __str__(self) -> str:
        return "Request 解析错误" + self.url

    def save(self):
        file = open("../Log/requestErrorUrls.txt", "a+")
        log = open("../Log/log.txt", "a+")
        file.writelines(self.url + "\n")
        log.writelines("Request 解析错误" + self.url + " " + time.asctime(time.localtime(time.time())) + "\n")


class ModeException(Exception):
    """
    加载格式错误
    """

    def __str__(self) -> str:
        return "Mode Exception"
