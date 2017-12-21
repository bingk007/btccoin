#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @author: WuBingBing

import requ
import time
import datetime

ListPrice = []
BuyTime = []
hugeChange = []

class Analyze:

    def analyze_data(self,exCoin,coin):

        global BuyTime
        tradeType = None
        ListTimes = []
        LatestTimesSpace = []
        if len(ListPrice) == 0:
            ListPrice.append(requ.Requ().get_data(exCoin))

        while True:
            try:
                time.sleep(60)
                print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

                if  BuyTime != []:
                    print("LatestBuyTime:" + ','.join(map(str, BuyTime)))
                    t_now_new = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    TimeNow = datetime.datetime.strptime(t_now_new,'%Y-%m-%d %H:%M:%S')
                    if (TimeNow - BuyTime[len(BuyTime)-1]).total_seconds() > 21600:
                        tradeType = '-1'
                        print("long no raise,so sell！")
                        break

                ListPrice.append(requ.Requ().get_data(exCoin))
                if len(ListPrice) > 20:
                    del ListPrice[0]
                print("Price:" + ','.join(map(str, ListPrice)))

                rateChange = round((float(ListPrice[len(ListPrice)-1]) - float(ListPrice[0])) / float(ListPrice[0]),4)
                print("TongBiRaise:"+str(rateChange))

                if rateChange >= 0.10 :
                    print("huge up change happen!")
                    t_now_new = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    TimeNow = datetime.datetime.strptime(t_now_new, '%Y-%m-%d %H:%M:%S')
                    if BuyTime != [] and (TimeNow - BuyTime[len(BuyTime)-1]).total_seconds() > 600:
                        tradeType = '-1'
                        break

                if rateChange >= 0.01:
                    ListTimes.append('1')
                elif rateChange <= -0.008:
                    ListTimes.append('-1')
                else:
                    ListTimes.append('0')
                if len(ListTimes) > 10:
                    del ListTimes[0]
                print ("TongBiRaiseTimes:"+ ','.join(ListTimes))

                if len(ListPrice) >= 6:
                    min_two_change = round((float(ListPrice[len(ListPrice)-1]) - float(ListPrice[len(ListPrice)-4])) / float(ListPrice[len(ListPrice)-4]),4)
                    print("SpaceBiRaise:" + str(min_two_change))
                    if min_two_change >= 0.002:
                        LatestTimesSpace.append('+1')
                    elif min_two_change <= -0.001:
                        LatestTimesSpace.append('-1')
                    else:
                        LatestTimesSpace.append('0')
                    if len(LatestTimesSpace) > 10:
                        del LatestTimesSpace[0]
                    print ("LatestTimesSpace:"+ ','.join(LatestTimesSpace))

                if ListTimes.count('1') >= 8:
                    if LatestTimesSpace.count('+1') >= 7:
                        tradeType = '1'
                        break
                elif ListTimes.count('-1') >= 7:
                    if LatestTimesSpace.count('-1') >= 8:
                        tradeType = '-1'
                        break

            except Exception as ex:
                print(Exception,":",ex )
                continue

        if tradeType == '1':
            requ.Requ().login()
            requ.Requ().trade('btc',exCoin,'buy-market')
            print("buy:"+coin)
            t_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            BuyTime.append(datetime.datetime.strptime(t_now,'%Y-%m-%d %H:%M:%S'))

        elif tradeType == '-1':
            requ.Requ().login()
            requ.Requ().trade(coin,exCoin,'sell-market')
            print("sell:"+coin)
            del BuyTime[:]
        else:
            print("exception,exception!")






