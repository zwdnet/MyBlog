---
title: ETF定投数据分析3——金融数据分析
date: 2019-01-21 13:36:43
tags: [ETF,投资理财,定投,Python,数据分析]
categories: 计算机
---

现在我们接着对数据进行分析，主要参考《Python金融实战》一书第8章及后面的章节。
首先是进行时间序列分析，主要涉及pandas和statsmodels两个库，用pydroid3都能装的。
在本地新建一个名为finance的git分支，新建finance.py文件，先读入数据到DataFrame中。
```python
import pandas as pd


if __name__ == "__main__":
    etf_total = pd.read_csv("total_etf.csv")
    etf_300 = pd.read_csv("300etf.csv")
    etf_nas = pd.read_csv("nasetf.csv")
```
用scipy里的统计函数，检验收益率是否为0。
```python
from scipy import stats

print(stats.ttest_1samp(etf_total.收益率, 0.0))
————
Ttest_1sampResult(statistic=-6.5965205827065132, pvalue=3.681639737817202e-10)         [Program finished]
```
可以看到p极小，排除原假设，总收益率不为0。
比较一下我定投的两个指数etf的走势是否有联系？用barlett。
```python
import scipy as sp

#比较两个指数的相关性
    print(sp.stats.bartlett(etf_300.close, etf_nas.close))
————BartlettResult(statistic=38.484328969292861, pvalue=5.5195108020696069e-10)                   [Program finished]
```
以5%的显著性，认为二者相关性很低。
书中还提到了很多策略:如52周策略:价格低于年线即买入，价格高于年线即卖出。后面再模拟下。先看看蒙特卡洛模拟一章。
用scipy生成正态分布。
```python
    #正态分布
    x = sp.random.standard_normal(size = 10)
    print(x[0:5])
    #另一种方式
    x = sp.random.normal(0, 1, 10)
    print(x[0:5])
```
生成随机数
```
    #生成随机数
    sp.random.seed(12345)
    x = sp.random.normal(0, 1, 20)
    print(x[0:5])
```
我用的跟书上一模一样的随机数种子，得到的随机数也跟书上一模一样。因此，计算机产生的随机数是伪随机数，最好用时间做随机数种子。
```
    #画出正态分布图
    sp.random.seed(12345)
    x = sp.random.normal(0.08, 0.2, 1000)
    fig = plt.figure()
    plt.hist(x, 15, normed = True)
    fig.savefig("norm_hist.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0089-etfinverstment/01.png)
再画一个对数正态分布的图
```python
    #对数正态分布
    x = np.linspace(0, 3, 200)
    mu =0
    sigma0 = [0.25, 0.5, 1.0]
    color = ['blue', 'red', 'green']
    target = [(1.2, 1.3), (1.7, 0.4), (0.18, 0.7)]
    start = [(1.8, 1.4), (1.9, 0.6), (0.18, 1.6)]
    fig = plt.figure()
    for i in range(len(sigma0)):
        sigma = sigma0[i]
        y = 1/(x*sigma*np.sqrt(2*np.pi))*np.exp(-(np.log(x)-mu)**2/(2*sigma*sigma))
        plt.annotate('mu = '+str(mu)+', sigma = '+str(sigma), xy = target[i], xytext = start[i], arrowprops = dict(facecolor = color[i], shrink = 0.01))
        plt.plot(x, y, color[i])
    fig.savefig("lognorm.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0089-etfinverstment/02.png)
接下来产生平均分布
```python
    #平均分布
    sp.random.seed(123345)
    x = sp.random.uniform(low = 1, high = 100, size = 10)
    print(x[0:5])
```
用蒙特卡洛算法算圆周率
```python
    #用蒙特卡洛算法求圆周率
    n = 100000
    x = sp.random.uniform(0, 1, n)
    y = sp.random.uniform(0, 1, n)
    dist = np.sqrt(x**2 + y**2)
    in_circle = dist[dist <= 1]
    our_pi = len(in_circle)*4./n
    print('pi = ', our_pi)
    print('error (%)= ', (our_pi - np.pi)/np.pi)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0089-etfinverstment/03.png)
接下来，打算用自己的数据实操一下蒙特卡洛算法。下次吧。

我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)