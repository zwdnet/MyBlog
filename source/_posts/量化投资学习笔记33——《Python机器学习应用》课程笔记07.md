---
title: 量化投资学习笔记33——《Python机器学习应用》课程笔记07
date: 2020-03-08 13:27:15
tags: [量化投资,Python,机器学习,回归分析,多项式回归]
categories: 量化投资
---
多项式回归
研究一个或多个自变量与一个因变量间多项式的回归分析方法。如果一个自变量，为一元多项式回归。自变量为多个时，为多元多项式回归。多项式回归使用曲线拟合数据的输入与输出的映射关系。
实例，还是预测房价。
用sklearn.preprocessing.PolynomialFeatures函数。
数据跟上一篇的一样。
PolynomialFeatures这个函数的作用，是生成变量的各种组合形式，如a,b两个自变量，最高二次，可以生成1，a,b, ab, a^2, b^2。
再用这个多项式进行回归分析。结果为
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/25/01.png)
注意不要用太高的次数，那样容易过拟合。
本文代码: 
https://github.com/zwdnet/MyQuant/blob/master/33



我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)