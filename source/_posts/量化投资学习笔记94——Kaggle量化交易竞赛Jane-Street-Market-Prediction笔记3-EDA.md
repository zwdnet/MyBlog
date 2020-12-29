---
title: 量化投资学习笔记94——Kaggle量化交易竞赛Jane Street Market Prediction笔记3-EDA
date: 2020-12-29 14:31:58
tags: [量化投资,kaggle竞赛,EDA,机器学习,学习笔记]
categories: 量化投资
---
接下来就正式开始干活吧。先进行数据探索(Exploratory Data Analysis，EDA)和特征工程。
主要参考了Wes McKinney.Python for Data Analysis. O'Reilly Media, Inc.October 2017:Second Edition.
还有几个个现成做好的：
[1](https://www.kaggle.com/muhammadmelsherbini/jane-street-extensive-eda)  [2](https://www.kaggle.com/manavtrivedi/eda-and-feature-selection)   [3](https://www.kaggle.com/carlmcbrideellis/jane-street-eda-of-day-0-and-feature-importance)
跟着这三个做吧。本文基本就是根据这三个notebook来的，排列组合了一下。
数据探索，就是看数据的特征，有没有什么规律，模式，可以在接下来的特征工程中应用。
加载数据后先看数据情况。
1.数据的基本情况：
print(df.info())
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/01.png)
有近240万列数据，138列。
2.目标值数据的情况。
①action列
增加目标列
df["action"] = np.where(df["resp"] > 0, 1, 0)
df.action = df.action.astype("category")
看看action的情况
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/02.png)
分布均匀，没有特别的模式。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/03.png)
②resp的情况
先看看收益的累积值。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/04.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/05.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/06.png)
前92天收益较高，resp_4的累积收益较高，resp_1的累积收益较低。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/07.png)
resp的[0.5%,99.5%]区间柱状图。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/08.png)
统计描述
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/09.png)
resp之间配对作图
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/10.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/11.png)
resp与resp_4，以及resp_1与resp_2之间高度相关。投资时区越长，风险及收益越大，反之越小。
把resp_1到resp_4画到一起。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/12.png)
再来看每天的收益波动情况。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/13.png)
更长时期的resp的标准差也更大。另外前100天的标准差大一些，因为80天后模型可能有调整。
③date列
下面分析date，
print(df.date.unique())
有500天的交易数据。
④weight列
再看weight
统计描述：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/14.png)
有17%的值为0。
画图看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/15.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/16.png)
对数分布图，用高斯曲线来拟合，有两个峰值。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/17.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/18.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/19.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/20.png)
偏态分布，有很多奇异值。
画散点图看resp和weight的关系。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/21.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/22.png)
两者不是线性相关的，高权重值与低收益值相关。
每天的累积回报，用resp乘weight得到的。 
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/23.png)
回报的分布情况：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/24.png)
⑤ts_id列及交易次数。
平均每天的ts_id数量和每天交易次数（假设每天交易时长6.5h）。在85天的那里画了线，想看看85天前后是否改变了策略。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/25.png)
每个交易日的交易次数分布。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/26.png)
3.features特征分析
①总体情况
看特征值的分布。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/27.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/28.png)
我们可以看到有很多异常值，影响特征分布。由于大部分数据集中于均值附近，用均值填充空值。
看累积值的情况。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/29.png)
大部分特征的累积均数是递增的，也有部分是递减，还有小部分是没有明显趋势的。
看来有四种不同类型的特征，分别画一个代表出来。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/30.png)
分别是线性正相关(Linear)，线性负相关(Negative)，复杂的(Noisy)，和混合的(Hybryd)。
特征的平均值：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/31.png)
每行/每列的均值，按要求的特征值分类。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/32.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/33.png)
每行/每列的标准差，同样按目标值分类
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/34.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/35.png)
特征的最大值
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/36.png)
最小值
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/37.png)
每行/每列的最小值分布
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/38.png)
看特征之间的相关性。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/39.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/40.png)
看起来很多特征之间存在共线性，画散点图看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/41.png)
由于这些特征是金融相关特征，很多都有很高的相关性。现在来看看有高度相关性的特征组。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/42.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/43.png)
另一组
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/44.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/45.png)
尽管相关系数很高，但变量并不完全是线性的，异常值影响了散点图的形状。
去除最小的0.1%和最大的0.1%值后的情况。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/47.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/48.png)

通过在特征分布上增加resp值，可以看到：①特征的柱状图现在有办法减少偏差形成更规则的分布。②一些特征比如1,2,85,87,88,91有很多负的偏差值。③一些特征49,50,51,55,56,57,58,59仍然有正的偏差值。④特征值分布不受resp值的影响。
特征值与resp的相关性
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/49.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/50.png)
②个别特征。
feature_0和特别，只有-1和1两个值。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/51.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/52.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/53.png)
看起来0号特征为正或为负与resp值无明显关系。但是用weight乘resp来作为收益，feature_0的值就与收益相关了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/54.png)
标签14的特征(feature_41-feature_43)很有趣，其特征在整个交易日内只有离散值。（是股票价格吗？)画散点图看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/55.png)
延迟画图（lag-plot,不知道啥意思）
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/56.png)
Tag22 特征60-68
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/57.png)
可以看到这些特征很相似。现在画直方图看看分布。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/58.png)
它们之间是 feature_64
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/59.png)
在0.7-1.38之间有间隙，像是(ln(2)=0.693, ln(4)=1.386)
Tag22还有很明显的每天的间隔，如feature64
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/60.png)
feature_64的全局最小值为-6.4，全局最大值为8，猜测其单位是30分钟。用arcsin试试。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/61.png)
再看看feature65
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/62.png)
再来看看分类为Noisy的特征。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/63.png)
Tag19 feature_51
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/64.png)
Tag19 feature_52
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/65.png)
Negative特征
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/66.png)
4.缺失值的情况：
temp = pd.DataFrame(train.isna().sum().sort_values(ascending = False) * 100/train.shape[0], columns = ["missing %"]).head(20)
print(temp)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/67.png)

大概有10%(14个)的特征的缺失值比例大于10%。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/68.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/69.png)

可以看到缺失值并不是随机分布的，中间有大段缺失值。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/70.png)
每列的缺失值情况。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/71.png)
交易日的特征值缺失情况。平均缺失3个。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/72.png)
平均每个交易的缺失特征数量：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/67/73.png)
原文还有聚类，降维等，在kaggle网站上运行太慢了（在我本地就更慢了，甚至不能完全加载所有数据），就先pass了。
5.EDA总结
①发现：
目标值：resp可以分为不同的4个周期，周期越长，收益和风险都越高。其中resp与resp_4、resp_1与resp_2相关度高。前92天收益较高，可能之后模型有变化。weight值有17%为0，因此计算收益的时候应该用resp×weight，而不是直接resp，可能更准确一些。每天的累积回报逐渐下降。weight值的对数分布有两个峰值，可能是两个分布的结合。
特征值：总体情况，大多数偏正态分布，但并不是完全如此。可以分成四种类型：分别是线性正相关(Linear)，线性负相关(Negative)，复杂的(Noisy)，和混合的(Hybryd)。有奇异值，可以用去除极端的两端的0.5%来尝试去除。特征之间相关性不大，其中19-26,29-36可能存在共线性。特征与resp之间的相关性大部分很小，也有部分相关性很大。
缺失值：约10%的特征的缺失值比例大于10%，缺失值分布呈现一定规律性，主要在一天的两个时段，可能与交易时间的间隔有关。在处理缺失值的时候可以考虑。
②总结EDA的套路：
先看数据整体情况，然后分别看每个特征的情况，画折线图、散点图，柱状分布图，累积图，箱状图等来研究。然后再对比特征之间的相关性，目标值之间的相关性，特征值与目标值之间的相关性等等，主要用相关性热点图，或者一起画折线图、散点图等来观察。最后，探索缺失值有没有什么规律。
接下来该进行特征工程了。
本文代码：https://github.com/zwdnet/JSMPwork/blob/main/EDA.py


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)