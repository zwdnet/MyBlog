---
title: 量化投资学习笔记32——《Python机器学习应用》课程笔记06
date: 2020-03-08 13:20:23
tags: [量化投资,Python,机器学习,回归分析,线性回归]
categories: 量化投资
---
讲有监督学习的线性回归。
线性回归是利用数理统计中的回归分析，来确定两种或两种以上变量间相互依赖的定量关系的一种统计分析方法。
只有一个自变量的回归称简单回归，大于一个变量的情况称多元回归。
用途:预测、分析变量与因变量关系的强度。
实例:对房屋尺寸与房价进行线性回归，预测房价。
分析:数据可视化，观察变量是否有线性关系。
画散点图
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/24/01.png)
可见明显呈线性趋势。
用sklearn进行线性回归，注意数据的维度需一致，用reshape进行调整。如
```python
linear.fit(x.reshape(length, -1), y)
```
完整代码见:
https://github.com/zwdnet/MyQuant/blob/master/30
回归的结果
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/24/01.png)


我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)