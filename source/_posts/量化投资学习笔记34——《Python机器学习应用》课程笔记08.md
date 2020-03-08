---
title: 量化投资学习笔记34——《Python机器学习应用》课程笔记08
date: 2020-03-08 13:30:35
tags: [量化投资,Python,机器学习,回归分析,岭回归]
categories: 量化投资
---
岭回归
解决某些训练样本线性相关，导致回归结果不稳定的情况。
它是一种用于共线性数据分析的有偏估计回归方法。是一种改良的最小二乘估计法。
在sklearn中使用sklearn.linear_model.Ridge进行。
课程的实例是交通流量预测，我找不到数据文件，从网上自己找个例子吧。
用波士顿房价预测做例子。
先加载数据并放到dataframe里。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/26/01.png)
用seaborn的pairplot画图看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/26/02.png)
真不错，又会一招。可以看到(最后一行或最后一列)有的属性与房价有明显的关系，而有的没有明显关系。
还是用所有属性建模。
lr的均方误差为： 33.00649127511586
Rd的均方误差为： 33.008436871102866
比较线性回归和岭回归，貌似结果差不多，想画图看看，老也不对，算啦。。
本文代码: 
https://github.com/zwdnet/MyQuant/blob/master/34



我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)