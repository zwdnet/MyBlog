---
title: 量化投资学习笔记96——kaggle量化投资比赛记录5-模型集成
date: 2021-01-11 15:36:06
tags: [量化投资,kaggle竞赛,模型集成,XGBoost,机器学习,学习笔记]
categories: 量化投资
---
上次尝试了几个机器学习的分类模型，效果都不太好。准确率刚刚超过50%，比瞎猜稍微好一点。提交以后分数最高的还是逻辑回归的2038分。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/01.png)
下面实施模型集成。
集成把不同模型的预测结果结合起来，生成最终预测，集成的模型越多，效果就越好。另外，由于集成结合了不同的基线预测，它们的性能至少等同于最优的基线模型。集成使得我们几乎免费就获得了性能提升！
集成的基本概念：结合多个模型的预测，对特异性误差取平均，从而获得更好的整体预测结果。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/02.png)
stacking：stacking是一种分层模型集成框架。以两层为例，第一层由多个基学习器组成，其输入为原始训练集，第二层的模型则是以第一层基学习器的输出作为特征加入训练集进行再训练，从而得到完整的stacking模型。
不同的模型，是在不同的角度观察我们的数据集。
基本步骤:
①选择基模型。各种基本的机器学习算法。
②把训练集分成不交叉的若干份。
③将其中一份作为预测集，使用其它份进行建模，预测预测集，保留结果。
④把预测结果按照对应的位置填上，得到对整个数据集在第一个基模型上的一个stacking转换。
⑤在④的过程中，每个模型分别对测试集进行预测，并保留这五列结果，取平均值，作为该基模型对测试集数据的一个stacking转换。
⑥对其它基模型重复②-⑤步。
⑦一般使用LR作为第二层的模型进行建模预测。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/03.png)
整个过程比较耗时，尽量增加一些不同类型的模型。
下面实操
用XGBoost。所谓 Boosting ，就是将弱分离器 f_i(x) 组合起来形成强分类器 F(x) 的一种方法。Boost的三个要素:待优化的损失函数，弱的做预测的分类器，附加的模型(将弱的分类器累加起来形成强分类器，进而使目标损失函数达到极小)。
先导入库
```python
from xgboost import XGBClassifier
```
然后完全用默认参数，用1%的数据在服务器里跑一下看看。
```python
model = XGBClassifier()
model.fit(X_train, y_train)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/04.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/05.png)
花了2个多小时。
在kaggle里提交的时候用了“tree_method="gpu_hist"”参数，使用GPU加速。每周可以使用40小时。真的快了好多。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/06.png)
结果还不错。下面试试调参，网上看到一个步骤：
①设置一些初始值。
②保持learning rate和其他booster相关的参数不变，调节和estimators的参数。
③保证estimators和其他的booster参数不变，调节learning rate
④保持estimators和learning rate不变，调节booste相关的参数。可以从影响最大的max_depth和min_child_weight开始。逐步调节所有可能影响的booster参数。
⑤缩小learning rate,得到最佳的learing rate值。
⑥得到一组效果还不错的参数组合。
先显示训练时每一步的分数，把训练代码改成
```python
    model = XGBClassifier()
    eval_set = [(X_train, y_train)]
    model.fit(X_train, y_train, early_stopping_rounds = 10, eval_metric = "logloss", eval_set = eval_set, verbose = True)
```
再输出特征重要性
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/07.png)
下面来看看XGBoost有哪些参数？分三类：通用参数（General Parameters）、Booster参数、学习目标参数（Task Parameters）。
1.通用参数：
booster:有gbtree和gblinear两种，前者使用基于树的模型，后者使用线性模型，默认gbtree。
silent:运行时是否输出信息，默认为0，不输出。
nthread:使用的线程数，默认为可以使用的最大值。
num_pbuffer：使用的缓存大小，由xgboost自动设置。
num_feature：使用的特征个数，自动设置，不用调。
2.tree booster参数
eta:更新过程中的收缩步长，即学习率。通过缩减特征的权重使提升计算过程更加保守。缺省为0.3，取值范围[0,1]，通常设置为[0.01,0.2]。
gamma:也称min_split_loss，在树的叶节点进行进一步划分时所需的最小损失的减少值，制定了节点分裂所需的最小损失函数下降值。值越大，算法越保守。该值需调节，范围[0,无穷大]，默认为0。
max_depth：树的最大深度，缺省为6。取值范围为[1,无穷]，指树的最大深度，树的深度越大，对数据的拟合程度越高（过拟合程度也越高）。控制过拟合。建议通过交叉验证调参，通常3-10。
min_child_weight:孩子节点中最小的样本权重和。如果一个叶子节点的样本权重和小于min_child_weight则拆分过程结束。指建立每个模型所需要的最小样本数。控制过拟合。范围[0,无穷大]。默认为1。
max_delta_step:在每棵树的权重估计中，允许的最大delta步长。如果为0，意味着没有约束。如果设置为一个正数，有助于在更新步长的时候，使模型更加保守。当类别极度不平衡时，有助于逻辑回归模型的训练。设置为1-10，可能有助于控制更新。取值范围[0,无穷大]。
subsample:用于训练模型的子样本占整个样本集合的比例。如果设置为0.5意味着将随机从整个样本集合中抽取出50%的子样本建立树模型，能够防止过拟合。取值范围(0,1]，默认1。
colsample_bytree:在建立树时对特征随机采样的比例。缺省值为1，取值范围(0,1]。
colsample_bylevel:决定每次节点划分时子样例的比例。通常不使用。
scale_pos_weight:大于0的取值可以处理类别不平衡的情况，帮助模型更快收敛。
3.Linear Booster参数
lambda:L2正则的惩罚系数，用于处理正则化部分，通常不使用，但可以用来降低过拟合。
alpha:L1正则的惩罚系数，当数据维度极高时可以使用，使得算法运行更快。
lambda_bias:在偏置上的L2正则，缺省为0.
4.学习目标参数
objective:定义学习任务及相应的学习目标。
"reg:linear"线性回归
"reg:logistic"逻辑回归
"binary:logistic"二分类的逻辑回归问题，输出为概率。
"binary:logitraw"二分类的逻辑回归问题，输出结果为wTx。
"count:poisson"计数问题的poisson回归，输出结果为poisson分布。
"multi:softmax"让XGBoost采用softmax目标函数处理多分类问题，同时需要设置参数num_class(类别个数）
"multi:softprob"同上，但输出是ndata×nclass的向量，可以将该向量reshape成ndata行nclass列的矩阵。每行数据表示样本所属于每个类别的概率。
"rank:pairwise"采用评分机制进行训练。
默认为"reg:linear"
base_score:所有实例的初始化预测分数，全局偏置。为了足够的迭代次数，改变这个值将不会有太大的影响。
eval_metric:校验数据所需要的评价指标，不同目标函数将会有缺省的评价指标。用户可以添加，用list传递参数给程序，而不是map参数。可选的有"rmse","logloss","error","merror","mlogloss","auc","ndcg","map"......
seed：随机数种子，缺省为0。
采用字典方式提供parms参数，即为上述参数的"名称":值的形式。
先按网站1的方法调参。
先调learning_rate, tree_depth, subsample三个参数。
学习率
```python
def tc(X, Y):
    model = XGBClassifier(use_label_encoder=False, eval_metric = "logloss")
    learning_rate = [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3]
    param_grid = dict(learning_rate=learning_rate)
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
    grid_search = GridSearchCV(model, param_grid, scoring="neg_log_loss", n_jobs=-1, cv=kfold)
    grid_result = grid_search.fit(X, Y)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    # 输出每个学习率对应分数
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    y = []
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))
        y.append(mean)
    plt.plot(learning_rate, y)
    plt.savefig("./output/learning_rate.png")
```
0.1最佳。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/08.png)
提交看看
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/09.png)
不错，提高了800多分。
再试试max_depth参数。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/10.png)
最好的是3，但345差不多。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/11.png)
用3，提交一次看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/69/12.png)
看来是欠拟合了。还可以进行其它参数的调整测试，先掌握方法，到这里吧。跑一次提交太慢了，要几个小时才看得到结果。目前为止我自己折腾的最高分是3903分，下次该考虑用深度学习试试了。
本文代码： https://github.com/zwdnet/JSMPwork/blob/main/myxgboost.py


参考资料：
[1]https://www.jianshu.com/p/7e0e2d66b3d4
[2]https://xgboost.readthedocs.io/en/latest/
[3]https://cloud.tencent.com/developer/article/1387686
[4]https://zhuanlan.zhihu.com/p/28672955
[5]https://blog.csdn.net/qq_30868737/article/details/108010935
[6]https://blog.csdn.net/weixin_41580067/article/details/86514402
[7]https://blog.csdn.net/qq_30868737/article/details/108385115



我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)