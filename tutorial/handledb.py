# -*- coding:utf-8 -*- 

'''
Function:handle database's any operation
Author:Wan Shitao
Email:wst.521@163.com
Date:2014.8.20
Reference:funcs.py
'''
from twisted.enterprise import adbapi

try:  # py3
    import pymysql

    CURSORCLASS = pymysql.cursors.DictCursor
    pymysql.install_as_MySQLdb()
except:  # py2
    import MySQLdb

    CURSORCLASS = MySQLdb.cursors.DictCursor

from scrapy.utils.project import get_project_settings
from .singleton import Singleton


class DBHelp(Singleton):
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

    # 查询数据库
    def query(self, sql, callback=None, **kwargs):
        query = self.dbpool.runQuery(sql)  # 调用查询的方法
        if callback and callable(callback):
            query.addCallback(callback, kwargs)

    def exec_sql(self, sql, callback=None, data='', **kwargs):
        '''execute insert/update/delete sql operation'''

        if data == '':
            query = self.dbpool.runInteraction(self._conditional_execute, sql)  # 调用插入的方法
            query.addErrback(self._handle_error, data)  # 调用异常处理方法
        else:
            query = self.dbpool.runInteraction(self._conditional_execute, sql, data=data)  # 调用插入的方法
            query.addErrback(self._handle_error, data)  # 调用异常处理方法
        query.addCallback(self._handleSuccess)
        if callback:
            query.addCallback(callback)
        return data

    def insert_data(self, data_, table, **kwargs):
        '''insert data into database'''
        insertSQL = "insert into `" + table + "`(%s) values (%s)"
        keys = list(data_.keys())
        fields = ','.join(['`%s`' % k for k in keys])
        qm = ','.join(['%s'] * len(keys))
        sql = insertSQL % (fields, qm)
        data = [data_[k] for k in keys]
        self.exec_sql(sql, data, **kwargs)

    def _handle_error(self, failue, data):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failue)
        print("data:{}".format(data))

    def _handleSuccess(self, data):
        print("success, data:", data)

    # 写入数据库中
    def _conditional_execute(self, tx, sql, data=None):
        tx.execute(sql, data)
