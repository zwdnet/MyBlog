---
title: 量化投资学习笔记128——股票实盘练习19BackTrader计算策略回测指标
date: 2021-08-04 21:30:15
tags: [量化投资, 实盘, 技术分析]
categories: 量化投资
---
主要是α，β等指标，BackTrader没有内置的计算功能，要自己根据回测的收益率数据计算。以前我写过一篇[文章](https://zhuanlan.zhihu.com/p/164533005)
照着做吧。只是数据获取方式由tushare改成akshare了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/98/01.jpg)

所有股票池中的股票回测的α和β值分布结果，大多数还是在0附近。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/98/02.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/98/03.png)


搞定，以后需要什么指标再加吧。接下来再看看怎么增加交易成本的记录。
[回测代码](https://github.com/zwdnet/stockpractice/blob/main/ma/doBacktest.py)
最近在看《日本蜡烛图技术》。关于反转信号，仅当反转信号所指的方向与市场的主要趋势方向一致时，才可以根据这个反转信号来开立新头寸。只有把价格形态与其之前的价格变化相结合，进行通盘考虑，才能准确把握价格形态的意义。看具体的形态的解释，每个形态都有具体的使用条件，不是简单的看图说话。所以，我觉得这种方法并不适合于自己。了解一下吧。其基本思想是多技术方法共同参照的原则。调整自己，适应市场。市场永远不会错，千万不要将自己的主观臆断强加于市场。一定要做一个趋势追随者，而不是趋势预测者。
最后来看实盘，一直就在7.9左右波动，均线没破，继续持有吧。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/98/04.jpg)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/98/05.jpg)




**声明:本文为个人学习记录，不构成投资建议!股市有风险，入市需谨慎!**




我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地




![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)