---
title: 量化投资学习笔记28——《Python机器学习应用》课程笔记02
date: 2020-03-08 12:50:57
tags: [量化投资,Python,机器学习,降维,NMF算法,PCA算法]
categories: 量化投资
---
降维
PCA算法及其应用
主成分分析(PCA)，通常用于高维数据的探索与可视化。可以拔具有相关性的高维变量转化为线性无关的低维变量。称为主成分，能够尽可能保存原始数据的信息。
几个概念
方差:样本与样本均值的差的平方和的均值，用来度量一组数据的分散程度。
协方差:用于度量两个变量的线性相关程度。
特征向量:描述数据集结构的非零向量。
原理:矩阵的主成分就是其协方差矩阵对应的特征向量，按照对应特征值排序，分为第一主成分，第二主成分，以此类推。
在sklearn中使用decomposition模块中的PCA进行降维。
实例，用PCA将鸢尾花数据进行降维，可视化。
代码见: https://github.com/zwdnet/MyQuant/blob/master/26/PCAtest.py
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/22/01.png)
非负矩阵分解(NMF)
是在矩阵中所有元素均为非负数约束条件下的矩阵分解方法。
基本思想:给定一个非负矩阵V，NMF能够找到一个非负矩阵W和一个非负矩阵H，使得二者的乘积近似等于矩阵V中的值。
W矩阵，从原矩阵V中提取的特征。
H矩阵，系数矩阵。
分解目标，最小化W与H乘积与V的差异。
在sklearn中使用decomposition模块中的NMF进行分解。
实例，用NMF进行人脸图像数据集Olivetti特征提取。
代码见: https://github.com/zwdnet/MyQuant/blob/master/26/face.py
这是原图
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/22/02.png)
NMF算法的结果
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/22/03.png)
PCA算法的结果
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/22/04.png)
可以看到NMF算法好一点。


我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)