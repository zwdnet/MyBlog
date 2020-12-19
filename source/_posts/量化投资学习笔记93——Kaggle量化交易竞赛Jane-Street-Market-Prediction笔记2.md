---
title: 量化投资学习笔记93——Kaggle量化交易竞赛Jane Street Market Prediction笔记2
date: 2020-12-19 12:46:18
tags: [量化投资,kaggle竞赛,机器学习,学习笔记]
categories: 量化投资
---
下面完全copy[人家的kernel](https://www.kaggle.com/isaienkov/jane-street-market-prediction-fast-understanding)看一下吧。
先看看目标特征的分布情况。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/01.png)
用到了ploty库，折腾了好久，装了好多库才成功。
weight是偏态的，其它几个都是正态的。再来看看features的分布。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/02.png)
主要是正态分布，偏态分布也有。
读取其它数据文件看看。
下面开始建模了。我还是用1/10的数据吧。
先看看特征值之间的相关性，只画相关度大于0.95的。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/03.png)
再看目标值的相关度。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/04.png)
下面真正开始干活。
具体代码就不在这里赘述了，见github上的源代码吧。
在kaggle上运行，很慢，四十几分钟都不动，又改成使用GPU。效果很好，90几秒就完成了，提交。又是长长的等待，最后看结果
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/05.png)
嘿嘿，这个靠谱，在其基础上改进吧。
随便吓改了一下参数，再提交试试。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/06.png)
果然没人家的好。改回去吧。接下来一是折腾特征工程，ta这个是直接用-999填充了空值，没做其它的了。二是试试其它模型，包括深度学习的。
再加一个附加任务吧:实现一个评分函数，用题目给出的评分公式，在本地对预测结果评分。
结果评估：采用效用分数。测试集的每一行代表一个交易机会，你必须预测一个行动值（action value），值为1进行交易，值为0拒绝交易。每个交易j有两个值，weight和resp，代表一个收益结果。
对于每个日期i，定义
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/07.png)
其中i的绝对值是测试集中的不同的数据的个数。效用分数定义为：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/66/08.png)
```python
# 评分函数
def Score(date, weight, resp, action):
    count_i = len(np.unique(date))
    Pi = np.zeros(count_i)
    # 用循环太慢
    #for i, day in enumerate(np.unique(date)):
#        Pi[i] = np.sum(weight[date == day] * resp[date == day] * action[date == day])
    # 用下面这行代替
    Pi = np.bincount(date, weight * resp * action)
    t = np.sum(Pi) / np.sqrt(np.sum(Pi ** 2)) * np.sqrt(250 / count_i)
    u = np.clip(t, 0, 6) * np.sum(Pi)
    return u
```
上面代码参考了[这里](https://www.kaggle.com/gogo827jz/jane-street-super-fast-utility-score-function)
用线性回归作为模型，提交看看。
提交出错了，提示没找到csv文件。折腾了两天，才发现原来是提交环境里可能没有example_test文件，用train.csv代替就对了。把评分程序和提交程序都封装到函数里，这样框架基本上就搭好了，可以具体干活了。下次吧。

[代码]( https://github.com/zwdnet/JSMPwork/blob/main/works.py)


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)