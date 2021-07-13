---
title: 量化投资学习笔记111——股票实盘练习2TA-Lib识别k线形态
date: 2021-07-12 15:28:51
tags: [量化投资, 实盘, 技术分析]
categories: 量化投资
---
首先下载股票数据，下载前一个月的日线数据，然后用mplfinance画K线，参考[这里](https://blog.csdn.net/weixin_42357256/article/details/112711191)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/81/01.png)

接下来，就是用TA-Lib来自动判断K线形态了。我的云服务器上装的系统是ubuntu，经过搜索，要用源码安装。安装好以后，发现它的官方文档里居然没有函数的详细解释!找了个[非官方的](https://zhuanlan.zhihu.com/p/24883961)
判断锤子形态用的是talib.CDLHAMMER(open, high, low, close)函数，其中的参数均是numpy数组，返回一个数组，不是锤子形态的返回0，是锤子形态的返回非零数值(我这是10)。我运行的结果是第15个k线是锤子图形，蛮准的。接下来，再改进一下程序，给出股票代码，自动找出含有锤子形态的股票并给出其位置。找出的股票按出现锤子形态的日期倒序排列，即最近的股票出现在最前面。
```python
# 检测k线有无锤头形态
@run.change_dir
def testCuizi(codes):
    print("检测锤子形态")
    results = {}
    for code in codes:
        date = []
        filename = "./data/" + code + ".csv"
        if os.path.exists(filename):
            data = pd.read_csv(filename)
            result = talib.CDLHAMMER(data.开盘.values, data.最高.values, data.最低.values, data.收盘.values)
            pos = ()
            pos = list(np.nonzero(result))
            if len(pos[0]) != 0:
                date.append(data.日期[pos[0][-1]])
                results[code] = date
    # 按日期降序排序，最近的日期排最前
    results = sorted(results.items(),key = lambda x:x[1],reverse = True)
    print(results)

```

结果
检测锤子形态                                               [('002195', ['2021-07-09']), ('600256', ['2021-07-09']), ('600582', ['2021-07-09']), ('601866', ['2021-07-09']), ('601608', ['2021-07-07']), ('002132', ['2021-07-06']), ('002269', ['2021-07-05']), ('600166', ['2021-07-05']), ('300266', ['2021-07-02']), ('002131', ['2021-07-02']), ('300217', ['2021-07-02']), ('601005', ['2021-07-02']), ('000592', ['2021-06-30']), ('600277', ['2021-06-30']), ('300159', ['2021-06-30']), ('601398', ['2021-06-30'])]
从头开始，到股票APP里看k线，600256比较靠谱。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/81/02.jpg)

买入1手。成本3.5，止损价3.15。
接下来就看实盘结果了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/81/03.jpg)

目前为止两个交易日亏损1%，都是开盘不久买入然后就跌。看来以后不必开盘就急着买。
代码: https://github.com/zwdnet/stockpractice/blob/main/kline/kline.py
**声明:本文为个人学习记录，不构成投资建议!股市有风险，入市需谨慎!**






我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地








![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
