#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @author: WuBingBing

import threading
import analyze
import analyze_new

if __name__ == '__main__':
    print('Start!')
    while True:
        try:
            analyze_new.Analyze().analyze_data('rcnbtc','rcn')
        except Exception as ex:
            print(Exception, ":", ex)

