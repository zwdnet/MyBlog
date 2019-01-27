---
title: ETF定投数据分析3——金融数据分析
date: 2019-01-21 13:36:43
tags: [ETF,投资理财,定投,Python,数据分析]
categories: 计算机
---

 上一篇文章用Python对定投数据进行了处理，计算出了总的收益率随时间的变化数据，保存到了csv文件里。现在我们就开始对数据进行具体的分析。具体如何分析，我也没谱，是第一次，走到哪儿就算哪儿吧。首先，先建立一个git分支，在分支上编辑新代码，完成以后再合并。git分支功能我以前也没怎么用过，只是知道有这么个功能。搜了一下，又动手实验，成功了。先建立名为data_analysis的分支，然后转移到该分支中:
```
git branch data_analysisgit checkout data_analysis
```
或者可以直接新建分支并转移
```
git checkout -b data_analysis
```
然后就可以增加代码啦。新建一个data_analysis.py的文件，用于数据分析。先从csv文件中导入数据到DataFrame变量中，再输出看看。
```python
import pandas as pd    
etf_total = pd.read_csv("total_etf.csv")    
etf_300 = pd.read_csv("300etf.csv")    
etf_nas = pd.read_csv("nasetf.csv")    
print(etf_total.head())    
print(etf_300.head())    
print(etf_nas.head())
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/01.png)

没问题啦。再提交代码。最后将本地分支推送到github上。
```
git push -u origin data_analysis
```
再把数据可视化一下吧，先尝试一下各种不同的图形类型。
```python
import matplotlib.pyplot as plt


#数据可视化
def Display(data):    
    fig = plt.figure()    
    ax1 = fig.add_subplot(2,2,1)    
    ax2 = fig.add_subplot(2,2,2)    
    ax3 = fig.add_subplot(2,2,3)    
    ax4 = fig.add_subplot(2,2,4)    
    #用各种不同的形式画图    
    ax1.plot(data.收益率)    
    ax2.hist(data.收益率, bins =10, alpha = 0.8, facecolor = 'b', normed = 1)    
    ax3.scatter(range(len(data)), data.收益率, marker ='.')    
    ax4.plot(data.收益率, 'k--')        
    fig.savefig("可视化数据.png")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/02.png)

还可以用另一种方法建立子图绘图
```python
#另一种方法    
fig,ax = plt.subplots(2,2)    
ax[0, 0].plot(data.收益率)    
ax[0, 1].plot(data.收益率, 'k--')    
ax[1, 0].plot(data.收益率, 'k-', drawstyle='steps-post')    
ax[1, 1].plot(data.收益率, linestyle='dashed', marker='o')    fig.savefig("可视化数据2.png")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/03.png)
给图形增加图例
```python
#绘图并增加图例    
fig,ax = plt.subplots(1,1)    
ax.plot(data.收益率, label ="收益率")    
fc = data.手续费/data.成本    
ax.plot(fc, label="手续费占比")    plt.legend(loc="best")    
fig.savefig("可视化数据3.png")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/04.png)
中文是乱码，搜了一圈，要显示中文好麻烦，貌似还要root手机，还是放弃了，就用英文吧。
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/05.png)
matplotlib是一个低阶的工具，要考虑作图的很多细节。pandas还有很多高阶的绘图工具。
```python   
#用pandas画图    
fig = plt.figure()    
data.收益率.plot(kind = 'bar')    
fig.savefig("pandas作图.png")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/06.png)
横坐标有问题
```python
fig = plt.figure()    
data.收益率.hist(bins =20, normed = True)    
fig.savefig("pandas作图2.png")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/07.png)
可视化显示就到这里吧，下面再试试用时间序列分析。pandas提供了很多时间序列分析工具。移动窗口分析，一看就是均线嘛。想当初我分析定投的时候还自己从数据里算均线，结果人家有现成的！画月线和双月线。书上的方法是用rolling_mean，结果提示该函数会被废弃，于是照其提示用最新的。
```python
#移动时间窗口分析
def MovementWindows(data):    
    mean_30 = data.收益率.rolling(window=30, center = False).mean()          mean_60 = data.收益率.rolling(window=60, center = False).mean()          fig = plt.figure()    
    data.收益率.plot()    
    mean_30.plot()    
    mean_60.plot()    
    fig.savefig("均线图")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/08.png)
同理可以算出标准差的移动窗口
```python
std_30 = data.收益率.rolling(window=30, center = False).std()    
std_60 = data.收益率.rolling(window=60, center = False).std()    
fig = plt.figure()    
std_30.plot(label="30std")    std_60.plot(label="60std")    plt.legend(loc="best")    
fig.savefig("标准差图.png")
```
![](
https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0087-etfinverstment/09.png)
这次先到这里吧，还是参考的《Python for data analysis》。我发文章的两个地方，欢迎大家在朋友圈等地方分享，欢迎点“好看”。谢谢。我的个人博客地址：https://zwdnet.github.io我的微信个人订阅号：赵瑜敏的口腔医学学习园地
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
