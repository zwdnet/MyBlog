---
title: 量化投资学习笔记126——股票实盘练习17BackTrader回测均线突破策略
date: 2021-08-02 15:24:19
tags: [量化投资, 实盘, 技术分析]
categories: 量化投资
---
使用backtrader框架进行回测，找了个[教程](https://algotrading101.com/learn/backtrader-for-backtesting/)
是英文的，正好示例用的策略就是均线突破策略。跟着撸了一遍，感觉写得很好，而且不像咱们中文的教程，老是藏着掖着，要么让你加公众号，要么让你加知识星球。强烈推荐。
backertrader数据的使用方法:0为当前数据索引，-1为前一交易日数据索引，以此类推。
在backtrader中，我们收到交易信号可以创建一个order，但只有在next()时才会被执行。
我把BackTrader的回测过程封装了一下，以后基本只用改写策略类就行了。用到再学吧。
先回测一下我实盘的股票莱茵生物。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/96/01.png)

又用另一个库(quantstats)计算了一些回测指标:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/96/02.png)

回测了五年，收益率是负的，不同年份之间差别很大。胜率46.5%。
有个问题是不知道怎么得到交易成本，再完善吧。
最后，把股票池里1800多只股票都回测一下，上市满五年的回测五年，不满五年的回测全程。画图看看胜率以及年化收益率的分布。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/96/03.png)

平均胜率低于50%(47%)，平均年化收益率也接近0%(0.01%)。
看来这个策略也不咋的。看看这次实盘吧。
[回测代码](https://github.com/zwdnet/stockpractice/blob/main/ma/doBacktest.py)
实盘的情况，大盘涨了，我买的莱茵生物却跌了一些，日线上5日均线还在20日均线以上，所以继续持有。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/96/04.jpg)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/96/05.jpg)


账户收益33.53元，3.3%。






**声明:本文为个人学习记录，不构成投资建议!股市有风险，入市需谨慎!**




我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地




![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
