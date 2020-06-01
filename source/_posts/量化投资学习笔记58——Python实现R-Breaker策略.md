---
title: 量化投资学习笔记58——Python实现R-Breaker策略
date: 2020-06-01 13:13:09
tags: [量化投资, 策略实现, pyalgotrade, R-Breaker]
categories: 量化投资
---
有位网友让我用python实现R-Breaker策略，搜了一下:
这个策略荣登《Futures Truth Magazine》Top10最赚钱策略15年，但都是在2010年以前，现在怎么样不得而知。
其基本原理为:根据前一交易日的收盘价、最高价和最低价数据计算出六个价位，从大到小依次为：突破买入价、观察卖出价、反转卖出价、反转买入、观察买入价、突破卖出价。
先根据三个数据计算枢轴点，即三个数据的平均值。
pivot = (high+low+close)/3
再计算六个价位:
突破买入价
bBreak = high+2*(pivot-low)
观察卖出价
sSetup = pivot+(high-low)
反转卖出价
sEnter = 2*pivot-low
反转买入价
bEnter = 2*pivot-high
观察买入价
bSetup = pivot-(high-low)
突破卖出价
sBreak = low-2*(high-pivot)
追踪盘中价格走势，实时判断触发条件:
1.突破
空仓条件下，价格突破买入价，买入(期货是做多)。
空仓条件下，价格突破卖出价，不操作(期货是做空)。
2.反转
满仓(期货为持多单)，当日内最高价超过观察卖出价后，盘中价格出现回落，且进一步跌破反转卖出价构成的支撑线时，卖出(期货为反手做空)。
持空单的略了。
开始干活，先用tushare获取数据，最小间隔是5分钟。而pyalgotrade默认的数据源格式的数据（雅虎金融，谷歌金融等4个）都只支持日线和周线数据。只能有更初级的GenericBarFeed,又参照网上资料试了半天。终于能让pyalgotrade跑起来了。
```python
# coding:utf-8
# 获取数据并转换成pyalgotrade接受的格式
# 参考https://blog.csdn.net/lawme/article/details/51495349


import tushare as ts
import pandas as pd

from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.feed import csvfeed
from pyalgotrade import strategy


def downloadData(code):
    data = ts.get_k_data(code, "2019-01-01", "2019-12-31", ktype="5")
    #print(data.head())
#    print(data.info())
    data.to_csv("data.csv")
    df = pd.read_csv("data.csv")
    df2 = pd.DataFrame({'Date Time' : df['date'], 'Open' : df['open'], 'High' : df['high'],'Close' : df['close'], 'Low' : df['low'],'Volume' : df['volume'], 'Adj Close':df['close']})
    # 调整数据为yahoo格式
    dt = df2.pop('Date Time')
    df2.insert(0,'Date Time',dt)
    o = df2.pop('Open')
    df2.insert(1,'Open',o)
    h = df2.pop('High')
    df2.insert(2,'High',h)
    l = df2.pop('Low')
    df2.insert(3,'Low',l)
    c = df2.pop('Close')
    df2.insert(4,'Close',c)
    v = df2.pop('Volume')
    df2.insert(5,'Volume',v)
    # 新格式数据存盘，不保存索引编号
    filename = code+".csv"
    # print(filename, type(filename))
    df2.to_csv(filename, index=False)
    #feed = yahoofeed.Feed()
    #feed.addBarsFromCSV("CB", filename)
    return filename
    
    
# 从csv文件数据导入为pyalgotrade数据源
def buildFeed(code, filename):
    feed = GenericBarFeed(Frequency.MINUTE)
    feed.setDateTimeFormat("%Y-%m-%d %H:%M")
    feed.addBarsFromCSV(code, filename)
    #feed = csvfeed.Feed("Date Time", "%Y-%m-%d %H:%M")
#    feed.addValuesFromCSV(filename)
    #for item in feed:
#        print(item[0], len(item), item[1])
#        print(item.getDateTime())
    return feed
    
    
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())
        date = bar.getDateTime()
        print(date.year, date.month, date.day)


if __name__ == "__main__":
    code = "601988"
    filename = downloadData(code)
    # filename = "testdata.csv"
    feed = buildFeed(code, filename)
    myStrategy = MyStrategy(feed, code)
    myStrategy.run()
```
数据搞定了就开始写策略了，程序框架参考了本系列第一篇文章的代码，直接复制过来改。
这是一个日内策略，要在每次数据变更的时候判断是否到了买入/卖出点。然而判断依据又是根据上一个交易日的最高/最低/收盘价计算的六个指标。于是先建立一个类来处理指标计算，买入卖出点判断等。
```python
# 策略要计算的指标
class Index():
    def __init__(self):
        self.__pivot = 0.0     # 枢轴点
        self.__bBreak = 0.0 # 突破买入价
        self.__sSetup = 0.0 # 观察卖出价
        self.__sEnter = 0.0  # 反转卖出价
        self.__bEnter = 0.0  # 反转买入价
        self.__bSetup = 0.0 # 观察买入价
        self.__sBreak = 0.0 # 突破卖出价
        
        
   # 根据前一日最高价，最低价，收盘价更新指标
    def updata(self, high, low, close):
        self.__pivot = (high+low+close)/3.0
        self.__bBreak = high+2.0*(self.__pivot-low)
        self.__sSetup = self.__pivot+(high-low)
        self.__sEnter = 2*self.__pivot-low
        self.__bEnter = 2*self.__pivot-high
        self.__bSetup = self.__pivot-(high-low)
        self.__sBreak = low-2*(high-self.__pivot)
       
       
    # 返回所有指标
    def getIndex(self):
        return (self.__bBreak, self.__sSetup, self.__sEnter, self.__bEnter, self.__bSetup, self.__sBreak)
        
        
    # 根据当前的价格，判断是否操作
    # 返回值，0-不操作，1-全仓买入，2-全仓卖出
    def judge(self, high, low, close, share, price):
        # 空仓且价格超过突破买入价，全仓买入
        if share == 0 and price > self.__bBreak:
            return 1
        # 满仓，日内最高价超过观察卖出价后，盘中价格回落跌破反转卖出价，清仓。
        if share != 0 and high > self.__sSetup and price < self.__sEnter:
            return 2
        # 其它情况，不操作
        return 0
```
而在pyalgotrade的策略类中，在onBar函数里每次更新数据都检查是否是下一个交易日了，如果是下一个交易日，就调用上面的updata函数重新计算六个指标。然后每次都判断是否到达买入卖出点，到达即全仓买入/卖出。
```python
# 策略类
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, brk):
        super().__init__(feed, brk)
        self.__position = None
        self.__instrument = instrument
        self.getBroker()
        self.__cost = 0.0
        # 记录当前的日期
        self.__year = 0
        self.__month = 0
        self.__day = 0
        # 策略的指标，每天更新
        self.__index = Index()
        # 每天的最高价，最低价，收盘价
        self.__high = 0
        self.__low = 100000000
        self.__close = 0

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        # self.info("买入 %.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("卖出 %.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
        
    # 日期改变，重新计算那六个指标
    def updateData(self):
        self.__index.updata(self.__high, self.__low, self.__close)
        self.__high = 0
        self.__low = 100000000
        self.__close = 0

    def onBars(self, bars):
        brk = self.getBroker()
        bar = bars[self.__instrument]
        # 先判断是否是新的交易日，是则更新指标
        date = bar.getDateTime()
        year = date.year
        month = date.month
        day = date.day
        print(date, self.__high, self.__low, self.__close)
        if self.__year != year or self.__month != month or self.__day != day:
            self.__year = year
            self.__month = month
            self.__day = day
            self.updateData()
        else:
            price = bars[self.__instrument].getPrice()
            if price > self.__high:
                self.__high = price
            if price < self.__low:
                self.__low = price
            self.__close = price
        share = brk.getShares(self.__instrument)
        price = bars[self.__instrument].getPrice()
        tradeCode = self.__index.judge(self.__high, self.__low, self.__close, share, price)
        if tradeCode == 1:
            # 全仓买入
            if shares != 0:
                break
            else: #这里全仓买入
                cash = brk.getCash()
                shares = cash/price
                shares = (shares//100)*100
                self.__position = self.enterLong(self.__instrument, shares, True)
                self.__cost += brk.getCommission().calculate(brk, price, shares)
        elif tradeCode == 2:
            # 全仓卖出
            if share == 0:
                break
            else: #这里全仓卖出
                self.__position.exitMarket()
                self.__cost += brk.getCommission().calculate(brk, price, shares)
```
其它代码不再赘述，可以看https://github.com/zwdnet/MyQuant/tree/master/45




参考:
1.https://zhuanlan.zhihu.com/p/81793766


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)