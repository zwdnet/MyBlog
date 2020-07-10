---
title: 量化投资学习笔记73——backtrader实操
date: 2020-07-10 10:49:51
tags: [量化投资,Backtrader,Python,学习笔记]
categories: 量化投资
---
上次了解了backtrader的基本内容和使用方法。下面就用backtrader框架来解决一个问题:回测一下我的实盘数据。
我从2018年开始股票定投，就两个:300etf和纳指etf。开始每个月一次，后来每隔十天一次。由于时间并不绝对固定，没法直接用算法来描述。我从券商APP里把交易记录人肉输入到一个csv文件里，像这样。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/01.png)
下面就用backtrader来回测一下。先用tushare下载历史数据并保存到文件里。并转换成backtrader可以接受的形式。
```python
# 获取数据
def getData(code, start, end):
    filename = code+".csv"
    print("./" + filename)
    # 已有数据文件，直接读取数据
    if os.path.exists("./" + filename):
        df = pd.read_csv(filename)
    else: # 没有数据文件，用tushare下载
        df = ts.get_k_data(code, autype = "qfq", start = start, end = end)
        df.to_csv(filename)
    df.index = pd.to_datetime(df.date)
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    return df
```
下面获取股价数据，并建立数据源。
```python
if __name__ == "__main__":
    start = "2018-01-01"
    end = "2020-05-31"
    df_300 = getData("510300", start, end)
    df_nas = getData("513100", start, end)
    print(df_300.info(), df_nas.info())
    # 建立数据源
    start_date = list(map(int, start.split("-")))
    end_date = list(map(int, end.split("-")))
    data300 = bt.feeds.PandasData(dataname = df_300, name = "300ETF", fromdate = datetime.datetime(start_date[0], start_date[1], start_date[2]), todate = datetime.datetime(end_date[0], end_date[1], end_date[2]))
    dataNas = bt.feeds.PandasData(dataname = df_nas, name = "nasETF", fromdate = datetime.datetime(start_date[0], start_date[1], start_date[2]), todate = datetime.datetime(end_date[0], end_date[1], end_date[2]))
```
下面建立策略类，先写最简单的，直接显示股价。
```python
# 交易策略
class TradeStrategy(bt.Strategy):
    def __init__(self):
        pass
       
    def next(self):
        for data in self.datas:
            print("name :%s, price:%.2f" % (data._name, data[0]))
```
然后建立cerebro实例，加载数据和策略。
```python
    # 建立回测实例，加载数据，策略。
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TradeStrategy)
    cerebro.adddata(data300, name = "300ETF")
    cerebro.adddata(dataNas, name = "nasETF")
```
最后运行回测。
```python
    # 运行回测
    cerebro.run()
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/02.png)
搞定!
接下来，把我的交易记录读入，根据交易记录进行交易。
折腾了好久，主要是datetime作为DataFrame的索引，如何找出某个日期的数据呢？用datetime的strftime函数输出字符串，再用loc选取数据。具体看下面。
```python
# 交易策略
class TradeStrategy(bt.Strategy):
    params = (
            ("recordFilename", "etfdata.csv"),
    )
    
    def __init__(self):
        self.df_record = pd.read_csv(self.params.recordFilename)
        self.df_record.成交日期 = pd.to_datetime(self.df_record.成交日期, format = "%Y%m%d")
        self.df_record.index = self.df_record.成交日期
        self.df_record.drop(labels = "成交日期", axis = 1, inplace = True)
        # print(self.df_record.head(), self.df_record.info())
        
    def next(self):
        tradeData = pd.DataFrame()
        for data in self.datas:
            date = data.datetime.date(0)
            tradeBar = self.df_record.loc[date.strftime("%Y-%m-%d"),:]
            if len(tradeBar) != 0:
                for i in range(len(tradeBar)):
                    name = tradeBar.iloc[i].证券名称 
                    price = tradeBar.iloc[i].成交均价 
                    stock = tradeBar.iloc[i].成交量 
                    commit = tradeBar.iloc[i].手续费
```
下面就要用这些实盘的数据进行回测交易。
```python
def next(self):
        if self.order:
            return
        tradeData = pd.DataFrame()
        for data in self.datas:
            date = data.datetime.date(0)
            tradeBar = self.df_record.loc[date.strftime("%Y-%m-%d"),:]
            if len(tradeBar) != 0:
                for i in range(len(tradeBar)):
                    name = tradeBar.iloc[i].证券名称 
                    price = tradeBar.iloc[i].成交均价 
                    stock = tradeBar.iloc[i].成交量 
                    commit = tradeBar.iloc[i].手续费
                    print("测试", i, name, price, stock, commit)
                    # 进行交易
                    if stock > 0:
                        self.broker.add_cash(price*stock + commit + 1.0)
                        print(self.broker.get_cash())
                        self.order = self.buy(data = data, size = stock, price = price)
                    else:
                        self.order = self.sell(data = data, size = -1*stock, price = price)
```
跑一下看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/03.png)
有两个问题：貌似一个bar里执行了两次，另外买入日期是第二天，因此有交易失败的情况。
看了半天，原来是因为我没有判断实盘证券名称与bar数据中的证券名称是否一致的原因。另外查了一下交易的exectype类型:
Order.Market或者None：Market订单将以下一个可行的价格进行交易，在回测中，就将以下一根K线的开盘价进行交易。
Order.Limit：在给定的价位price或者更好的价位执行的订单。
Order.Stop：当价格突破price时，触发订单成交。
Order.StopLimit：当价格突破price时触发订单（类似于Order.Stop订单），之后以给定的价位plimit或者更好的价位执行订单（相当于以参数plimit为price的Order.Limit订单）。
Order.StopTrailLimit：Order.StopTrail和Order.Limit的组合，按照Order.StopTrail条件触发，按照Order.Limit条件成交。
Order.Historical：尚未发现相关说明及应用。
以上参考:https://blog.csdn.net/m0_46603114/article/details/106031259
看不太明白，我挨个试了一下。最后结果还是第一个，即以第二天开盘价成交的回测结果与实际结果最接近，但还是差了几千块。就先用这个结果吧。
```python
    def next(self):
        if self.order:
            return
        tradeData = pd.DataFrame()
        orderType = bt.Order.Market
        for data in self.datas:
            date = data.datetime.date(0)
            tradeBar = self.df_record.loc[date.strftime("%Y-%m-%d"),:]
            # print("bar数据", date, data._name)
            if len(tradeBar) != 0:
                for i in range(len(tradeBar)):
                    name = tradeBar.iloc[i].证券名称
                    price = tradeBar.iloc[i].成交均价
                    stock = tradeBar.iloc[i].成交量
                    commit = tradeBar.iloc[i].手续费
                    # 进行交易
                    if stock > 0 and name == data._name:
                        print("测试a", date, name, price, stock, commit)
                        self.broker.add_cash(price*stock + commit)
                        print(self.broker.get_cash())
                        self.order = self.buy(data = data, size = stock, price = price, exectype = orderType)
                    elif stock < 0 and name == data._name:
                        print("测试b", date, name, price, stock, commit)
                        self.order = self.sell(data = data, size = -1*stock, price = price, exectype = orderType)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/04.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/05.png)
绿色标志是买入点，红色是卖出点，接下来看看画图能不能改进。
默认的cerebro.plot()调用有CashValue，Trade，BuySell三个观察器，分别监控总市值，交易盈亏和买卖点。用stdstats参数来控制，默认为True。
有三种方法可以改变绘图数据:
通过adddata, replaydata和resampledata往cerebro里添加数据。
通过addindicator往strategy里添加指标。
通过addobserver往cerebro里添加观察器。
实操一下，先通过添加观察器增加回撤观察器:
```python
    # 添加回撤观察器
    cerebro.addobserver(bt.observers.DrawDown)
```
再到策略类里实现stop函数。输出策略的最大回撤值:
```python
    def stop(self):
        self.log("最大回撤:-%.2f%%" % self.stats.drawdown.maxdrawdown[-1], doprint=True)
```
输出结果:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/06.png)
画的图里也有回撤值的图像。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/07.png)
下面试试在strategy里添加indicator，要注意的是任何在__init__()里声明的indicator都会在next()被调用之前被计算。
关于绘图，声明Indicator会自动绘图，但通过操作符得到的lines对象不会自动绘图，要绘图可以通过LinePlotterIndicator进行。
直接在策略类的__init__()里声明indicators就行啦。
```python
bt.indicators.AroonDown()
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/08.png)
下面来看看怎么修改图片显示参数。indicators和observers有很多选项可以调整图片显示。有三大类，分别是可以控制整个对象，单独某个lines，和整个系统范围内的图像输出。对于indicators和observers可以设置plotinfo参数，可以在定义是直接指定参数及值，也可以在定义了对象之后，设置对象名.plotinfo.参数名。
两个方法都试一下:
```python
    ad = bt.indicators.AroonDown(plotname = "AD")
    ad.plotinfo.subplot = False
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/09.png)
当subplot参数为False时，图与前面一个图形画在一起，如画移动均线时跟股价画到一起。
indicators和observers类中也定义了很多以_开头的函数用来控制绘图。
还有控制整个系统绘图的函数，cerebro.plot(),其中numfigs指定分成几张图，默认为1，我改一下看看。
```python
cerebro.plot(numfigs = 2)
```
貌似没啥用。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/48/10.png)
先这样吧。下面看看怎么加入分析器。
用cerebro.addanalyzer函数加入，在run结束后才计算结果，尽管其在内部也是lines。
```python
import backtrader.analyzers as btay
```
先算个夏普比例
```python
    # 添加分析对象
    cerebro.addanalyzer(btay.SharpeRatio, _name = "sharpe")
    # 运行回测
    results = cerebro.run()
    print("夏普比例:", results[0].analyzers.sharpe.get_analysis())

夏普比例: OrderedDict([('sharperatio', 0.7071076137019872)])
```
才0.707，嘿嘿。
再加几个试试。
```python
    # 添加分析对象
    cerebro.addanalyzer(btay.SharpeRatio, _name = "sharpe")
    cerebro.addanalyzer(btay.AnnualReturn, _name = "AR")
    cerebro.addanalyzer(btay.DrawDown, _name = "DD")
    cerebro.addanalyzer(btay.Returns, _name = "RE")
    cerebro.addanalyzer(btay.TradeAnalyzer, _name = "TA")
......
    print("夏普比例:", results[0].analyzers.sharpe.get_analysis())
    print("年化收益率:", results[0].analyzers.AR.get_analysis())
    print("回撤:", results[0].analyzers.DD.get_analysis())
    print("收益:", results[0].analyzers.RE.get_analysis())
    print("交易统计结果:", results[0].analyzers.TA.get_analysis())
```
这种方式输出很乱，有两种改进方法，一个是直接输出结果字典的某个键值，还有一个方法是调用分析对象的print()成员函数。两种方法都试试:
```python
    print("夏普比例:", results[0].analyzers.sharpe.get_analysis()["sharperatio"])
    print("年化收益率:", results[0].analyzers.AR.get_analysis())
    print("最大回撤:%.2f，最大回撤周期%d" % (results[0].analyzers.DD.get_analysis().max.drawdown, results[0].analyzers.DD.get_analysis().max.len))
    print("总收益率:%.2f" % (results[0].analyzers.RE.get_analysis()["rtot"]))
    results[0].analyzers.TA.print()
```
结果
```python
夏普比例: 0.7071076051413587
年化收益率: OrderedDict([(2018, 2477996.959), (2019, 1.80777128840242), (2020, 0.15721567033664452)])
最大回撤:15.09，最大回撤周期95
总收益率:15.90
===============================================================================
TradeAnalyzer:
  -----------------------------------------------------------------------------
  - total:
    - total: 5
    - open: 2
    - closed: 3
  -----------------------------------------------------------------------------
  - streak:
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - won:
      - current: 0
      - longest: 2
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - lost:
      - current: 1
      - longest: 1
  -----------------------------------------------------------------------------
  - pnl:
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - gross:
      - total: 8245.700000000004
      - average: 2748.566666666668
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - net:
      - total: 8206.782110000004
      - average: 2735.5940366666678
  -----------------------------------------------------------------------------
  - won:
    - total: 2
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - pnl:
      - total: 8212.406090000004
      - average: 4106.203045000002
      - max: 6878.523510000001
  -----------------------------------------------------------------------------
  - lost:
    - total: 1
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - pnl:
      - total: -5.623979999999938
      - average: -5.623979999999938
      - max: -5.623979999999938
  -----------------------------------------------------------------------------
  - long:
    - total: True
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - pnl:
      - total: 8212.406090000004
      - average: 8212.406090000004
      *************************************************************************
      - won:
        - total: 8212.406090000004
        - average: 4106.203045000002
        - max: 6878.523510000001
      *************************************************************************
      - lost:
        - total: 0.0
        - average: 0.0
        - max: 0.0
    - won: 2
    - lost: 0
  -----------------------------------------------------------------------------
  - short:
    - total: 1
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - pnl:
      - total: -5.623979999999938
      - average: -5.623979999999938
      *************************************************************************
      - won:
        - total: 0.0
        - average: 0.0
        - max: 0.0
      *************************************************************************
      - lost:
        - total: -5.623979999999938
        - average: -5.623979999999938
        - max: -5.623979999999938
    - won: 0
    - lost: 1
  -----------------------------------------------------------------------------
  - len:
    - total: 958
    - average: 319.3333333333333
    - max: 479
    - min: 13
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - won:
      - total: 945
      - average: 472.5
      - max: 479
      - min: 466
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - lost:
      - total: 13
      - average: 13.0
      - max: 13
      - min: 13
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - long:
      - total: 945
      - average: 945.0
      - max: 479
      - min: 466
      *************************************************************************
      - won:
        - total: 945
        - average: 472.5
        - max: 479
        - min: 466
      *************************************************************************
      - lost:
        - total: 0
        - average: 0.0
        - max: 0
        - min: 9223372036854775807
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    - short:
      - total: 13
      - average: 13.0
      - max: 13
      - min: 13
      *************************************************************************
      - won:
        - total: 0
        - average: 0.0
        - max: 0
        - min: 9223372036854775807
      *************************************************************************
      - lost:
        - total: 13
        - average: 13.0
        - max: 13
        - min: 13
```
这就清楚多了。
现在的问题是计算α，β值的方法，貌似框架里没有直接的方法。下次弄吧，另外想根据《重构》这本书对代码进行一下重构。
本文代码： https://github.com/zwdnet/MyQuant/tree/master/46



我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)