---
title: 量化投资学习笔记37——《Python机器学习应用》课程笔记10
date: 2020-03-08 13:41:32
tags: [量化投资,Python,机器学习,手写识别,KNN算法]
categories: 量化投资
---
用KNN算法来进行数字识别，还是用sklearn自带的digits数据集。
```python
# coding:utf-8
# KNN算法实现手写识别


from sklearn import neighbors
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
    knn = neighbors.KNeighborsClassifier(algorithm = "kd_tree", n_neighbors = 3)
    knn.fit(x_train, y_train)
    # 准确率评估
    predictions = knn.predict(x_test)
    print(classification_report(y_test, predictions))
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/29/02.png)
除了训练那部分，代码几乎都是抄前文的。可以看到用sklearn库非常方便。结果也很好，准确率98%。
KNN的准确率远高于MLP分类器，原因是MLP在小数据集上容易过拟合。而且MLP对于参数调整比较敏感。
接下来是强化学习。




我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)