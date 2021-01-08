---
title: 量化投资学习笔记95——kaggle量化投资比赛记录4-尝试各种模型
date: 2021-01-08 15:47:27
tags: [量化投资,kaggle竞赛,分类模型,机器学习,学习笔记]
categories: 量化投资
---
完成了EDA，下面本来该进行特征工程了。但是有个问题是，这个题目是金融相关的，为了防止使用未来函数，要求用题目给函数来提交，大概就是把测试数据一个一个的提供，而不是一起提供吧。这就带来一个问题就是连填充空值也有问题，比如用均值填充，在训练数据上可以，在测试数据上就失败了。在本地能跑通的程序，在kaggle上却不行。也有办法，比如记录训练集的每列的均值，拿来填充测试集的均值。以后再试吧。先简单地用0来填充空值。
下面尝试一下各种预测算法吧。线性回归试了一下，评分不高，就主要用分类模型和聚类吧。
sklearn文档里有个算法选择图:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/01.png)
就用这些。
先写评估模型的函数
```python
# 对模型进行交叉验证
def cross_val(model, X, Y, cv = 5):
    scores = cross_val_score(model, X, Y, cv=cv)
    score = scores.mean()
    return score
```
用的方法是k折交叉验证，即将所有数据分成k份，不重复地每次取一份做测试集，其它几份作为训练集，计算该模型在数据集上的MSE，最后取平均数。
```python
# 模型评估
def evalution(model, test):
    X = test.loc[:, test.columns.str.contains("feature")].values
    y_true = test.action.values
    y_pred = model.predict(X)
    target_names = ["1", "0"]
    result = classification_report(y_true, y_pred, target_names = target_names)
    print(result, type(result))
```
用这些评分函数回测一下逻辑回归模型:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/02.png)
具体的含义:
precision是预测精确度，被预测的结果的准确性，分母是预测出的数据。TP/(TP+FP)，比瞎猜好不了多少啊。
recall是召回率，即所有真实的样本有多少被正确预测出来了。分母是原数据。TP/(TP+FN)。
f1-score:二者的调和均值。等于1时最佳，等于0时最差。2*precision*recall/(precision+recall)
在二分类场景中，正标签的召回率称为敏感度（sensitivity），负标签的召回率称为特异性（specificity）。
比瞎猜好那么一点点。
另外再画一下ROC曲线。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/03.png)
图像越偏左上角越好，可以看到ROC几乎跟对角线重合，也就是跟瞎猜差不多了。
从https://blog.csdn.net/quiet_girl/article/details/70830796借张图：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/04.png)
曲线与DBC围成的面积越大越好。
再画一下学习曲线：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/05.png)
提交到kaggle的结果
Public Score:2038.005
下面就用其它分类算法来尝试。开始用20%的数据，结果在服务器上跑了一夜，12小时，还没有出结果。后来就改用1%的数据，跑了好几个小时才完。
导入相关的库
```python
# 支持向量机
from sklearn.svm import SVC, LinearSVC
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/06.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/07.png)
```python
# 随机森林
from sklearn.ensemble import RandomForestClassifier
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/08.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/09.png)
```python
# KNN算法
from sklearn.neighbors import KNeighborsClassifier
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/10.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/11.png)
```python
# 朴素贝叶斯算法
from sklearn.naive_bayes import GaussianNB
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/12.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/13.png)
```python
# SGD算法
from sklearn.linear_model import SGDClassifier
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/14.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/15.png)
```python
# 决策树算法
from sklearn.tree import DecisionTreeClassifier
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/16.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/17.png)
从ROC曲线来看，这几个模型都不太好。再来看学习曲线，怎么看呢？
再从https://ljalphabeta.gitbooks.io/python-/content/debugging.html 借张图吧：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/68/18.png)
左上角的是高偏差的模型，训练集和测试集准确率都很低(低于我们可以接受的水平，比如这里，准确率仅稍微高于0.5，比瞎猜只好那么一点），很可能是欠拟合。解决方法是增加模型参数，减小正则项。上面的模型中，朴素贝叶斯和SGD算法属于此类。
右上角是高方差的模型，表现是训练集和测试集准确率相差太多。可能属于模型过拟合了。解决方法是增加训练集或降低模型复杂度，如增大正则项，或通过特征选择减少特征数。上面的随机森林，支持向量机，knn，决策树等模型属于这种情况。
右下角是我们想要的，随着样本数量的上升，训练集和测试集的准确率收敛到一个水平，而这个水平是我们可以接受的水平。
挨个提交看看吧。kaggle提交太慢了。结果先不发了，应该也不好。下次试试模型集成。

本文代码：
https://github.com/zwdnet/JSMPwork/blob/main/test_work.py
https://github.com/zwdnet/JSMPwork/blob/main/tools.py


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)