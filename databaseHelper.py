from pymysql import *


# 封装了一些数据库语句
# mysql utf-8 一个汉字3字节

class database:
    cur = None
    conn = None

    # 规定使用scraping
    def initialize(self):
        self.conn = connect(host="127.0.0.1", port=3306, user="root", password='424424', db='mysql')
        self.cur = self.conn.cursor()
        self.cur.execute("USE scraping")

    def close(self):
        self.conn.close
        self.cur.close

    def insert_url(self, values):
        # 能不能做一点数据检查呢
        if self.cur is None:
            self.initialize()

        # values = [source,time,url,comsum,comatd]
        try:
            self.cur.execute(
                "INSERT INTO url (source,time,url,comsum,comatd) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\")".
                    format(values[0], values[1], values[2], values[3], int(values[4])))
            self.cur.connection.commit()
            return 0
        except IntegrityError as e:
            return -1

    def insert_eLexicon(self, values):
        if self.cur is None:
            self.initialize()

        # values = [word,type,score]
        self.cur.execute(
            "INSERT INTO eLexicon (word,type,score) VALUES (\"{0}\",\"{1}\",\"{2}\")".format(values[0], values[1],
                                                                                             values[2]))
        self.cur.connection.commit()

    def insert_keyword(self, keyword):
        if self.cur is None:
            self.initialize()

        try:
            self.cur.execute("INSERT INTO keyword (word) VALUES (\"{0}\")".format(keyword))
            self.cur.connection.commit()
            return 0
        except IntegrityError as e:
            return -1
        except Exception as e:
            print(e)
            return -2

    def insert_comments(self, values):
        if self.cur is None:
            self.initialize()

        self.cur.execute(
            "INSERT INTO comments (urlid,content,time,province) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\")".format
            (values[0], values[1], values[2], values[3]))
        self.cur.connection.commit()

    def insert_keycom(self, values):
        if self.cur is None:
            self.initialize()
        self.cur.execute(
            "INSERT INTO keycom (urlid,content,time,province,ranks) VALUES (\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\")".format
            (values[0], values[1], values[2], values[3], values[4]))
        self.cur.connection.commit()

    def select(self, table, limit_A, limit_B):
        if self.cur is None:
            self.initialize()

        # default
        if limit_A is None:
            limit_A = "*"
        if limit_B is None:
            limit_B = ""

        self.cur.execute("SELECT {0} FROM {1} {2}".format(limit_A, table, limit_B))
        return self.cur

    def selectUrl(self):
        return self.select("url", "")

    def update(self, table, value, wherePhrase):
        if self.cur is None:
            self.initialize()

        word = "UPDATE {0} SET {1} WHERE {2}".format(table, value, wherePhrase)
        self.cur.execute("UPDATE {0} SET {1} WHERE {2}".format(table, value, wherePhrase))
        self.conn.commit()

    def myExecute(self, function):
        if self.cur is None:
            self.initialize()
        self.cur.execute(function)
        self.cur.connection.commit()
