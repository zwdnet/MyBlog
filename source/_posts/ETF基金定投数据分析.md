---
title: ETF基金定投数据分析
date: 2019-01-12 17:25:28
tags: [ETF,投资理财,定投,Python,数据分析]
categories: 计算机
---
作为一个80后的小伙，我错过了一次又一次让自己财富增加的机会，唯一的投资理财就是把钱通通放到某额宝里。一年前，我开始学习理财的知识，最后选择进行etf基金定投来投资。找了一家券商开了户。投资的品种就两个:300ETF和纳指ETF，分别追踪沪深300指数和纳斯达克指数。选择这两个指数之前我用python跑了一下历史数据，二者的相关性很低，也许可以做风险对冲？
开始是每个月一次，后来逐渐增加到每个月三次，隔十天左右进行一次。单纯买入，没有止盈止损。我计划是先这么投一年，再看结果来调整。截止2019年1月9日，账户收益情况如下:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/01.jpg)亏的。前几天美股暴跌，亏得更多。近一年定投的感受就是，这种投资方式真的很考验人性，好几次我都想卖了，忍住了。
现在，我们就用Python来分析一下近一年来的投资数据吧。开发环境:由于条件限制，我是在安卓手机上用Pydroid3做编程环境的，Python版本3.6.2。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/02.jpg)  
常用的一些库都能安装，看自带的例子，似乎还能写安卓APP，我还没试过。与在电脑上编程相比，有两个限制:首先画图不能直接显示，要用savefig保存图片到文件;其次，深度学习的一些库，如Tensorflow等，装不了，可能是因为与硬件相关吧。但机器学习的库，如scikit-learn等，可以安装的。另外还安装了Termux等，用于进行git操作。
开发环境搞定了，接下来就是获取数据的问题了。我从券商的APP上把数据一个一个搬到Excel表格里，像这样:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/03.jpg)
本来想就这么读了，发现还可以另存为csv文件。那更好。于是数据就有了。开工吧。先导入相关的库，然后用read_csv读入数据:
```python
import pandas as pd
from pandas import Series, DataFrame


#从csv文件读入数据
def ImportData(FileName):
    df = pd.read_csv(FileName)
    return df
   
   
#主程序
if __name__ == "__main__":
    etfdata = ImportData("etfdata.csv")
    print(etfdata)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/04.jpg)
OK，没问题。
接下来就开始折腾数据吧。DataFrame是一种表格式的，含有多列的数据结构。每列的数据类型可以不一样。每行/每列数据都有一个索引。用DataFrame.columns()得到每列的索引。
```python
#探索数据
def ExploreData(Data):
    #每列的索引名称
    print(Data.columns)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/05.jpg)
用每列索引名称可以提取相应列的数据
```python
print(Data["成交金额"])
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/06.jpg)
还可以用"变量名.列名"的方式，结果是一样的。
```python
print(Data.成交金额)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/07.jpg)
还可以用相同的方式输出指定行的信息:
```python  
print(Data.ix[1])
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/08.jpg)
用values属性可以返回DataFrame的值。
```python
#返回Data的值   
print(Data.values)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/09.jpg)
现在，可以把原始数据按买入的etf分成两个了:
```
#分离数据:根据买入的etf的不同划分数据
def DivData(Data):
    df_300 = Data[Data["证券名称"] == "300ETF"]
    df_nas = Data[Data["证券名称"] == "纳指ETF"]
    return (df_300, df_nas)
    用describe描述数据特征
#描述数据
    print(df_300.describe())
    print(df_nas.describe())
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/10.jpg)    
按成交均价，画个图看看吧。
```python
import matplotlib.pyplot as plt


plt.plot(df_300["成交均价"])
    plt.plot(df_nas["成交均价"])
    plt.savefig("成交均价.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/11.jpg)
OK，接下来要计算收益率等信息了，需要知道历史股价信息，用tushare库。这是国产的库，用来获取各种金融数据。官方版本已经到1.2.15了，我在pydroid3里装的是0.6.8，升级出现pyzmq错误，搜了半天没找到解决方法，就暂时用旧的那个好了。
用get_k_data函数，因为其日期数据是yyyy-mm-dd格式的，先转换一下。
```python
#将八位数字的日期转换为yyyy-mm-dd
def TransfDate(d):
    year = int(d/10000)
    month = int((d - year*10000)/100)
    day = int((d - year*10000 - month*100))
    date = format("%4d-%02d-%02d" % (year, month, day))
    return date
```
转换函数留着备用。
先找出最早开始定投的时间:
```python
beginTime = df_300.成交日期.min()
endTime = df_300.成交日期.max()
```
然后就用tushare抓取历史数据
```python
#抓取历史数据
def GetHistoryData(Code, BeginTime, EndTime):
    df = ts.get_k_data(Code, index = False,  start = TransfDate(BeginTime), end = TransfDate(EndTime))
    return df
```
输出一下看看
```python
df_300_hist = GetHistoryData("510300", beginTime, endTime)
    df_nas_hist = GetHistoryData("513100", beginTime, endTime)
    print(df_300_hist)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/12.jpg)
没问题啦。现在就可以用历史数据计算定投的持仓收益情况了。这个要考虑一下计算方法：就从开始定投的交易日开始，每个交易日计算一次。根据每次交易的成交量和手续费，计算一个总投入。再根据买入股票的量，计算一个持仓量，根据持仓量就可以算出当前股票的市值。再减去总投入，就是总收益了。用收盘价计算吧。 
先筛选下载的历史数据，只保留日期和收盘价。
```python   
df_300_hist = df_300_hist.loc[0:len(df_300_hist), ["date", "close"]]
    df_nas_hist = df_nas_hist.loc[0:len(df_nas_hist), ["date", "close"]]
```
接下来就计算数据啦。出现很多问题，折腾半天，发现是原始数据中有同一天对同一只基金多次买入的问题。搞不定，最后用手工合并啦。   
计算数据费了很多功夫，主要是因为不是每个交易日都有交易，而每个交易日股价都在变动，市值和收益率也在变动，因此交易记录和股价记录长度不一致，要换算。这是最长的一个函数了，一定还有更简洁的方法。我之前学的C/C++，c语言的"味道"很浓。
```python
#根据投资记录和历史数据计算持仓收益率等数据。
def Calculator(inverstData, histData):
    i = 0
    j = 0
    vol = []    #持仓股票数量
    fee = []    #手续费
    money = []   #投资总额
    rate = []     #收益率
    time = []   #时间
    market = []  #股票市值

    for date in histData.date:
        d1 = TransfDate2(date)
        d2 = inverstData.成交日期[i]
        b = (d1 == d2)
        time.append(d1)
        #该日期有交易，改变数据
        if b == True:
            if i == 0: #第一天，直接插
                vol.append(inverstData.成交量[i])
                fee.append(inverstData.手续费[i])
                money.append(inverstData.发生金额[i])
                market.append(vol[i]*histData.close[i])
                #计算收益率=市值/投资总额
                rate.append(market[i]/money[i] - 1.0)
            else: #不是第一天，但有交易
                 vol.append(vol[j-1] + inverstData.成交量[i])
                 fee.append(fee[j-1] + inverstData.手续费[i])
                 money.append(money[j-1] + inverstData.发生金额[i])
                 market.append(vol[j]*histData.close[j])
                 #计算收益率=市值/投资总额
                 rate.append(market[j]/money[j] -1.0)
            i = i+1
        else: #没有交易，复制上一天的数据
            vol.append(vol[j-1])
            fee.append(fee[j-1])
            money.append(money[j-1])
            market.append(vol[j]*histData.close[j])
            rate.append(market[j]/money[j] - 1.0)
        j = j+1
    data = pd.DataFrame({
    "日期":time,
    "持仓量":vol,
    "手续费":fee,
    "成本":money,
    "市值":market,
    "收益率":rate})
    return data
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/13.jpg)
搞定！再把收益率趋势图画出来。
```python
    plt.figure()
    plt.plot(data_300.收益率, label = "300etf")
    plt.plot(data_nas.收益率, label = "纳指etf")
    plt.legend(loc = "upper right")
    plt.savefig("收益率.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/14.jpg)
美股跟a股相关性果然很低。接下来就是具体折腾数据啦。先把两个股票的数据合并一下，算出一个总持仓的收益数据。
```python
#合并两个数据，算出总的持仓收益率等数据
def MergeData(data1, data2, histData1, histData2):
    #合并日期，持仓金额，手续费,市值，并计算持仓收益率
    money = [] #成本
    fee = [] #手续费总额
    market = [] #总的股票市值
    rate = [] #总的收益率
    time = [] #日期
    i = 0
    for date in histData1.date:
        date = TransfDate2(date)
        time.append(date)
        money.append(data1.成本[i] + data2.成本[i])
        fee.append(data1.手续费[i] + data2.手续费[i])
        market.append(data1.市值[i] + data2.市值[i])
        #计算收益率
        rate.append(market[i]/money[i] - 1.0)
        i = i + 1
    data = pd.DataFrame({
    "日期":time,
    "成本":money,
    "手续费":fee,
    "市值":market,
    "收益率":rate
    })
    return data
```
再把总的收益率也画到一个图里看看。
```python
#将收益率数据合并，算出总的持仓数据
    data_total = MergeData(data_300, data_nas, df_300_hist, df_nas_hist)
    plt.figure()
    plt.plot(data_300.收益率, label = "300etf")
    plt.plot(data_nas.收益率, label = "nasetf")
    plt.plot(data_total.收益率, label = "etf")
    plt.legend(loc = "upper right")
    plt.savefig("收益率.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0085-etfinverstment/15.jpg)
可以看到同时定投两个市场的指数的确可以平衡风险。数据的收集处理就到这里了。接下来就是数据分析啦，作为一篇公众号文章，已经太长了，就下回分解吧。         
几点说明：       
1.我本职是一名牙医，编程是我的爱好，以前用得最多的是C/C++（不过也只是写一些几千行的小程序），python用的时间不长，所以代码里好多C的味道。       
2.写本文是因为crossin编程教室公众号搞了个征稿活动，正好我也打算用python分析一下自己近一年的etf定投数据，就想着把分析过程记录下来，不是说分享就是最好的学习吗？        
3.我学习的体会，这种带着问题在做中学，是要比那种一本书或者一个课程从头看到尾要好一些，在这个过程中会碰到各种各样想不到的问题，就想办法解决或者去搜。写程序也是这样，开始只是一个想法：我要分析自己的ETF定投数据，接着就慢慢拆问题：怎么收集数据，需要哪些数据，数据如何处理得到自己想要的数据，如何分析......每个问题又可以拆成更多的问题，直到问题小到可以直接解决。这是计算机的思维方法，也可以用到其它领域，比如我自己的专业领域。         
4.本文的主要参考资料：《Python for Data Analysis》，Pandas库作者写的，对，是英文版的。再多说一句，能读原文的最好读原文，其实没那么难的。我读原文书的想法是来自于我自己的专业：口腔医学。以前除了教科书，其它专业书我是基本不看的，看不下去（最主要还是没兴趣）。后来想把自己专业搞好了，开始看书，发现很多书翻译过来要么是比较老的版本了，要么根本就没有翻译的，最重要的是专业书都是厚本厚本的，死贵了。后来发现一个搜英文书的网站：b-ok，很多专业书都能找到英文电子版，还往往是最新的。于是下了很多口腔专业的电子书，上班就在诊室电脑上看，看着看着我发现，看原文也没那么难。这个过程不太长的，就两三个月。从此我又有了一个习惯：看到翻译过来的新书，想看，用英文书名去搜，往往能找到电子版。         
5.本文的代码已经上传到github里：https://github.com/zwdnet/etfdata 后期如果写新的内容，可能会开新的分支。         
6.我自己开了个博客：https://zwdnet.github.io 还有一个微信订阅号：赵瑜敏的口腔医学学习园地，二维码在最后。主要都是口腔医学的东西，而且不是科普，是给牙医同行看的。所以不是同行的话可以不用看了。谢谢！         
**最后声明：本文只是探讨python数据处理技术，不构成投资建议。投资有风险，入市需谨慎。**
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)

