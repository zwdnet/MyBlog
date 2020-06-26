---
title: 量化投资学习笔记69——量化回测框架backtrader
date: 2020-06-26 12:02:52
tags: [量化投资,Backtrader,Python,学习笔记]
categories: 量化投资
---
从开始学量化交易以来，我先后试了bt和pyalgotrade两个框架，都有一些问题。最近得知backtrader这个单机的量化投资回测框架，试了一下能装上，就尝试一下吧。本文是我看官方文档并进行尝试的记录。
文档地址: https://www.backtrader.com/docu/
这个框架的主要目标就是易用。
运行框架的基本步骤:
1.创建一个策略
①确定可能需要调整的参数。
②实现策略中需要的指标。
③写买入卖出逻辑。
2.创建一个回测引擎(Cerebro Engine)
①插入一个策略。
②加载并插入一个数据源。
③运行引擎。
④可视化回测结果(cerebro.plot())
安装: pip install backtrader
backtrader的两个基本概念:
1.Lines(不知道咋翻了)
数据源，指标和策略有Lines。一系列在时间上连续的数据点称为线。数据源含有"Open, High, Low, Close, Volume, OpenInterest"六条线，如果加上日期就是七条。
2.0索引
在一条Line中，当前值的索引为0。最后输出值的索引为-1。即当前时刻的索引为0，当前时刻之前的时刻的索引为-1。更早的时刻可以用-2，-3等获得。
默认的，引擎会在后台建立broker实例，还有默认的初始金额，是1万货币单位。如果没改变，就会使用默认值。这会简化使用。
设置初始资金，用cerebro.broker.setcash()函数。
框架使用的数据源为bt.feeds，支持雅虎金融，谷歌金融等格式，对于国内常用的tushare，先保存为DataFrame，再用bt.feeds.PandasData()转换成数据源。要求是有'open','high','low','close','volume','openinterest'六列，其中'openinterest'可设为0。另外DataFrame需要以datetime类型的date列为索引。建立以后用cerebro.adddata()将数据载入引擎。
现在就实现第一个策略了，每个交易日都输出股价现值。
```python
# coding:utf-8
# backtrader的第一个策略


import datetime
import sys
import pandas as pd
import backtrader as bt
import tushare as ts


# 创建一个策略
class TestStrategy(bt.Strategy):
    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))
       
    def __init__(self):
        self.dataclose = self.datas[0].close
       
    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # 加载数据
    start = "2019-01-01"
    end = "2019-12-31"
    df = ts.get_k_data("510300", autype = "qfq", start = start,  end = end)
    df.index = pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    data = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2019, 1, 1), todate = datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)
    # 设置初始资金
    cerebro.broker.setcash(100000.0)
    print("初始资金:%.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("期末资金:%.2f" % cerebro.broker.getvalue())
```
```python
初始资金:100000.00
2019-01-02, Close, 3.02
2019-01-03, Close, 3.02
2019-01-04, Close, 3.09
2019-01-07, Close, 3.11
2019-01-08, Close, 3.11
2019-01-09, Close, 3.13
2019-01-10, Close, 3.13
2019-01-11, Close, 3.16
......
2019-12-20, Close, 4.02
2019-12-23, Close, 3.96
2019-12-24, Close, 3.98
2019-12-25, Close, 3.99
2019-12-26, Close, 4.02
2019-12-27, Close, 4.02
2019-12-30, Close, 4.08
2019-12-31, Close, 4.10
期末资金:100000.00
```
框架的策略类有python的list数据，名为datas。其中第一个数据self.datas[0]是交易操作的默认数据并随策略保持同步。
self.dataclose = self.datas[0].close保存收盘价的地址。
在每次数据源更新时都会调用策略的next()成员函数。
接着在策略中增加一些逻辑。
```python
    def next(self):
        self.log("Close, %.2f" % self.dataclose[0])
        # 今天收盘价比昨天低
        if self.dataclose[0] < self.dataclose[-1]:
            # 昨天收盘价比前天低
            if self.dataclose[-1] < self.dataclose[-2]:
                # 买买买
                self.log("在%.2f创建买单" % self.dataclose[0])
                self.buy()
```
连续两天下跌就买入。
```python
初始资金:100000.00
2019-01-02, Close, 3.02
2019-01-03, Close, 3.02
2019-01-04, Close, 3.09
2019-01-07, Close, 3.11
2019-01-08, Close, 3.11
2019-01-09, Close, 3.13
2019-01-10, Close, 3.13
2019-01-11, Close, 3.16
2019-01-14, Close, 3.13
2019-01-15, Close, 3.19
2019-01-16, Close, 3.13
2019-01-17, Close, 3.11
2019-01-17, 在3.11创建买单
......
2019-12-20, 在4.02创建买单
2019-12-23, Close, 3.96
2019-12-23, 在3.96创建买单
2019-12-24, Close, 3.98
2019-12-25, Close, 3.99
2019-12-26, Close, 4.02
2019-12-27, Close, 4.02
2019-12-30, Close, 4.08
2019-12-31, Close, 4.10
期末资金:100014.36
```
现在的问题是不知道买单何时执行，成交价多少。
在默认情况下，购买self.datas[0]的证券，买入量固定为1股每次，框架在买入指令下达后的下一个交易日以开盘价执行交易，没有考虑交易成本。这些都可以改变的。
接下来考虑卖出。框架策略有position属性，保存仓位。买卖命令都返回created命令(还没有执行)。通过策略的notify方法可以得到交易状态改变的通知。数据源的每个bar的时间单位并没有确定，天，周，月等都可以。
下面修改策略，在买入5个交易周期后卖出。
```python
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        '''log记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查一个交易是否完成。
        # 如果钱不够，交易会被拒绝。
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('执行买入, 价格%.2f' % order.executed.price)
            elif order.issell():
                self.log('执行卖出, 价格%.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消/被拒绝。')

        self.order = None

    def next(self):
        # 输出持仓
        self.log('持仓 %.2f' % self.position.size)

        # 检查是否有交易在进行，不能提交第二个
        if self.order:
            return

        # 检查是否有持仓
        if not self.position:

            # 没有持仓，检查是否达到买入条件
            if self.dataclose[0] < self.dataclose[-1]:
                    if self.dataclose[-1] < self.dataclose[-2]:
                        # 买买买，以默认参数
                        self.log('买单创建, 价格%.2f' % self.dataclose[0])
                        # 创建买单
                        self.order = self.buy()

        else:
            # 已经有持仓了，卖出
            if len(self) >= (self.bar_executed + 5):
                # 卖卖卖，以默认参数
                self.log('卖单创建, 价格%.2f' % self.dataclose[0])
                # 创建卖单
                self.order = self.sell()
```
结果
```python
初始资金:100000.00
2019-01-02, 持仓 0.00
2019-01-03, 持仓 0.00
2019-01-04, 持仓 0.00
2019-01-07, 持仓 0.00
2019-01-08, 持仓 0.00
2019-01-09, 持仓 0.00
2019-01-10, 持仓 0.00
2019-01-11, 持仓 0.00
2019-01-14, 持仓 0.00
2019-01-15, 持仓 0.00
2019-01-16, 持仓 0.00
2019-01-17, 持仓 0.00
2019-01-17, 买单创建, 价格3.11
2019-01-18, 执行买入, 价格3.12
2019-01-18, 持仓 1.00
2019-01-21, 持仓 1.00
2019-01-22, 持仓 1.00
……
2019-12-25, 持仓 1.00
2019-12-26, 持仓 1.00
2019-12-27, 持仓 1.00
2019-12-30, 持仓 1.00
2019-12-31, 持仓 1.00
2019-12-31, 卖单创建, 价格4.10
期末资金:100000.80
```
下面再加上手续费，费率0.1%。
用cerebro.broker.setcommission(commission=0.001)
并在策略里输出手续费。
```python
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        '''log记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查一个交易是否完成。
        # 如果钱不够，交易会被拒绝。
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            elif order.issell():
                self.log(
                    '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消/被拒绝。')

        self.order = None
       
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('操作收益%.2f, 成本%.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # 输出持仓
        self.log('持仓 %.2f' % self.position.size)

        # 检查是否有交易在进行，不能提交第二个
        if self.order:
            return

        # 检查是否有持仓
        if not self.position:

            # 没有持仓，检查是否达到买入条件
            if self.dataclose[0] < self.dataclose[-1]:
                    if self.dataclose[-1] < self.dataclose[-2]:
                        # 买买买，以默认参数
                        self.log('买单创建, 价格%.2f' % self.dataclose[0])
                        # 创建买单
                        self.order = self.buy()

        else:
            # 已经有持仓了，卖出
            if len(self) >= (self.bar_executed + 5):
                # 卖卖卖，以默认参数
                self.log('卖单创建, 价格%.2f' % self.dataclose[0])
                # 创建卖单
                self.order = self.sell()
```
结果
```python
……
2019-12-23, 操作收益0.09, 成本0.08
2019-12-23, 持仓 0.00
2019-12-23, 买单创建, 价格3.96
2019-12-24, 执行买入, 价格: 3.96, 成本: 3.96, 手续费 0.00
2019-12-24, 持仓 1.00
2019-12-25, 持仓 1.00
2019-12-26, 持仓 1.00
2019-12-27, 持仓 1.00
2019-12-30, 持仓 1.00
2019-12-31, 持仓 1.00
2019-12-31, 卖单创建, 价格4.10
期末资金:100000.64
```
注意因为最后一天仍然有持仓，所以最后的收益与每次交易后收益之和的累加有差异。
可以在策略中定义一些参数以配置策略。
用Python的tuple在策略类里定义
```python
    params = (
    ('myparam', 27),
    ('exitbars', 5),
)
```
然后在addstrategy中以参数形式给参数赋值。
cerebro.addstrategy(TestStrategy, myparam=20, exitbars=7)
可以用addsizer来设置交易量。
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

把这些结合起来。
```python
# coding:utf-8
# backtrader的第一个策略


import datetime
import sys
import pandas as pd
import backtrader as bt
import tushare as ts
               
               
class TestStrategy(bt.Strategy):
    params = (
        ("exitbars", 5),
    )
    def log(self, txt, dt=None):
        '''log记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查一个交易是否完成。
        # 如果钱不够，交易会被拒绝。
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消/被拒绝。')

        self.order = None
       
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('操作收益%.2f, 成本%.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # 输出持仓
        self.log('持仓 %.2f' % self.position.size)

        # 检查是否有交易在进行，不能提交第二个
        if self.order:
            return

        # 检查是否有持仓
        if not self.position:

            # 没有持仓，检查是否达到买入条件
            if self.dataclose[0] < self.dataclose[-1]:
                    if self.dataclose[-1] < self.dataclose[-2]:
                        # 买买买，以默认参数
                        self.log('买单创建, 价格%.2f' % self.dataclose[0])
                        # 创建买单
                        self.order = self.buy()

        else:
            # 已经有持仓了，卖出
            if len(self) >= (self.bar_executed + self.params.exitbars):
                # 卖卖卖，以默认参数
                self.log('卖单创建, 价格%.2f' % self.dataclose[0])
                # 创建卖单
                self.order = self.sell()


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # 加载数据
    start = "2019-01-01"
    end = "2019-12-31"
    # df = ts.get_k_data("510300", autype = "qfq", start = start,  end = end)
    # df.to_csv("data.csv")
    df = pd.read_csv("data.csv")
    df.index = pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    data = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2019, 1, 1), todate = datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)
    # 设置初始资金
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    print("初始资金:%.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("期末资金:%.2f" % cerebro.broker.getvalue())
```
接下来就可以增加指标了。
下面考虑简单移动平均线策略:
收盘价高于均值就买入;如果有持仓，收盘价低于均值则卖出;同时只能有一个交易。
用bt.indicators.MovingAverageSimple
```python
# coding:utf-8
# backtrader的第一个策略


import datetime
import sys
import pandas as pd
import backtrader as bt
import tushare as ts
               
               
class TestStrategy(bt.Strategy):
    params = (
        ("maperiod", 15),
    )
    def log(self, txt, dt=None):
        '''log记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
       
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.maperiod)

    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查一个交易是否完成。
        # 如果钱不够，交易会被拒绝。
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消/被拒绝。')

        self.order = None
       
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('操作收益%.2f, 成本%.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # 输出持仓
        self.log('持仓 %.2f' % self.position.size)

        # 检查是否有交易在进行，不能提交第二个
        if self.order:
            return

        # 检查是否有持仓
        if not self.position:

            # 没有持仓，检查是否达到买入条件
            if self.dataclose[0] > self.sma[0]:
                # 买买买，以默认参数
                self.log('买单创建, 价格%.2f' % self.dataclose[0])
                # 创建买单
                self.order = self.buy()

        else:
            # 已经有持仓了，股价低于平均价格，卖出
            if self.dataclose[0] < self.sma[0]:
                # 卖卖卖，以默认参数
                self.log('卖单创建, 价格%.2f' % self.dataclose[0])
                # 创建卖单
                self.order = self.sell()


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # 加载数据
    start = "2019-01-01"
    end = "2019-12-31"
    # df = ts.get_k_data("510300", autype = "qfq", start = start,  end = end)
    # df.to_csv("data.csv")
    df = pd.read_csv("data.csv")
    df.index = pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    data = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2019, 1, 1), todate = datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)
    # 设置初始资金
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    print("初始资金:%.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("期末资金:%.2f" % cerebro.broker.getvalue())
```
结果
```python
……
2019-12-11, 卖单创建, 价格3.90
2019-12-12, 执行卖出, 价格: 3.90, 成本: 394.40, 手续 费 0.39
2019-12-12, 操作收益-4.30, 成本-5.08
2019-12-12, 持仓 0.00
2019-12-13, 持仓 0.00
2019-12-13, 买单创建, 价格3.97
2019-12-16, 执行买入, 价格: 3.97, 成本: 396.70, 手续 费 0.40
2019-12-16, 持仓 100.00
2019-12-17, 持仓 100.00
2019-12-18, 持仓 100.00
2019-12-19, 持仓 100.00
2019-12-20, 持仓 100.00
2019-12-23, 持仓 100.00
2019-12-24, 持仓 100.00
2019-12-25, 持仓 100.00
2019-12-26, 持仓 100.00
2019-12-27, 持仓 100.00
2019-12-30, 持仓 100.00
2019-12-31, 持仓 100.00
期末资金:1055.60
```
注意是从第15个交易日开始交易的。框架假设所使用的指标是已经准备好的，当指标没有准备好时，交易不会开始。
可视化，用cerebro.plot()完成。
为了画更多的图像，可以加入更多的均线等指标。
```python
# coding:utf-8
# backtrader的第一个策略


import datetime
import sys
import pandas as pd
import backtrader as bt
import tushare as ts
import matplotlib.pyplot as plt
               
               
class TestStrategy(bt.Strategy):
    params = (
        ("maperiod", 15),
    )
    def log(self, txt, dt=None):
        '''log记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
       
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.maperiod)
        # 一些要画的指标
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot = False)

    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查一个交易是否完成。
        # 如果钱不够，交易会被拒绝。
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消/被拒绝。')

        self.order = None
       
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('操作收益%.2f, 成本%.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # 输出持仓
        self.log('持仓 %.2f' % self.position.size)

        # 检查是否有交易在进行，不能提交第二个
        if self.order:
            return

        # 检查是否有持仓
        if not self.position:

            # 没有持仓，检查是否达到买入条件
            if self.dataclose[0] > self.sma[0]:
                # 买买买，以默认参数
                self.log('买单创建, 价格%.2f' % self.dataclose[0])
                # 创建买单
                self.order = self.buy()

        else:
            # 已经有持仓了，股价低于平均价格，卖出
            if self.dataclose[0] < self.sma[0]:
                # 卖卖卖，以默认参数
                self.log('卖单创建, 价格%.2f' % self.dataclose[0])
                # 创建卖单
                self.order = self.sell()


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # 加载数据
    start = "2019-01-01"
    end = "2019-12-31"
    # df = ts.get_k_data("510300", autype = "qfq", start = start,  end = end)
    # df.to_csv("data.csv")
    df = pd.read_csv("data.csv")
    df.index = pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    data = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2019, 1, 1), todate = datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)
    # 设置初始资金
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    print("初始资金:%.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("期末资金:%.2f" % cerebro.broker.getvalue())
    cerebro.plot()
    plt.savefig("result.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/44/01.png)
尽管交易逻辑没变，结果却变了，因为数据不一样了。2月25日才计算完所有指标开始交易。
最后来看看优化。不同的市场和交易品种可能有不同的参数。可以在一个范围内改变参数取值来看回测结果。但注意不要过度优化，那样好的结果只适合于特定的数据集。还是用上面的移动均线策略做例子，改变均线周期。
用cerebro.optstrategy(TestStrategy, maperiod = range(10, 31)) 来代替addstrategy()。
```python
# coding:utf-8
# backtrader的第一个策略


import datetime
import sys
import pandas as pd
import backtrader as bt
import tushare as ts
import matplotlib.pyplot as plt
               
               
class TestStrategy(bt.Strategy):
    params = (
        ("maperiod", 15),
        ("printlog", False),
    )
    def log(self, txt, dt=None, doprint=False):
        '''log记录'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
       
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period = self.params.maperiod)

    def notify_order(self, order):
        # 有交易提交/被接受，啥也不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 检查一个交易是否完成。
        # 如果钱不够，交易会被拒绝。
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '执行买入, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    '执行卖出, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消/被拒绝。')

        self.order = None
       
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('操作收益%.2f, 成本%.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # 输出持仓
        self.log('持仓 %.2f' % self.position.size)

        # 检查是否有交易在进行，不能提交第二个
        if self.order:
            return

        # 检查是否有持仓
        if not self.position:

            # 没有持仓，检查是否达到买入条件
            if self.dataclose[0] > self.sma[0]:
                # 买买买，以默认参数
                self.log('买单创建, 价格%.2f' % self.dataclose[0])
                # 创建买单
                self.order = self.buy()

        else:
            # 已经有持仓了，股价低于平均价格，卖出
            if self.dataclose[0] < self.sma[0]:
                # 卖卖卖，以默认参数
                self.log('卖单创建, 价格%.2f' % self.dataclose[0])
                # 创建卖单
                self.order = self.sell()
               
    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' % (self.params.maperiod, self.broker.getvalue()), doprint=True)



if __name__ == "__main__":
    cerebro = bt.Cerebro()
    # cerebro.addstrategy(TestStrategy)
    # 用参数优化代替添加策略
    strats = cerebro.optstrategy(TestStrategy, maperiod = range(10, 31))
    # 加载数据
    start = "2019-01-01"
    end = "2019-12-31"
    # df = ts.get_k_data("510300", autype = "qfq", start = start,  end = end)
    # df.to_csv("data.csv")
    df = pd.read_csv("data.csv")
    df.index = pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    data = bt.feeds.PandasData(dataname = df, fromdate = datetime.datetime(2019, 1, 1), todate = datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)
    # 设置初始资金
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    print("初始资金:%.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus = 1)
    # print("期末资金:%.2f" % cerebro.broker.getvalue())
    # cerebro.plot()
    # plt.savefig("result.png")
```
运行结果
```python
$ python first.py
初始资金:1000.00
2019-12-31, (MA Period 10) Ending Value 1031.22
2019-12-31, (MA Period 11) Ending Value 1018.49
2019-12-31, (MA Period 12) Ending Value 1027.47
2019-12-31, (MA Period 13) Ending Value 1038.64
2019-12-31, (MA Period 14) Ending Value 1052.18
2019-12-31, (MA Period 15) Ending Value 1055.60
2019-12-31, (MA Period 16) Ending Value 1054.62
2019-12-31, (MA Period 17) Ending Value 1058.46
2019-12-31, (MA Period 18) Ending Value 1053.79
2019-12-31, (MA Period 19) Ending Value 1050.40
2019-12-31, (MA Period 20) Ending Value 1046.80
2019-12-31, (MA Period 21) Ending Value 1042.11
2019-12-31, (MA Period 22) Ending Value 1042.97
2019-12-31, (MA Period 23) Ending Value 1035.79
2019-12-31, (MA Period 24) Ending Value 1034.00
2019-12-31, (MA Period 25) Ending Value 1030.99
2019-12-31, (MA Period 26) Ending Value 1029.02
2019-12-31, (MA Period 27) Ending Value 1023.43
2019-12-31, (MA Period 28) Ending Value 1052.18
2019-12-31, (MA Period 29) Ending Value 1040.87
2019-12-31, (MA Period 30) Ending Value 1039.77
```
用17日均线收益最高。
更进一步的改进:自定义指标，设置Sizer(资金管理)，交易类型(限价等)。
接下来打算看一遍官网的文档，写个回测实操下。



我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)