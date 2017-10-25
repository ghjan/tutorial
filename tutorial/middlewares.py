# -*- coding: utf-8 -*-

import random

from tutorial.settings import IPPOOL_HTTP, IPPOOL_HTTPS
from tutorial.ipadd import IPPOOL_BACKUP_HTTP, IPPOOL_BACKUP_HTTPS
from tutorial.utils.dbhelper import DBHelp


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        print("type of request:{}".format(request))
        # Set the location of the proxy
        if IPPOOL_HTTP is None:
            sql = "select ip, port, `type` from ips"
            DBHelp().query(sql, self.after_queryips, request=request)
        else:
            self.after_queryips(None, request=request)

    def after_queryips(self, rs, request=None):
        from tutorial.settings import IPPOOL_HTTP, IPPOOL_HTTPS
        if rs:
            if IPPOOL_HTTP is None:
                IPPOOL_HTTP = []
            if IPPOOL_HTTPS is None:
                IPPOOL_HTTPS = []
            for r in rs:
                try:
                    url_ = r['type'].decode('utf-8') + '//' + r['ip'].decode('utf-8') + ':' + r['port'].decode('utf-8')
                    IPPOOL_HTTP.append(url_) if r['type'].strip() == 'HTTP' else IPPOOL_HTTPS.append(url_)
                except Exception as e:
                    print("r:{}".format(r))
                    print(e)
        thisip = self._get_address(request['request'])
        print("this is ip:" + thisip)
        if request:
            request['request'].meta["proxy"] = thisip
        else:
            print("Exception, request is None?!!!")

    def _get_address(self, request):
        is_http = request.url.startswith("http://")
        ippool_backup = IPPOOL_BACKUP_HTTP if is_http else IPPOOL_BACKUP_HTTPS
        ippool = IPPOOL_HTTP if is_http else IPPOOL_HTTPS
        use_backup = not IPPOOL_HTTP if is_http else not IPPOOL_HTTPS
        thisip = 'http://' + random.choice(ippool_backup) if use_backup else random.choice(ippool)
        return thisip


from .settings import USER_AGENT_MAPPING


class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # load USER_AGENTS from settings
        return cls(crawler.settings.getlist('USER_AGENTS'))

    # overwrite process request
    def process_request(self, request, spider):
        # set User-Agent
        request.headers.setdefault('User-Agent', self._build_request_user_agent())

    def _build_request_user_agent(self, pc_only=False):
        """构建随机的模拟用户浏览器user agent"""
        usage = random.randint(0, 2) if pc_only else random.randint(0, 4)
        return USER_AGENT_MAPPING[usage]
