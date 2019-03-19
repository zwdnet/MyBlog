---
title: ETF定投数据分析7——模拟交易系统开发
date: 2019-03-19 13:10:11
tags: [ETF,投资理财,定投,Python,模拟交易]
categories: 计算机
---
之前写的模拟交易程序，把整个过程放到一个函数里，好几百行，全是if else，导致有问题我也很难找出来。现在打算重写。看了一些网上的资料和开源框架，模拟交易主要有for循环模式和事件驱动模式两种方式，前者速度较快，实现简单，但移植到实盘交易系统里需要重新修改很多。后者速度慢，实现复杂，但可以很方便的用于实盘交易。由于我不是搞高频交易，只是研究，就用for循环模式吧。画了个流程图。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0112-mnjyxt/01.png)
从图里可以分出这么几个模块：市值计算模块，止盈判断模块，止盈操作模块，退出止盈模块，正常交易模块，数据更新模块，计算回测数据模块。其中会变动的主要是止盈判断，止盈操作，退出止盈模块，其它的变动较小。写一个类吧。
新建了一个simulate分支，建立模拟程序框架。
```python
# -*- coding:utf-8 -*-
# 模拟交易程序


class simulate(object):
    def __init__(self, totalTimes):
        self.tradeTimes = 0  #已经交易次数
        self.totalTimes = totalTimes
        pass
       
    # 计算持仓股票市值
    def getValue(self):
        pass
       
    # 判断是否进行止盈操作
    def isStopProfit(self):
        pass
       
    # 进行止盈操作
    def doStopProfit(self):
        pass
       
    # 进行交易
    def doTrade(self):
        pass
       
    # 判断是否需要重新购买
    def isReturnBuy(self):
        pass
       
    # 用止盈的钱重新购买etf
    def doReturnBuy(self):
        pass
       
    # 更新相关数据
    def updateData(self):
        pass
       
    #计算回测指标
    def getIndex(self):
        pass
       
    # 执行交易循环
    def run(self):
        while self.tradeTimes < self.totalTimes:
            self.getValue()
            if self.isStopProfit():
                self.doStopProfit()
            else:
                if self.isReturnBuy():
                    self.doReturnBuy()
                else:
                    self.doTrade()
            self.updateData()
            self.tradeTimes += 1
        self.getIndex()
           

if __name__ == "__main__":
    test = simulate(10)
    test.run()
```
现在就往里面填东西吧。
先把不带止盈操作的交易程序给写出来，然后画收益率的图看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0112-mnjyxt/02.png)
跟之前的差不多了，接下来就是难点，进行止盈操作，和回测数据计算了。
距离上次发博文过了很长时间，一方面是我去参加华南口腔展，另一方面是我被卡主了，程序老也调不对。我还在知乎上提问，有大神建议我不要用收益率做止盈止损指标，用股价做指标比较好。又大改程序，主要是止盈和停止止盈的程序，以及计算收益率等数据的程序。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0112-mnjyxt/03.png)
```python
# 执行交易循环
    def run(self):
        for days in range(self.totalTimes):
            if days % self.freq == 0: #进行交易
                self.doTrade(days)
            else:
                for code in range(2):
                    self.update(code, days)
            # print("位置a", days, self.value[0][days], self.cost[0][days], self.rate[0][days], self.value[1][days], self.cost[1][days], self.rate[1][days], self.totalrate[days])
            if days == 0:
                self.minPrice[0] = self.data[0]["close"][0]
                self.minPrice[1] = self.data[1]["close"][0]
                self.maxPrice[0] = self.data[0]["close"][0]
                self.maxPrice[1] = self.data[1]["close"][0]
            else:
                for code in range(2):
                    if self.isStopProfit(code, days):
                        self.doStopProfit(code, days)
                        # print(code, days, "止盈")
                        # print(code, days, self.cost[code][days-1], self.value[code][days-1], self.cost[code][days], self.value[code][days])

            for code in range(2):
                if self.isReturnBuy(code, days):
                    self.doReturnBuy(code, days)
                    # print(code, days, "停止止盈")
                    # print(code, days, self.cost[code][days-1], self.value[code][days-1], self.cost[code][days], self.value[code][days])

            # # 止盈后更新数据
            # for code in range(2):
            #     self.cutUpdate(code, days)
            self.combine(days)
            # print("位置b", days, self.value[0][days], self.cost[0][days], self.rate[0][days], self.value[1][days], self.cost[1][days], self.rate[1][days], self.totalrate[days])
            self.tradeTimes += 1
            # print(days, self.totalcost[days], self.totalvalue[days], self.totalrate[days])
        self.getIndex()
        # 作图测试
        plt.figure()
        plt.plot(self.rate[0], label = "300etf", linestyle = "-")
        plt.plot(self.data[0]["close"]/self.data[0]["close"][0]-1.0, label = "300", linestyle = "-.")
        plt.legend(loc="best")
        # plt.show()
        plt.savefig("simulate_01.png")
        plt.figure()
        plt.plot(self.rate[1], label = "nasetf", linestyle = "--")
        plt.plot(self.data[1]["close"]/self.data[1]["close"][0]-1.0, label = "nas", linestyle = ":")
        plt.legend(loc="best")
        # plt.show()
        plt.savefig("simulate_02.png")
        plt.figure()
        plt.plot(self.data[0]["close"]/self.data[0]["close"][0]-1.0, label = "300", linestyle = "-.")
        plt.plot(self.data[1]["close"]/self.data[1]["close"][0]-1.0, label = "nas", linestyle = ":")
        plt.plot(self.totalrate, label = "total")
        plt.legend(loc="best")
        # plt.show()
        plt.savefig("simulate_03.png")
        
        plt.figure()
        
        plt.plot(self.value[0], label = "300value")
        plt.plot(self.cost[0], label = "300cost")
        plt.legend(loc = "best")
        plt.savefig("debug1.png")
        
        plt.figure()
        
        plt.plot(self.value[1], label = "nasvalue")
        plt.plot(self.cost[1], label = "nascost")
        plt.legend(loc = "best")
        plt.savefig("debug2.png")
```
先说下我止盈和停止止盈的策略:当股价从最高点下跌10%，卖出存量股票的一半，再下跌10%，再卖剩下的一半，直到股票数量不足一手的时候停止。当进行了止盈操作，股价从最低点上涨10%，用之前止盈累计剩下的钱中的一半以现价买入股票，再涨10%，再买一半，直到剩下的钱不够买一手时停止。止盈操作不影响正常按期定投。止盈点和停止止盈点(在上面是10%)可以自行设定。
```python
# 判断是否进行止盈操作，根据days前的交易情况，code为0或1
    def isStopProfit(self, code, days):
        # return False # 测试用
        price = self.data[code]["close"][days]
        # 没有正在进行止盈
        if self.bStop[code] == False:
            if self.minPrice[code] > price:
                self.minPrice[code] = price
            if self.maxPrice[code] < price:
                self.maxPrice[code] = price
            # 判断止盈条件
            if price/self.maxPrice[code] <= 1.0 - self.stopPoint:
                self.bStop[code] = True
                # 将最高/低价调整到现价
                self.maxPrice[code] = price
                self.minPrice[code] = price
                return True
        # 如果已经进行了止盈
        if self.bStop[code] == True:
            if self.minPrice[code] > price:
                self.minPrice[code] = price
            # 判断止盈条件
            if price/self.maxPrice[code] <= 1.0 - self.stopPoint:
                # 将最高/低价调整到现价
                self.maxPrice[code] = price
                self.minPrice[code] = price
                return True
        return False
                
        
    # 进行止盈操作
    def doStopProfit(self, code, days):
        money = self.value[code][days-1]/2.0
        num = self.getTradeNumber(money, self.data[code]["close"][days])
        value = num * self.data[code]["close"][days]
        fee = self.getFee(num, self.data[code]["close"][days])
        # 更新数据
        # 只有股票数量大于一手并且交易金额小于预定金额才做
        if num > 100 and value + fee <= money:
            # print("止盈前", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
            self.money_cut[code] += value - fee
        
            # print("a", code, days, money, num, value, fee)
            # 进行止盈操作
            self.stock[code][days] -= num
            self.value[code][days] -= value
            self.fee[code][days] += fee
            self.rate[code][days] = (self.value[code][days] + self.money_cut[code])/ self.cost[code][days] -1.0
            #self.cutValue[code] = value
#            self.cutFee[code] = fee
            # print(self.cost[code])
            # print(self.value[code])
            # print(self.rate[code])
            # print("止盈后", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
        else:
            self.bStop[code] = False
        

    # 判断是否需要重新购买
    def isReturnBuy(self, code, days):
        # return False #测试用
        # 如果进行了止盈，判断是否停止止盈
        if self.bStop[code] == True or self.bStart[code] == True:
            price = self.data[code]["close"][days]
            if price/self.minPrice[code] >= 1.0 + self.startPoint:
                self.bStart[code] = True
                # 将最高/低价调整到现价
                self.maxPrice[code] = price
                self.minPrice[code] = price
                # 停止止盈
                self.bStop[code] = False
                return True
        return False


    # 用止盈的钱重新购买etf
    def doReturnBuy(self, code, days):
        # 用止盈得到的剩余的钱的一半以现价再投资。
        money = self.money_cut[code]/2.0
        num = self.getTradeNumber(money, self.data[code]["close"][days])
        value = num * self.data[code]["close"][days]
        fee = self.getFee(num, self.data[code]["close"][days])
        # print("止盈", code, days, money, num, value, fee)
        # 如果可以交易的股票数量低于一手，或者股价+手续费大于预定的金额，则停止交易。
        if num <= 100 or value + fee > money:
            self.bStart[code] = False
        else: # 进行交易并更新数据。
            # print("停止止盈前", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
            self.stock[code][days] += num
            self.value[code][days] += value
            self.fee[code][days] += fee
            self.money_cut[code] -= value+fee
            # print("停止止盈后", code, days, self.value[code][days], self.cost[code][days], self.stock[code][days], self.rate[code][days], num, value, fee)
```
再看计算收益率，一开始我还是用市值/成本的方法，结果一止盈收益率就急降，后来把计算方法改成(市值+止盈得到的钱-手续费)/成本，看起来就差不多了。但画出图来感觉还是有问题，跟完全不止盈效果也差不多啊。
这是单独看两个etf的股价和收益率变化情况。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0112-mnjyxt/04.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0112-mnjyxt/05.png)
尤其纳指etf，怎么低那么多？
总的收益率
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0112-mnjyxt/06.png)
感觉还有问题，再仔细看看。另外可以开始写计算回测指标的程序了。之前写的感觉有问题，打算重来。
完整代码：https://github.com/zwdnet/etfdata/blob/simulate/simulate.py
我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“好看”。谢谢。
我的个人博客地址：https://zwdnet.github.io
我的CSDN博客地址：https://blog.csdn.net/zwdnet
我的微信个人订阅号：赵瑜敏的口腔医学学习园地

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)

