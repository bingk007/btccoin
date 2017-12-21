#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @author: WuBingBing

import requ
import time
import datetime

ListPrice = []
BuyTime = []
BuyPrice = []

class Analyze:

    def get_time(self):
        t_now_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        TimeNow = datetime.datetime.strptime(t_now_new, '%Y-%m-%d %H:%M:%S')
        return TimeNow

    def analyze_data(self,exCoin,coin):

        global BuyTime
        global BuyPrice
        tradeType = None
        ListTimes = []
        UpListTimes = []


        if len(ListPrice) == 0:
            ListPrice.append(requ.Requ().get_data(exCoin))

        while True:
            try:
                time.sleep(300)
                print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                ListPrice.append(requ.Requ().get_data(exCoin))
                if len(ListPrice) > 25:
                    del ListPrice[0]
                print("Price:" + ','.join(map(str, ListPrice)))

                rateChange = round((float(ListPrice[len(ListPrice)-1]) - float(ListPrice[0])) / float(ListPrice[0]),4)
                print("TongBiRaise:"+str(rateChange))

                if BuyPrice != []:
                    buyChange = round((float(ListPrice[len(ListPrice)-1]) - float(BuyPrice[0])) / float(BuyPrice[0]),4)
                    print("WinBi:" + str(buyChange))
                    if buyChange > 0.20:
                        UpListTimes.append('1')
                    else:
                        UpListTimes.append('0')
                if len(UpListTimes) > 2:
                    del UpListTimes[0]

                if UpListTimes.count('1') == 2:
                    tradeType = '-1'
                    break

                if rateChange < -0.1:
                    if BuyTime == []:
                        ListTimes.append('-1')
                    elif (self.get_time() - BuyTime[len(BuyTime)-1]).total_seconds() >7200 :
                        ListTimes.append('-1')
                    else:
                        ListTimes.append('0')
                else:
                    ListTimes.append('0')
                if len(ListTimes) > 2:
                    del ListTimes[0]

                if ListTimes.count('-1') == 2:
                    tradeType = '1'
                    break

            except Exception as ex:
                print(Exception,":",ex )
                continue

        if tradeType == '1':
            requ.Requ().login()
            requ.Requ().trade('btc',exCoin,'buy-market')
            print("buy:"+coin)
            BuyTime.append(self.get_time())
            BuyPrice.append(ListPrice[len(ListPrice)-1])

        elif tradeType == '-1':
            requ.Requ().login()
            requ.Requ().trade(coin,exCoin,'sell-market')
            print("sell:"+coin)
            del BuyTime[:]
            del BuyPrice[:]
        else:
            print("exception,exception!")






