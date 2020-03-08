---
title: 量化投资学习笔记31——《Python机器学习应用》课程笔记05
date: 2020-03-08 13:18:32
tags: [量化投资,Python,机器学习,交叉验证]
categories: 量化投资
---
用分类算法进行上证指数涨跌预测。
根据今天以前的150个交易日的数据，预测今日股市涨跌。

交叉验证的思想:将数据集D划分为k个大小相似的互斥子集，每个子集都尽可能保持数据分布的一致性，即从D中通过分层抽样来得到。然后，每次用k-1个子集的并集作为训练集，余下的那个子集作为测试集。这样可以获得k组训练/测试集，从而可进行k次训练/测试，最终返回的是这k个测试结果的均值。通常称为"k者交叉验证"，常用取值是10。
```python
# coding:utf-8
# 用分类算法预测股市涨跌


import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
import tushare as ts


if __name__ == "__main__":
    # 读取股票数据
    data = pd.read_csv("HS300_his.csv")
    print(data.head())
    data.sort_index(0,ascending=True,inplace=True)
    print(data.head())
    dayfeature = 150
    featurenum = 4*dayfeature
    x = np.zeros((data.shape[0] - dayfeature, featurenum + 1))
    y = np.zeros((data.shape[0] - dayfeature))
    for i in range(0, data.shape[0] - dayfeature):
        x[i, 0:featurenum] = np.array(data[i:i+dayfeature][["close", "open", "low", "high"]]).reshape((1, featurenum))
        x[i, featurenum] = data.ix[i + dayfeature]["open"]
    for i in range(0, data.shape[0] - dayfeature):
        if data.ix[i + dayfeature]["close"] >= data.ix[i + dayfeature]["open"]:
            y[i] = 1
        else:
            y[i] = 0
    # 建模
    clf = svm.SVC(kernel = "rbf")
    result = []
    for i in range(5):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
        clf.fit(x_train, y_train)
        result.append(np.mean(y_test == clf.predict(x_test)))
    print("用rbf核函数的预测准确率:")
    print(result)
   
    clf = svm.SVC(kernel = "sigmoid")
    result = []
    for i in range(5):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
        clf.fit(x_train, y_train)
        result.append(np.mean(y_test == clf.predict(x_test)))
    print("用sigmoid核函数的预测准确率:")
    print(result)
```
预测结果
用rbf核函数的预测准确率: [0.6842105263157895, 0.5263157894736842, 0.47368421052631576, 0.47368421052631576, 0.5263157894736842]
用sigmoid核函数的预测准确率: [0.47368421052631576, 0.6842105263157895, 
0.5263157894736842, 0.42105263157894735, 0.5789473684210527]
可以看到预测成功率50%左右，跟瞎猜差不多。
本文代码:
https://github.com/zwdnet/MyQuant/blob/master/30


我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)