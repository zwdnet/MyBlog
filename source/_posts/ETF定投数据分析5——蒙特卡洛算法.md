---
title: ETF定投数据分析5——蒙特卡洛算法
date: 2019-02-03 09:27:58
tags: [ETF,投资理财,定投,Python,蒙特卡洛算法]
categories: 计算机
---
接下来就用蒙特卡洛算法分析一下数据吧。老规矩，先新建一个名为MonteCarlo的分支，新建一个名为MonteCarlo.py的文件。先看一下我的数据，平均每7个交易日交易一次，手续费率0.0003(万分之三,不足0.1元收0.1元)。购买300etf和纳指etf两个股票，金额平分。即交易28次，每次交易金额1000元，剩下的，并到下次交易。以上就是模拟的假设。
接下来就是进行交易模拟的函数，比较长，主要是一些细节的计算。
```python
'''执行一次交易模拟
输入的参数
cost 总交易成本
time 交易周期的天数
freq 交易频率，几天交易一次
df_300, df_nas,分别为两个定投的etf的实盘成交数据
返回值为一个DataFrame，包含每个交易日的成本，收益，收益率等数据
'''
def work(cost, time, freq, df_300, df_nad):
    #计算交易次数
    tradetimes = int(time/freq)
    print(tradetimes)
    #计算每次交易的金额
    money = cost/tradetimes
    print(money)
    #手续费比率
    fee_rate = 0.0003
    #把每次交易金额均分为两部分，分别买两个etf，如果钱不够交易，留到下次
    money_300 = money/2.0
    money_nas = money/2.0
    #开始模拟前定义相关变量
    cost = [] #投入的总成本
    cost3 = [] #买300etf的成本
    costN = [] #买纳指etf的成本
    m3 = 0.0 #买300etf的钱
    mN = 0.0 #买纳指etf的钱
    fee = [] #手续费
    V3 = [] #300etf股票数量
    VN = [] #纳指etf股票数量
    Total3 = [] #300etf的当前市值
    TotalN = [] #纳指etf的当前市值
    Total = [] #当前总市值
    Income3 = [] #300etf的收益
    IncomeN = [] #nasetf的收益
    Income = [] #总收益
    Rate3 = [] #300etf收益率
    RateN = [] #nasetf收益率
    Rate = [] #总收益率
    #每次交易剩下的钱
    money_300_rem = 0.0
    money_nas_rem = 0.0
   
    #开始模拟
    j = 0
    for i in range(time):
        if j == 0:   #交易
            #计算可以买的股票数量
            num_300 = int(money_300/df_300["close"][i]/100)*100
            num_nas = int(money_nas/df_nas["close"][i]/100)*100
            if i == 0:
                V3.append(num_300)
                VN.append(num_nas)
            else:
                V3.append(V3[i-1] + num_300)
                VN.append(VN[i-1]+ num_nas)
            #计算购入成本
            m3 = num_300*df_300["close"][i]
            fee_300 = m3*fee_rate
            if fee_300 < 0.1:
                fee_300 = 0.1
            money_300_rem = money_300 - m3 - fee_300
            money_300 += money_300_rem
            mN = num_nas*df_nas["close"][i]
            fee_nas = mN*fee_rate
            if fee_nas < 0.1:
                fee_nas = 0.1
            fee.append(fee_300 + fee_nas)
            money_nas_rem = money_nas - mN - fee_nas
            money_nas += money_nas_rem
           
            #计算总成本
            total_cost = m3+fee_300+mN+fee_nas
            if i == 0:
                cost3.append(m3+fee_300)
                costN.append(mN+fee_nas)
                cost.append(cost3[i] + costN[i])
            else:
                cost3.append(cost3[i-1] + m3 + fee_300)
                costN.append(costN[i-1] + mN + fee_nas)
                cost.append(cost[i-1] + cost3[i] + costN[i])
            #其它数据无论是否交易都要算，放最后
        else:    #不交易
            fee.append(0.0)
            cost.append(cost[i-1])
            cost3.append(cost3[i-1])
            costN.append(costN[i-1])
            V3.append(V3[i-1])
            VN.append(VN[i-1])
        #无论是否交易都要算的持仓市值，收益，收益率
        j += 1
        if j >= freq:
            j = 0
        Total3.append(V3[i]*df_300["close"][i])
        TotalN.append(VN[i]*df_nas["close"][i])
        Total.append(Total3[i] + TotalN[i])
        Income3.append(Total3[i] - cost3[i])
        IncomeN.append(TotalN[i] - costN[i])  
        Income.append(Income3[i] + IncomeN[i])
        Rate3.append(Income3[i]/cost3[i])
        RateN.append(IncomeN[i]/costN[i])
        Rate.append(Income[i]/cost[i])
       
    data = pd.DataFrame(
    {
    "成本":cost,
    "手续费":fee,
    "市值":Total,
    "收益":Income,
    "收益率":Rate
    }
    )
    return data
```
测试一下。
```python
#进行模拟
    #先获取成本，交易周期等信息
    cost = df_etf["成本"].values[-1]
    print(cost)
    time = len(df_etf)
    #进行交易模拟
    data = work(cost, time, 10, df_300, df_nas)
    print(data.head())
    testdata = pd.DataFrame(
    {
    "数据":data["收益率"].values
    }
    )
    result = index.index(testdata, df_base, 0.03)
    print(result)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0096-mtkletf/01.png)
OK，测试成功。以后还可以进一步完善，比如设定止盈止损规则等。先从最简单的来吧，改变交易频率看看，即从每日进行交易到每30个交易日进行一次交易，看看数据有何不同。
建一个函数进行模拟
```python
#按不同交易频率进行交易
def Run(cost, time, df_300, df_nas):
    data = []
    for freq in range(1, 31):
        data.append(work(cost, time, freq, df_300, df_nas))
    return data
```
然后调用
```python
#测试成功，现在模拟不同交易频率对结果的影响
    testresult = Run(cost, time, df_300, df_nas)
    testindex = [] #保存测试结果的回测指标
    for res in testresult:
        print(res.head())
        test = pd.DataFrame(
        {
        "数据":res["收益率"].values
        }
        )
        testindex.append(index.index(test, df_base, 0.03))
    for test in testindex:
        print(test.head())
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0096-mtkletf/02.png)
再画图看一下，先比较一下年化收益率。
```python
    AR =[]
    for test in testindex:
        print(test.head())
        AR.append(test["年化收益率"])
        #数据可视化
        fig = plt.figure()
        plt.plot(AR)
        fig.savefig("montecarlo_ar.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0096-mtkletf/03.png)
随着交易频率的下降，年化收益率也下降？再看看最大回撤
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0096-mtkletf/04.png)
随着交易频率的下降，最大回撤值上升。
阿尔法值
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0096-mtkletf/05.png)
夏普系数
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0096-mtkletf/06.png)
从中可以总结出各种规律，貌似交易频率越高越好？但第一收益率全是负的而不是正的，第二交易天数仅200余天，好像有点少。不过这算是基本的模拟方法，更进一步的探索，留待下次吧。
明天就是春节了，提前祝大家猪年吉祥！明年见！
我发文章的三个地方（对，多了一个，计算机方面的文章可能会发CSDN的博客上。所有的文章都会发在github个人博客上），欢迎大家在朋友圈等地方分享，欢迎点“好看”。谢谢。
我的个人博客地址：https://zwdnet.github.io
我的CSDN博客地址：https://blog.csdn.net/zwdnet
我的微信个人订阅号：赵瑜敏的口腔医学学习园地

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)

