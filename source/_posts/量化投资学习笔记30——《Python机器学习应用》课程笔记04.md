---
title: 量化投资学习笔记30——《Python机器学习应用》课程笔记04
date: 2020-03-08 13:05:25
tags: [量化投资,Python,机器学习,监督学习]
categories: 量化投资
---
有监督学习
常用分类算法
KNN:K近邻分类器。通过计算待分类数据点，与已知数据中所有点的距离，取距离最小的前K个点，根据"少数服从多数"的原则，将这个数据点划分为出现次数最多的那个类别。
在sklearn中，使用sklearn.neighbors.KNeighborsClassifier创建K邻近分类器。
选取较大K值，可以减小误差，但可能导致预测错误。选取k值较小，易引起过拟合。一般倾向于选择较小的k值，并使用交叉验证法选取最优的k值。
决策树算法
是一种树形结构分类器，通过顺序询问分类点的属性决定分类点最终的类别。通常根据特征的信息增益等构建决策树。
使用sklearn.tree.DecisionTreeClassifier构建决策树进行分类。
决策树本质上是寻找一种对特征空间上的划分，旨在构建一个训练数据拟合的好，并且复杂度小的决策树。
朴素贝叶斯
以贝叶斯定理为基础的分类器。sklearn实现了三个朴素贝叶斯分类器:高斯朴素贝叶斯，多项式朴素贝叶斯，伯努利朴素贝叶斯。分别适用与不同的观测值的分布。
朴素贝叶斯是典型的生成学习算法。在小规模的数据上表现良好，适合进行多分类任务。
代码: https://github.com/zwdnet/MyQuant/blob/master/30



我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)

