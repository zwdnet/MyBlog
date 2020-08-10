---
title: ETF定投数据分析4——计算各种回测指标
date: 2019-01-31 15:30:22
tags: [ETF,投资理财,定投,Python,数据分析]
categories: 计算机
---
先计算各种回测和评估策略时要用的指标吧。
参考:
https://zhuanlan.zhihu.com/p/24356155
https://zhuanlan.zhihu.com/p/55425806
https://zhuanlan.zhihu.com/p/29386150
先建立一个新的分支Index，再建立一个新文件index.py，写计算各种指标的程序。
这个过程折腾了我几天，方法是先建立一个testpaper.py的文件，复制上面第二篇文章中的代码，直到调通，得到跟作者一致的结果。然后再把各个指标的计算方法放到各自的函数里，最后再写一个总的调用各个指标计算方法的函数。做成一个index库。调通以后，再用文章中的数据来检验库的计算是否正确(的确发现几个bug)。另外因为我的数据是收益率数据(因为成本在变化，收益率能涵盖成本变化，而市值等数据貌似不行)，计算年化收益率和最大回撤的方法跟作者不一样。
```python
#计算期间年化收益率，用原始数据
def GetAR(data):
    ar = (1+data["数据"].iloc[-1])**(250.0/len(data["数据"]))-1
    return ar
   

#计算最大回撤，因为数据已经是收益率了，直接减就行了。用原始数据。
def GetMD(data):
    md = (data["数据"].cummax() - data["数据"]).max()
    return round(md, 4)
   
   
#计算β和α系数
#因为是指数定投，不存在停盘等数据缺失的问题
def AlphaBeta(data, basedata):
    x = basedata["数据"].values #基准数据
    y = data["数据"].values #要评价的数据
    b,a,r_value,p_value,std_err = stats.linregress(x, y)
    #print(b, a, r_value, p_value, std_err)
    a = round(a*250, 3)
    AB = [a, round(b, 3)]
    return (AB)


#计算夏普比率,saferate为无风险收益，用余额宝收益吧。
def Sharpe(data, saferate):
    exReturn = data["数据"] - saferate/250.0
    sharperatio = np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
    #print(sharperatio)
    return sharperatio
   
   
#计算信息比率
def Information(data, basedata):
    ex_return = data["数据"] - basedata["数据"]
    information = np.sqrt(len(ex_return))*ex_return.mean()/ex_return.std()
    #print(information)
    return information


'''计算各指标的总函数，以后用户就调这个就行了。
data为要计算的策略的数据，basedata为基准数据。
safeIncome为无风险收益率，暂用余额宝的3%吧'''
def index(data, basedata, safeIncome):
    AR = GetAR(data) #计算年化收益率
    MD = GetMD(data) #计算最大回撤
    AB = AlphaBeta(data, basedata) #计算αβ系数
    SR = Sharpe(data, safeIncome) #计算夏普系数
    IR = Information(data, basedata)
    result = [AR, MD, AB[0], AB[1], SR, IR]
    df_result = pd.Series(data = result, index =["年化收益率", "最大回撤", "α系数", "β系数", "夏普系数", "信息比率"])
    return df_result
```
完整代码就不贴了，去看我的github项目主页吧: https://github.com/zwdnet/etfdata
最后用我实际定投数据算出的指标为
```python
年化收益率     -0.114184
最大回撤       0.159400                                     
α系数      -42.816000                                       
β系数        0.044000                                       
夏普系数      -6.646816                                     
信息比率    -186.269012
```
任何夏普比例低于1的策略都不适合单独使用，几乎每月都实现盈利的策略，其年化夏普比率通常都大于2；几乎每天盈利的策略，其夏普比率通常大于3。（《量化交易 如何建立自己的算法交易》 p18）
夏普比率越高，该策略在每单位风险（标准差）上创造出的超额收益就越多。
α表示了一个策略风险调整后的超额收益。与夏普比率不同之处是它使用β来表示风险。
(《量化投资策略：如何实现超额收益》 p22)
可见我的策略实盘并不好，接下来就利用这些函数开始折腾数据啦。
我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)