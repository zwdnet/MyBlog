---
title: 量化投资学习笔记01——初识Pyalgotrade量化交易回测框架
date: 2019-12-11 09:37:13
tags: [量化投资,pyalgotrade,Python,学习笔记]
categories: 量化投资
---
年初学习量化投资，一开始想自己从头写，还是受了C/C++的影响。结果困在了计算回测数据那里，结果老也不对，就暂时放下了。最近试了一下python的各个量化投资框架，发现一个能用的——pyalgotrade，重新开始吧。这是一个事件驱动型量化交易框架。
使用pyalgotrade的一大问题是数据获取，其支持从yahoo，谷歌等途径获得数据，但要获取A股数据比较麻烦。还是用tushare获取数据比较方便。但pyalgotrade并不直接支持tushare数据格式。网上有人介绍了将tushare数据转换成pyalgotrade能接受的数据源的方法，我先按照其方法自己写了一个tsfeed的程序，用于将从tushare获取的数据转化成pyalgotrade可以接受的数据。后来突然发现有个现成的:pyalgotrade_tushare。试用了一下，比我写的好，就用它吧。用pip install pyalgotrade_tushare 安装即可。
现在就开始干活了。先要测试一下pyalgotrade回测数据对不对。我找了个参照标准:在聚宽上开通了个账号，按入门教程写了个策略:2016-2018年每个交易日买入100股平安银行(000001)，回测结果如下:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/01/01.png)
现在用pyalgotrade来实现一下这个策略。先用tushare下载平安银行及沪深300指数的2016年数据。首先建立数据源。 
```python
from pyalgotrade_tushare import tools, barfeed    


instruments = ["000001"]    
feeds = tools.build_feed(instruments, 2016, 2018, "histdata")
```
如果没有下载过数据，会自动下载以后存到histdata目录里，如果下载过，就自动使用目录里的数据了。feeds是BarFeed类型，就是其中的数据驱动pyalgotrade回测框架运行。
接着就从Pyalgotrade.strategy.BacktestingStrategy继承自己的策略类。 
```python
class MyStrategy(strategy.BacktestingStrategy):    
    def __init__(self, feed, instrument, brk):        
        super().__init__(feed, brk)        
        self.__position = None        
        self.__instrument = instrument        
        self.getBroker()        
        self.__cost = 0.0    
        
    def onEnterOk(self, position):        
        execInfo = position.getEntryOrder().getExecutionInfo()        
    
    def onEnterCanceled(self, position):        
        self.__position = None    
        
    def onExitOk(self, position):        
        execInfo = position.getExitOrder().getExecutionInfo()        
        self.info("卖出 %.2f" % (execInfo.getPrice()))        
        self.__position = None    
        
    def onExitCanceled(self, position):        
    # If the exit was canceled, re-submit it.        
        self.__position.exitMarket()            
        
    def onBars(self, bars):        
        brk = self.getBroker()        
        shares = 100        
        price = bars[self.__instrument].getPrice()        
        if brk.getCash() < price*shares:             
            self.info("现金不足")             
            return        
        self.__position = self.enterLong(self.__instrument, shares, True)        
        self.__cost += brk.getCommission().calculate(brk, price, shares)                                self.info("可用现金%.2f 股价%.2f 持股数量%d 市值1:%.2f 市值2:%.2f 计算市值:%.2f 交易成本%.2f" % (brk.getCash(), price, brk.getShares(self.__instrument), brk.getEquity(), self.getResult(), (brk.getCash() + brk.getShares(self.__instrument)*price), self.__cost))              # x = input(&quot;按任意键继续&quot;)

```
其中onBar是必须重写的，即每次数据更新要执行的操作。然后设置手续费，滑点等设置。
```python
# 设置手续费    
broker_commision = broker.backtesting.TradePercentage(0.0003)    
brk = broker.backtesting.Broker(cash, feeds, broker_commision)
```
Broker对象是进行交易的类。然后生成策略对象: 
```python    
myStrategy = MyStrategy(feeds,     instruments[0], brk)
```
接下来生成用于计算回测指标的四个对象，并将其添加进入策略中: `
```python    
retAnalyzer = returns.Returns()    
myStrategy.attachAnalyzer(retAnalyzer)    
sharpeAnalyzer = sharpe.SharpeRatio()    
myStrategy.attachAnalyzer(sharpeAnalyzer)    
drawDownAnalyzer = drawdown.DrawDown()   
myStrategy.attachAnalyzer(drawDownAnalyzer)     
tradesAnalyzer = trades.Trades()     
myStrategy.attachAnalyzer(tradesAnalyzer)
```

如果要作图，类似的，也要将绘图对象添加进入策略对象。
```python
from pyalgotrade import plotter     


plter = plotter.StrategyPlotter(myStrategy)    plter.getOrCreateSubplot("return").addDataSeries("retuens", retAnalyzer.getReturns())    plter.getOrCreateSubplot("CumReturn").addDataSeries("CumReturn",retAnalyzer.getCumulativeReturns())
```
准备工作做完，就可以执行回测了，用myStrategy.run()执行以后就可以输出回测结果，输出图形了。

限于篇幅，就不放代码了。

详细代码见:

https://github.com/zwdnet/MyQuant/blob/master/01/testdata.py

现在来看看回测结果。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/01/02.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/01/03.png)
其中年化收益率那里应该是三年的策略收益，这样看两个的回测结果是基本一致的，但并不完全一致。原因呢？我看了一下每个交易日的情况：聚宽上面的：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/01/04.png)
我本地文件里的数据
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/01/05.png)
在本地输出每个交易日的情况：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/01/06.png)
可以看到2016-01-05，聚宽的股价数据是8.99，tushare下载的数据是9.07。2016-01-06，聚宽的数据是9.10，tushare是9.179。我在聚宽的论坛里发帖问了，被告知可能是数据复权方法，滑点设置等差异引起的。另外，pyalgotrade貌似是第一天产生交易信号第二天再执行交易。好在差别也不大，就这样吧。还有一些问题，比如pyalgotrade里貌似没有没有直接计算alpha值，beta值，信息比率等数据的函数，用到了再说吧。
最后再总结一下用pyalgotrade进行量化交易回测的一般步骤:
①用数据生成BarFeed对象，作为驱动框架的数据来源。
②用Broker对象设置交易成本，滑点等。
③从strategy.BacktestingStrategy建立Strategy对象，并重写onBars成员函数，其内容为每次交易事件时都要执行的动作。其中可能会用到technical对象，用于计算一些技术指标。
④实例化strategy对象，建立回测指标对象和绘图对象，并将它们与strategy绑定。
⑤执行回测。
⑥输出回测结果，绘图。
下一步，该真正进行量化交易策略的学习研究了。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的CSDN博客地址：https://blog.csdn.net/zwdnet
我的微信个人订阅号：赵瑜敏的口腔医学学习园地
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)