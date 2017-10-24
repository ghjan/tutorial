# encoding = utf8
from .handledb import DBHelp
import urllib.request, urllib.error, urllib.parse
import time
from tutorial.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD
from .singleton import Singleton
from .ipadd import IPPOOL_BACKUP_HTTP, IPPOOL_BACKUP_HTTPS

dbapi = "MySQLdb"
kwargs = {'user': MYSQL_USER, 'passwd': MYSQL_PASSWD, 'db': MYSQL_DBNAME, 'host': MYSQL_HOST, 'port': MYSQL_PORT,
          'use_unicode': True}


def counter(start_at=0):
    '''Function: count number
	Usage: f=counter(i) print f() #i+1'''
    count = [start_at]

    def incr():
        count[0] += 1
        return count[0]

    return incr


def use_proxy(browser, proxy, url):
    '''Open browser with proxy'''
    # After visited transfer ip
    profile = browser.profile
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', proxy[0])
    profile.set_preference('network.proxy.http_port', int(proxy[1]))
    profile.set_preference('permissions.default.image', 2)
    profile.update_preferences()
    browser.profile = profile
    browser.get(url)
    browser.implicitly_wait(30)
    return browser


class GetIp(Singleton):
    def __init__(self):
        sql = '''SELECT  `ip`,`port`,`type`
        FROM  `ips`
        WHERE `type` REGEXP  'HTTP|HTTPS'
        AND  `speed`<5 OR `speed` IS NULL
        ORDER BY `type` ASC
        LIMIT 50 '''
        DBHelp().query(sql, self._after_query)
        self.result = None

    def _after_query(self, rs):
        print("success for query ips; len(result):{}".format(len(rs)))
        self.result = rs

    def del_ip(self, record):
        '''delete ip that can not use'''
        sql = "delete from ips where IP='%s' and PORT='%s'" % (record[0], record[1])
        print(sql)

        DBHelp().exec_sql(sql)
        print(record, " was deleted.")

    def judge_ip(self, record):
        '''Judge IP can use or not'''
        http_url = "http://www.baidu.com/"
        https_url = "https://www.alipay.com/"
        proxy_type = record[2].lower()
        url = http_url if proxy_type == "http" else https_url
        proxy = "%s:%s" % (record[0], record[1])
        try:
            req = urllib.request.Request(url=url)
            req.set_proxy(proxy, proxy_type)
            response = urllib.request.urlopen(req, timeout=30)
        except Exception as e:
            print("Request Error:", e)

            self.del_ip(record)
            return False
        else:
            code = response.getcode()
            if code >= 200 and code < 300:
                print('Effective proxy', record)
                return True
            else:
                print('Invalide proxy', record)

                self.del_ip(record)
                return False

    def get_ips(self, timeout=10):
        print("Proxy getip was executed.")
        count = 0
        while not self.result and timeout and count < timeout:
            time.sleep(1)
            count += 1
        if not self.result:
            print("use ipadd_backup!")
            http = [item.split(':') for item in IPPOOL_BACKUP_HTTP]
            https = [item.split(':') for item in IPPOOL_BACKUP_HTTPS]
        else:
            http = [h[0:2] for h in self.result if h[2] == "HTTP" and self.judge_ip(h)]
            https = [h[0:2] for h in self.result if h[2] == "HTTPS" and self.judge_ip(h)]
        print("Http: ", len(http), "Https: ", len(https))

        return {"http": http, "https": https}
