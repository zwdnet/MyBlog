---
title: 量化投资学习笔记36——《Python机器学习应用》课程笔记09
date: 2020-03-08 13:38:54
tags: [量化投资,Python,机器学习,手写识别,神经网络]
categories: 量化投资
---
手写识别实例，用神经网络实现。
手写识别是一个多分类任务，共有10个分类，即0-9。
图像识别是指利用计算机对图像进行处理、分析和理解，以识别各种不同模式的目标和对象的技术。一般经历文字识别，数字图像处理与识别和物体识别。
用DBRHD数据集，在这里下载: http://archive.ics.uci.edu/ml/machine-learning-databases/pendigits/
折腾了半天，程序是运行成功了，但结果不对。另找了一篇文章，用sklearn自带数据集digits。
https://blog.csdn.net/mcyjacky/article/details/85226752
```python
# coding:utf-8
# 神经网络实现手写识别


from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # 加载数据
    digits = load_digits()
    x_data = digits.data
    y_data = digits.target
    print(x_data.shape)
    print(y_data.shape)
   
    # 划分训练测试集
    x_train, x_test, y_train, y_test =  train_test_split(x_data, y_data)
    # 训练
    mlp = MLPClassifier(hidden_layer_sizes = (100, 50), max_iter = 500)
    mlp.fit(x_train, y_train)
    # 准确率评估
    predictions = mlp.predict(x_test)
    print(classification_report(y_test, predictions))
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/28/01.png)
准确率蛮高。细节还不明白，先会用吧。




我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)