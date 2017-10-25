# encoding = utf8
from scrapy.utils.project import get_project_settings

try:  # py3
    import pymysql

    CURSORCLASS = pymysql.cursors.DictCursor
    pymysql.install_as_MySQLdb()
except:  # py2
    import MySQLdb

    CURSORCLASS = MySQLdb.cursors.DictCursor

from twisted.enterprise import adbapi

dbpool = adbapi.ConnectionPool("MySQLdb", 'mydb', 'andrew', 'password')


class DBHelp(object):
    def __init__(self):
        self.settings = get_project_settings()  # 获取settings配置，设置需要的信息

        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

        dbparams = dict(
            host=self.host,  # 读取settings中的配置
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=CURSORCLASS,
            use_unicode=False,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy..

    # 连接到mysql，不是连接到具体的数据库
    def connectMysql(self):
        conn = MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               # db=self.db,不指定数据库名
                               charset='utf8')  # 要指定编码，否则中文可能乱码
        return conn

    # 创建数据库
    def createDatabase(self):
        '''因为创建数据库直接修改settings中的配置MYSQL_DBNAME即可，所以就不要传sql语句了'''
        conn = self.connectMysql()  # 连接数据库

        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)  # 执行sql语句
        cur.close()
        conn.close()

    # 查询数据库
    def query(self, sql, callback=None, **kwargs):
        query = self.dbpool.runQuery(sql)  # 调用查询的方法
        if callback and callable(callback):
            query.addCallback(callback, kwargs)
