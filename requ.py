#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @author: WuBingBing

import requests
import re
import config
import time
import math
# import requests.packages.urllib3.util.ssl_
# import ssl
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
# ssl._create_default_https_context = ssl._create_unverified_context
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Requ:

    HB_SSO_GT = 'HrDDZmhbDDsL6VRY+/1MyM5M12k+H8X23CjgAu4h/T73Ht++TO+7FKXizaYzMA9T6uXEYKiGGXICtKp/ZEiFO2k9s4VGQ4WxUEfy6bbU8VeMHDkuejYkqDMOEhJkCojuIXbOZ5KOgJD4JP19nxe1wFdVrjtO4igdBtNXR9HtEIw=;'
    SESSION = '378de756-4f22-4ddf-a183-bcd00fc858a8;'
    AUTHTOKEN = 'dnAbMTL8fFj_e5v_8FnfFzT0IAjgGuVXN9TWotPHsRkY-uOP2m0-gvjE57ad1qDF;'
    __jsluid = 'e68523630818cb03b92f677123381923'

    def get_data(self, exCoin):
        try:
            for i in range(10):
                r = requests.get('https://l10n.huobi.cn/market/overview', verify=False, headers={
                    'Accept-Language': 'zh-CN',
                    'Connection': 'close',
                    'appType': '1',
                    'appVersion': '310',
                    'Huobi-Website': 'huobi.pro',
                    'Host': 'l10n.huobi.com',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.8.0',
                    'If-Modified-Since': ''
                })
                if r.text.find('"status":"ok"') != -1:
                    break
                else:
                    print("data,data,data")
                    time.sleep(1)
            market = r.json()['data']
            for i in market:
                for k, v in i.items():
                    if v == exCoin:
                        price_now = i['close']
                        break
            return price_now
        except Exception as ex:
            print(Exception, ":", ex)

    def login(self):
        try:
            for i in range(10):
                r = requests.post('https://uc-cn.huobi.com/uc/open/login',verify=False,headers={
                    'Accept-Language': 'zh-CN',
                    'Huobi-Website': 'huobi.pro',
                    'Host': 'uc-cn.huobi.com',
                    'Connection': 'close',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.8.0',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Cookie': 'HB_SSO_GT='+self.HB_SSO_GT+'SESSION='+self.SESSION+'AUTHTOKEN='+self.AUTHTOKEN+'config.HUOBIMEIBISESSID='+config.HUOBIMEIBISESSID+'__jsluid='+self.__jsluid
                }, data='{"way":"APP_HUOBI_PRO","password":"密码","login_name":"13728728079"}')
                if r.text.find('"success":true') != -1:
                    break
                else:
                    print("login,login 11")
                    time.sleep(1)
            ssotoken = re.search('ssotoken=(.+?)"',r.text).group(1)
            for i in range(10):
                r0 = requests.get('https://www.huobi.com/p/user/uc_login',verify=False,headers={
                    'Accept-Language': 'zh-CN',
                    'Huobi-Website': 'huobi.pro',
                    'Host': 'www.huobi.com',
                    'Connection': 'close',
                    'Accept-Encoding': 'gzip',
                    'User-Agent': 'okhttp/3.8.0',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Cookie': 'HB_SSO_GT=' + self.HB_SSO_GT + 'SESSION=' + self.SESSION + 'AUTHTOKEN=' + self.AUTHTOKEN + 'config.HUOBIMEIBISESSID=' + config.HUOBIMEIBISESSID + '__jsluid=' + self.__jsluid
                }, params='ssotoken='+ssotoken)
                config.HUOBIMEIBISESSID = re.search('"HUOBIMEIBISESSID":"(.+?)"',r0.text).group(1)
                if r.text.find('"success":true') != -1:
                    break
                else:
                    print("login,login 22")
                    time.sleep(1)
        except Exception as ex:
            print(Exception, ":", ex)


    def account(self,coin):
        try:
            for i in range(10):
                r = requests.get('https://l10n.huobi.com/v1/account/accounts/443597/balance',verify=False,headers={
                    'Token': config.HUOBIMEIBISESSID,
                    'Accept-Language': 'zh-CN',
                     'Connection': 'close',
                    'Huobi-Website': 'huobi.pro',
                    'Host': 'l10n.huobi.com',
                    'Accept-Encoding': 'gzip',
                   'User-Agent': 'okhttp/3.8.0',
                    'If-Modified-Since': ''
                })
                if r.text.find('"status":"ok"') != -1:
                    break
                else:
                    print("accout,accout")
                    time.sleep(1)
                    self.login()
            l= re.search('"currency":"'+coin+'","type":"trade","balance":"(.+?)"',r.text).group(1)
            if coin == 'btc':
                if float(l)/4 > 0.001:
                    ls = str(float(l)/4)
                    num = ls.split('.')[0]+'.'+ls.split('.')[1][0:4]
                elif float(l)/3 > 0.001:
                    ls = str(float(l)/3)
                    num = ls.split('.')[0] + '.'+ ls.split('.')[1][0:4]
                elif float(l)/2 > 0.001:
                    ls = str(float(l)/2)
                    num = ls.split('.')[0]+'.'+ls.split('.')[1][0:4]
                else:
                    num = l.split('.')[0] + '.' + l.split('.')[1][0:4]
            else:
                if coin in ['xrp','snt','tnb','knc','itc','qash','gnt','zrx','storj','qsp','rcn','ast','tnt','cmt','bat','rdn']:
                    num = l.split('.')[0]
                elif coin in ['eos']:
                    num = l.split('.')[0]+'.'+l.split('.')[1][0:2]
                else:
                    num = l.split('.')[0]+'.'+l.split('.')[1][0:4]
            return num
        except Exception as ex:
            print(Exception, ":", ex)

    def trade(self,coin,exCoin,tradeType):
        try:
            headers = {
                'Token': config.HUOBIMEIBISESSID,
                'Accept-Language': 'zh-CN',
                'Connection': 'close',
                'appType': '1',
                'appVersion': '310',
                'Huobi-Website': 'huobi.pro',
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': 'l10n.huobi.cn',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.8.0'
            }
            if float(self.account(coin)) >= 0.0001:
                for i in range(10):
                    r = requests.post('https://l10n.huobi.cn/v1/order/orders',verify=False,headers=headers,data='{"amount":"'+self.account(coin)+'","account-id":443597,"source":"app","symbol":"'+exCoin+'","type":"'+tradeType+'"}')
                    if r.text.find('"status":"ok"') != -1:
                        break
                    else:
                        print("trade,trade 11")
                        time.sleep(1)
                        self.login()
                order = re.search('"data":(.+?)}', r.text).group(1)
                for i in range(10):
                    r0 = requests.post('https://l10n.huobi.cn/v1/order/orders/'+order+'/place',verify=False,headers=headers)
                    if r.text.find('"status":"ok"') != -1:
                        break
                    else:
                        print("trade,trade 22")
                        time.sleep(1)
                        self.login()
                print(r.text)
                print(r0.text)
            else:
                print("No money")
        except Exception as ex:
            print(Exception, ":", ex)


# Requ().login()
# Requ().account("btc")
# Requ().account("bcc")
# print(Requ().get_data("bccbtc"))
# Requ().trade('bcc','sell-market')
# Requ().trade('btc','buy-market')

