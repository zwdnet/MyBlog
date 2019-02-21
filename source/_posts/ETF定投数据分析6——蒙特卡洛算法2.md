---
title: ETF定投数据分析6——蒙特卡洛算法2
date: 2019-02-21 13:55:03
tags: [ETF,投资理财,定投,Python,蒙特卡洛算法]
categories: 计算机
---
春节过完了，我们继续量化投资学习之旅。先获取更多的数据，我定投的两个etf基金分别建立于2012年和2013年，我们以最晚的纳指etf的创立时间2013年5月1日为起始点，收集股价数据。
先收集数据，用之前用过的函数。只用运行一次。
``` python
#获取从2013年5月15日至2019年2月1日的数据
    beginTime = 20130515
    endTime = 20190201
    etf300 = etfdata.GetHistoryData("510300", beginTime, endTime)
    etfnas = etfdata.GetHistoryData("513100", beginTime, endTime)
    print(len(etf300), len(etfnas))
    #保存文件
    etf300.to_csv("df_300_hist.csv")
    etfnas.to_csv("df_nas_hist.csv")
#读取数据
    df_300 = pd.read_csv("df_300_hist.csv")
    df_nas = pd.read_csv("df_nas_hist.csv")
    #只保留收盘价
    length1 = len(df_300)
    length2 = len(df_nas)
    df_300 = df_300.loc[0:length1, ["date", "close"]]
    df_nas = df_nas.loc[0:length2, ["date", "close"]]
    print(len(df_300), len(df_nas))
```
输出结果:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/01.png)
搞定。
然后用实盘的策略模拟一次试试(代码见 https://github.com/zwdnet/etfdata)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/02.png)
共交易139次，貌似结果也不太好。
再自己看代码，work函数有bug，折腾半天，重写吧。分成几个函数，画个流程图。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/03.png)
将一个长的函数拆分成几个函数，终于算的像是对的了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/04.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/05.png)
坚持定投近六年，收益大概是30%左右，年化收益率4.7%，比余额宝高不了多少，但是最大收益曾达到60%左右，如果增加止盈和止损策略，会不会更好一些？
下面就来模拟一下增加了止盈止损策略后的效果。
改一下模拟交易函数，增加止盈操作，策略用最简单的:止盈点10%，即收益率上升到最高点以后下跌10%，卖出一半。再跌10%再卖一半，到底部反弹超过10%，全部买回。结果老是调不对，调了几个晚上，终于看起来像是对了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/06.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/07.png)
看图形和数据，都比不止盈好一点，但是计算的那些数据还是有问题。再改改看。另外，两个etf的相关系数很低，也就是说一个etf在跌时另一个可能还在涨，分开进行止盈操作会不会更好？
折腾了好几天，终于调通了，结果貌似还可以，但还不如总的一起止盈的？
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/08.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/09.png)
单独画出两个个股的收益率曲线看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/10.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0100-mtkletf2/11.png)
都有那种收益率一下子上升数倍又回落的情况。应该是终止止盈的策略那里的问题，我的策略是触发终止止盈后，将止盈得到的钱一次性又买回相应的个股。分期投入会不会更好？
写到这里，我跟交易模拟函数挣扎了好几天，结果总是不正确，而且函数也写得越来越复杂，越来越难改。另外算出来的回测数据貌似也有问题。于是我试了一下在某在线平台上写策略，然后回测，看算出来的数据是否跟我一致，但是有很多限制，没有完成。我也试了一些开源的量化交易框架，如vn.py, backtrader等，有的手机装不上，有的看了下用着好复杂。现在我决定重构交易模拟和回测的部分，弄好了再继续了。
我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“好看”。谢谢。
我的个人博客地址：https://zwdnet.github.io
我的CSDN博客地址：https://blog.csdn.net/zwdnet
我的微信个人订阅号：赵瑜敏的口腔医学学习园地
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)