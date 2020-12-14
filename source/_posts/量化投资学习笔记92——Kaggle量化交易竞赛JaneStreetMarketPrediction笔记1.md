---
title: 量化投资学习笔记92——Kaggle量化交易竞赛JaneStreetMarketPrediction笔记1
date: 2020-12-14 16:25:18
tags: [量化投资,kaggle竞赛,机器学习,学习笔记]
categories: 量化投资
---
以下竞赛介绍翻译自[官网](https://www.kaggle.com/c/jane-street-market-prediction)
“低买高卖”，听起来很容易......
实际上，为盈利而交易是一个很难的问题，尤其是在当今这个快速变化的复杂金融市场上。电子化交易允许在几分之一秒内进行数千次交易，导致有几乎无限的获利的机会。
在一个完美有效市场，买卖者拥有做出理性交易决策所需要的所有信息。结果，产品会总是保持在它们的“公平价格”(fair values)，并且从来不会被低估或高估。然而现实的金融市场不是完美有效的。
开发出交易策略来识别和利用市场无效性是一个挑战。即便一个策略在目前是能获利的，它在未来未必能获利，而且市场波动会使得预测任何给定的交易的盈利情况变得不可能。结果，很那区分好运气和做出了好的交易决策。
在本竞赛的头三个月，你将构建你自己的量化交易模型以最大化你的收益，你所使用的市场数据来自全球主要证券交易市场的数据。接下来，你将用未来市场的回报测试模型，并在排行榜上收到反馈。
您的挑战包括使用历史数据，数学工具，技术工具，以创建一个模型，尽可能符合于现实。你将被给予一定数量的潜在交易机会，你的模型必须选择接受或拒绝。
一般来说，如果一个模型能够产生较高的预测度，以选择正确的交易来执行，它们将会在传递市场信号，推动价格接近“公平”价格中发挥很重要的作用。即，一个更好的模型意味着市场会更有效。然而，开发一个好的模型意味着很多挑战，包括很低的信噪比，潜在的冗余，强的特征相关性，以及难以求解的数学问题。
Jane Street是一个量化交易机构，开发了很多交易模型并获利。这个问题是对他们日常工作的简化。
结果评估：采用效用分数。测试集的每一行代表一个交易机会，你必须预测一个行动值（action value），值为1进行交易，值为0拒绝交易。每个交易j有两个值，weight和resp，代表一个收益结果。
对于每个数据i，定义
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/01.png)
其中i的绝对值是测试集中的不同的数据的个数。效用分数定义为：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/02.png)
提交文件：必须用python time-series API提交数据，它能确保模型没有使用未来数据。使用方法如下：
```python
import janestreet
env = janestreet.make_env() # initialize the environment
iter_test = env.iter_test() # an iterator which loops over the test set

for (test_df, sample_prediction_df) in iter_test:
    sample_prediction_df.action = 0 #make your 0/1 prediction here
    env.predict(sample_prediction_df)
```
时间限制：
参加时间限制：2021年2月15日之前。
组队合并限制：2021年2月15日之前。
最后提交限制：2021年2月22日之前。
预测时间显示：2021年8月23日之前。
不允许在团队外私自分享代码或数据。
奖金：
总奖金10万刀，一等奖4万刀，二等奖2万刀，三等奖1万刀，四至九名，5000刀。

数据描述
包括一系列匿名的特征，feature_0...feature_129,代表了真实市场数据。数据集中每一行代表了一个交易机会，你的模型要根据这些数据预测一个行动值：1（交易）或0（不交易）。每个交易有一个相应的weight和resp，它们一起代表了一个交易的回报。date列是一个整数，代表了交易的日期，ts_id代表了一个时间顺序。为了匿名化(anonymized)特征值，提供了一个特征值的元数据。
在训练集，train.csv，提供了一个resp值，还有其它四个resp_1,...resp_4值，代表不同时区的收益值。在测试集中没有这些数据。weight=0的数据是为了完整性保留在数据集中，尽管它们对模型评分没有贡献。
使用时间序列API(time-series API)来确保模型没有使用未来数据。当提交数据的时候，需要使用时间序列API。

实操记录
首先在服务器上下载数据，有2.5G，直接读取，超过内存报错啦。
想了很多办法，先读取数据的1/100，画图，意外发现数据有两种类型，一种像随机数据
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/03.png)
还有一种是类似三角形的
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/04.png)
之后，发现一个处理数据规模大于物理内存的库:dask，用法跟pandas类似，只是它是延迟计算的，真正算的时候调用computer成员函数:
```python
import matplotlib.pyplot as plt
import dask.dataframe as dd
data = dd.read_csv("./train.csv")
fig = plt.figure()
plt.plot(data["weight"].values.compute())
plt.savefig("./output/weight.png")
```
dask官网:https://docs.dask.org
这样把训练集所有数据按列分别画图，等于用时间换空间，在服务器上整整运行了一天多才完。把图片down下来看看，完整的数据的图形就比较正常了。但是实际预测的时候用dask可能太慢了，还是就用1/10的数据吧。
```python
n = 2390491
row_read = int(n/10)
data = pd.read_csv("./train.csv", nrows = row_read)
print(data.info())
data.to_csv("./small_train.csv")
```
之后就用small_train.csv里的数据干活吧。
把small_train.csv从服务器上下载回来，1/10的数据就有591MB。
很多特征里有空行。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/05.png)
特征之间差异很大，还要进行归一化吧。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/06.png)
先填充空值
```python
# 复制数据，进行操作
newdata = data.copy()
# 填充空值 向前填充
newdata = newdata.fillna(method = "backfill")
print(newdata.info(verbose = True, null_counts = True))
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/07.png)
然后归一化，用max-min归一化。
```python
# 数据归一化
features = (features - features.min())/(features.max() - features.min())
print(features.describe())
# 更新原来的特征数据
newdata.update(features)
print(newdata.head())
```
现在可以开始干活了。先用weight和resp构造一个训练集的行动变量。参考[这里](https://github.com/amareshgood/Jane-Street-Market-Prediction/blob/main/jane_street_market_predictions.ipynb)
```python
# 够造训练集的行动变量
newdata["action"] = ((newdata["weight"].values * newdata["resp"].values) > 0).astype("int")
```
把上述代码放到一个函数里，算是特征工程了。
接下来可以开始训练了。先用最简单的多元线性回归吧。
参考[这里](https://github.com/767472021/Jane-Street-Market-Prediction/blob/master/EDA.ipynb)
```python
# 线性回归模型
def LR(data):
    train_set, test_set, train_action, test_action = train_test_split(data.loc[:, "feature_0":"feature_129"], data.action, test_size = 0.2)
    print(len(train_set))
    # 训练
    linreg = LinearRegression()
    linreg.fit(train_set, train_action)
    # 预测
    train_pred = linreg.predict(train_set)
    test_pred = linreg.predict(test_set)
    # 模型评估
    print("train MSE:", metrics.mean_squared_error(train_action, train_pred))
    print("test MSE:", metrics.mean_squared_error(test_action, test_pred))
    print("train RMSE:", np.sqrt(metrics.mean_squared_error(train_action, train_pred)))
    print("test RMSE:", np.sqrt(metrics.mean_squared_error(test_action, test_pred)))
    # 保存模型到文件
    # joblib.dump(linreg, "LinesRegress.pkl")
    with open("LinesRegress.pkl", "wb") as fw:
        pickle.dump(linreg, fw)
    print(test_pred)
```
提交的时候才发现，预测结果是浮点数，提交要求的是整数。就简单设置成大于0的结果设为1，小于等于0的结果设为0。
第一次用notebook的方式提交，参考了[这里](https://www.kaggle.com/gogo827jz/jane-street-neural-network-starter)
写了提交的notebook，折腾半天，终于提交成功了。
结果:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/08.png)
比全是1或者随机的结果好，但是分很低。排行榜上分最高的大神分数有8000多分……再努力吧。另外处理缺失值的方法得改了，提交的时候测试数据貌似是用一个for循环一个值一个值的给出的，而不是一下子给出来。
照[人家的notebook](https://www.kaggle.com/harshit2708/linear-regression)改一个看看
看了人家的，是预测resp变量，然后再用weight×resp的值决定行动值是0还是1。另外是用sklearn的SimpleImputer, MissingIndicator来处理缺失值。
画了一下预测值和实际值。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/09.png)
再提交看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/65/10.png)
尝试了几次，都是0分。不知道哪里出问题了。不管怎么样，框架是有了。细节再慢慢搞吧。
[代码](https://github.com/zwdnet/JSMPwork)


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)