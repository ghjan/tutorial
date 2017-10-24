# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

# from scrapy import signals
# Importing base64 library because we'll need it ONLY in case
# if the proxy we are going to use requires authentication
# import base64
import time
from .proxy import GetIp, counter
from .ipadd import IPPOOL_BACKUP_HTTP, IPPOOL_BACKUP_HTTPS
import logging

GetIp_Single = GetIp()


class ProxyMiddleware(object):
    http_n = 0  # counter for http requests
    https_n = 0  # counter for https requests

    # overwrite process request
    def process_request(self, request, spider):
        count = 0
        timeout = 10
        while not GetIp_Single.result and timeout and count < timeout:
            time.sleep(1)
            count += 1
        ips = {}
        if not GetIp_Single.result:
            print("use ipadd_backup!")
            ips['http'] = [item.split(':') for item in IPPOOL_BACKUP_HTTP]
            ips['https'] = [item.split(':') for item in IPPOOL_BACKUP_HTTPS]
        else:
            print("use result successfully!")
            ips = GetIp().get_ips()
        # Set the location of the proxy
        if request.url.startswith("http://"):
            n = ProxyMiddleware.http_n
            n = n if n < len(ips['http']) else 0
            request.meta['proxy'] = "http://%s:%d" % (
                ips['http'][n][0], int(ips['http'][n][1]))
            logging.info('Squence - http: %s - %s' % (n, str(ips['http'][n])))
            ProxyMiddleware.http_n = n + 1

        if request.url.startswith("https://"):
            n = ProxyMiddleware.https_n
            n = n if n < len(ips['https']) else 0
            request.meta['proxy'] = "https://%s:%d" % (
                ips['https'][n][0], int(ips['https'][n][1]))
            logging.info('Squence - https: %s - %s' % (n, str(ips['https'][n])))
            ProxyMiddleware.https_n = n + 1
