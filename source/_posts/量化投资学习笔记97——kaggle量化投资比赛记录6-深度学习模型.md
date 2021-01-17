---
title: 量化投资学习笔记97——kaggle量化投资比赛记录6-深度学习模型
date: 2021-01-16 10:40:23
tags: [量化投资,kaggle竞赛,深度学习,pytorch,学习笔记]
categories: 量化投资
---
首先自己手撸一个，按照b站上的[视频](https://b23.tv/srXty3)来。
这是一个用神经网络解决二分类问题的简单例子，先用单层神经网络，然后用多层神经网络(深度学习了)。
神经网络的核心是将输入的每个神经节的值乘以其权重，再进行一定变换(比如用sigmoid函数，即激活函数)，得到输出。这个过程叫前向传播(Forward propagation)，得到的输出结果与训练值对比，计算误差，并用梯度下降法计算纠正值，纠正初始的权重(这叫反向传播，Back propagation)。如此循环多次，得到训练后的各个神经节的权重值，最后用这组权重值去预测。而多层神经网络在输入层和输出层之间有一层或多层隐藏层，每层有若干个神经节(隐藏层的层数和每层的神经节个数就是调参的对象)，前一层的输出就是后一层的输入，每一层都进行上述的前向传播和后向传播过程。机器学习的目的，就是确定这些权重系数。
根据视频用numpy实现了上述单层和多层神经网络，大致清楚了基础过程。接下来就尝试用pytorch框架实现这个过程。
用[这篇](https://towardsdatascience.com/understanding-pytorch-with-an-example-a-step-by-step-tutorial-81fc5f8c4e8e)跟着撸吧。（好像要科学上网......）
网上大多数pytorch都用图像方面的应用来做例子，比如识别手写数字等。这篇是用线性回归作为例子来写的，我觉得比较好。
把代码撸了一遍，使用pytorch的主要步骤是：
①把数据转化为张量tensor，还可以组装为Dataset，目的是可以使用DataLoader加载数据，可以分批加载。张量与numpy的n维数组的区别是前者可以在GPU里使用。注意设置需要的参数的requires_grad为True。
②创建模型，继承自torch.nn.Module。主要实现初始化参数和前向传播forward过程。
③设置超参数，如学习率，迭代次数等。
④设置损失函数类型，如nn.MSELoss等，根据模型类型选择合适的损失函数。
⑤设置优化器，如optim.SGD等。
⑥建立迭代循环，每次循环中依次完成下述步骤：
a.设置训练模式：model.train()
b.获取预测值：y_pred = model(x)
c.计算损失： loss = loss_fn(y, y_pred)
d.计算loss的梯度，后向传播过程：loss.backward()
e.更新参数、梯度置零（用优化器完成）：
optimizer.step()
optimizer.item()
f.返回损失值。
⑦迭代后获得结果的参数，即模型结果。
⑧应用建模结果的参数对新数据进行预测。
最主要的，计算损失、计算梯度、更新参数等都由pytorch操作。
[代码](https://github.com/zwdnet/JSMPwork/blob/main/test_pytorch.py)
下面就尝试用pytorch构建深度学习模型来解题。
```python
import torch
import torch.nn as nn
import torch.optim as optim
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import janestreet


# 工具函数，返回神经网络训练的每一步
def make_train_step(model, loss_fn, optimizer):
    # 执行在循环中训练过程
    def train_step(x, y):
        # 设置训练模式
        model.train()
        # 预测
        yhat = model(x)
        # 计算损失
        # print("测试")
        # print(len(yhat), len(y))
        yhat = yhat.squeeze(-1)
        loss = loss_fn(yhat, y)
        # 计算梯度
        loss.backward()
        # 更新参数，梯度置零
        optimizer.step()
        optimizer.zero_grad()
        # 返回损失值
        return loss.item()
        
    # 返回在训练循环中调用的函数
    return train_step


# 建模过程
def modeling(train):
    print("开始建模")
    
    x_train = train.loc[:, train.columns.str.contains('feature')]
    y_train = train.loc[:, 'action']
    
    x_tensor = torch.from_numpy(x_train.values).float().to(device)
    y_tensor = torch.from_numpy(y_train.values).float().to(device)
    
    class Model(nn.Module):
        def __init__(self):
            super(Model, self).__init__()
            self.linear1 = nn.Linear(130, 65)
            self.linear2 = nn.Linear(65, 30)
            self.linear3 = nn.Linear(30, 1)
            # self.linear4 = nn.Linear(25, 10)
            # self.linear5 = nn.Linear(10, 1)
            self.sigmoid = nn.Sigmoid()
        
        def forward(self, x):
            x = self.sigmoid(self.linear1(x))
            x = self.sigmoid(self.linear2(x))
            x = self.sigmoid(self.linear3(x))
            # x = self.sigmoid(self.linear4(x))
            # x = self.sigmoid(self.linear5(x))
            return x
            
    model = Model().to(device)
    print(model.state_dict())
    # 设置超参数
    lr = 1e-2
    n_epochs = 1000
     
    # loss_fn = nn.BCELoss(size_average = False)
    loss_fn = nn.MSELoss(reduction = "mean")
    optimizer = optim.SGD(model.parameters(), lr = lr)
    # 创建训练器
    train_step = make_train_step(model, loss_fn, optimizer)
    losses = []
    
    print("开始训练")
    # 进行训练
    for epoch in range(n_epochs):
        # y_tensor = y_tensor.detach()
        loss = train_step(x_tensor, y_tensor)
        losses.append(loss)
    
    return model

# 特征工程
def featureEngineer(data):
    data = data[data['weight'] != 0]
    data = data.fillna(0.0)
    weight = data['weight'].values
    resp = data['resp'].values
    data['action'] = ((weight * resp) > 0).astype('int')
    return data

# 进行预测，生成提交文件，分类版
def predict_clf(model):
    env = janestreet.make_env()
    iter_test = env.iter_test()
    for (test_df, sample_prediction_df) in iter_test:
        if test_df['weight'].item() > 0:
            X_test = test_df.loc[:, test_df.columns.str.contains('feature')]
            X_test = X_test.fillna(0.0)
            X_test_tensor = torch.from_numpy(X_test.values).float().to(device)
            res = model(X_test_tensor)
            if res >= 0.5:
                y_preds = 1
            else:
                y_preds = 0
        else:
            y_preds = 0
        print(y_preds)
        sample_prediction_df.action = y_preds
        env.predict(sample_prediction_df)
        
    
train = pd.read_csv("/kaggle/input/jane-street-market-prediction/train.csv")
train = featureEngineer(train)

print("深度学习")
model = modeling(train)
# 进行预测和提交
predict_clf(model)
print("结束。")
```
提交了，0分......再研究一下吧。
试一下[optuna](https://tigeraus.gitee.io/doc-optuna-chinese-build)
参考[这篇](https://blog.csdn.net/weixin_26752765/article/details/108225744)
用来找xgboost模型的参数，结果为learning_rate = 0.07, max_depth = 15。
用这个参数提交一次看看，结果是2892.153。看来还需要找更多的参数。先摆着吧，至少方法会了。
下次，打算从头学一下深度学习和pytorch，在kaggle上找到两篇文章。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
