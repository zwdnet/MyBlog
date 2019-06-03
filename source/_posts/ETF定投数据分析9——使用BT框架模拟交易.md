---
title: ETF定投数据分析9——使用BT框架模拟交易
date: 2019-06-03 15:41:04
tags: [ETF,投资理财,定投,Python,模拟交易,回测框架,BT]
categories: 计算机
---
距离上次文章已经过去几个月了，我一直在与模拟交易挣扎。代码已经能运行了，但是想添加止盈止损的策略，总是调不对。具体可以看项目github库(https://github.com/zwdnet/etfdata)里的simulate分支里的simulater2.py。
后来，我想不能再这么挣扎下去了。于是就在网上找量化投资的python库。几番尝试找到一个叫bt的库，是建立在ffn基础上的。试了一下，pydroid3里能装的，就用它吧。
官方文档地址: http://pmorissette.github.io/bt/index.html
以下翻译自官方文档:
bt是一个灵活的用于测试量化投资策略的Python回测框架。回测(Backtesting)是用给定的数据集测试量化投资策略的过程。本框架能使您容易的建立混合和匹配不同算法的策略。
目标是节省量化投资者重新造轮子的时间，使他们专注于工作的重要部分——策略开发。
一个例子
``` python
import bt

# 首先下载数据
data = bt.get('spy,agg', start='2010-01-01')
"""这是通过yahoo下载的数据，要下载A股数据要用其它工具，例如tushare"""

# 接着，创建策略
s = bt.Strategy('s1', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
"""第一个参数是策略名称，第二个策略是一个包含策略具体内容的list，包括操作间隔，选股策略，权重，和再平衡策略。这里都使用algos类里的函数，如果没满足需要也可以自定义。"""
"""最后，建立一个回测Backtest，在策略与数据之间建立逻辑联系。"""
test = bt.Backtest(s, data)
# 然后就可以运行回测了
res = bt.run(test)
# 之后就可以查看结果了
res.plot()
res.display()
```
以上是文档里的例子，还有其它例子，我照着敲了一遍，详见btExample.py。
总结一下，使用bt框架的主要步骤是:获取数据->建立策略->建立回测->运行回测->获得结果。关键是建立策略。
下面开始用bt跑我自己的数据跟策略吧。首先先获得数据，就用我之前下载到csv文件的数据吧。
``` python
#获取数据
def GetData():
    #读取数据
    df_300 = pd.read_csv("df_300_hist.csv")
    df_nas = pd.read_csv("df_nas_hist.csv")
    #只保留收盘价
    length1 = len(df_300)
    length2 = len(df_nas)
    df_300 = df_300.loc[0:length1, ["date", "close"]]
    df_nas = df_nas.loc[0:length2, ["date", "close"]]
    # 更改数据格式，使其符合bt要求
    df_300.columns = ["Date", "300etf"]
    df_300["Date"] = pd.to_datetime(df_300["Date"])
    df_300.set_index("Date", inplace = True)
   
    df_nas.columns = ["Date", "nasetf"]
    df_nas["Date"] = pd.to_datetime(df_nas["Date"])
    df_nas.set_index("Date", inplace = True)
   
    # 合并数据
    data = pd.concat([df_300, df_nas], axis = 1, join = "inner")
   
    # 返回数据
    return data
```
bt框架对数据的要求是以"Date"为index，所以进行了相应的转换，最后把数据合并。
接着开始建立策略，先用没有止盈止损的策略。
``` python
# 建立策略
def CreateStrategy(name):
    strategy = bt.Strategy(name,
    [bt.alogs.RunWeekly(),
     bt.algos.SelectAll(),
     bt.algos.WeighEqually(),
     bt.algos.Rebalance()
    ])
    return strategy
```
主要参数就是策略名称，还有一个列表，包含的内容主要为执行策略的间隔，选股策略，权重，以及是否再平衡。一些常用的选项都在bt.algos模块里定义了，如果不满足需要，可以自行定义。
策略建立好以后就建立回测，所谓回测就是把策略和数据结合在一起的结构。在其中也可以指定投入初始资金等。注意策略会进行深度复制，即在回测中原始数据不会被改变，可以用在其它回测中。
``` python
test = bt.Backtest(strategy, data)
```
最后运行回测
``` python
res = bt.run(test)
```
以不同的方式输出回测结果
``` python
# 输出回测结果
def outputResult(res):
    fig = res.plot()
    plt.savefig("BTStimulateTest.png")
    res.display()
    fig = res.plot_histogram()
    plt.savefig("BTStimulateHistTest.png")
    res.plot_security_weights()
    plt.savefig("BTStimulateWeights.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0137-etfdata/01.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0137-etfdata/02.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0137-etfdata/03.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0137-etfdata/04.png)
搞定!总收益率110%，最大回撤26.5%。还不错。但是还有个问题，怎么设定添加交易手续费？
方法是定义一个计算手续费的函数，
``` python
# 计算交易手续费
def getFee(quantity, price):
    rate = 0.0003
    fee = quantity*price*rate
    if fee < 0.1:
        fee = 0.1
    return fee
```
然后用strategy.set_commissions(getFee)将该函数传递给策略。测试了一下(把佣金费率改大，到3%。再大，比如到30%，运行会报错。)，总收益率是下降的。说明是对的。
接下来就是怎么把止盈止损策略加到策略里的问题了。下次吧。
我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“好看”。
我的个人博客地址：https://zwdnet.github.io
我的个人博客地址：https://zwdnet.github.io
我的CSDN博客地址：https://blog.csdn.net/zwdnet
我的微信个人订阅号：赵瑜敏的口腔医学学习园地

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)

