---
title: 量化投资学习笔记98——kaggle量化投资比赛记录7-深度学习及pytorch
date: 2021-01-21 06:41:04
tags: [量化投资,kaggle竞赛,深度学习,pytorch,学习笔记]
categories: 量化投资
---
本文主要参考kaggle上的两篇文章：
[Deep Learning Tutorial for Beginners](https://www.kaggle.com/kanncaa1/deep-learning-tutorial-for-beginners)
[Pytorch Tutorial for Deep Learning Lovers](https://www.kaggle.com/kanncaa1/pytorch-tutorial-for-deep-learning-lovers)
不是全文翻译，算是我的学习笔记吧。
先看Deep Learning Tutorial for Beginners。
深度学习，是一种直接从数据中学习特征的机器学习技术。（Deep learning: One of the machine learning technique that learns features directly from data.）随着数据规模上升（如超过1百万个数据），传统机器学习技术不太适合，深度学习在准确率方面有更好的表现。深度学习应用在语音识别，图像分类，自然语言处理(nlp)或者推荐系统等方面。机器学习包括深度学习，在机器学习中，特征是人工标注的，而深度学习中特征是直接从数据中学习出来的。
实验数据是2062个手语数字图像，从0到9，一共10个不同的符号。0的序号从204到408,有205个。1的序号从822到1027,有206个。先只考虑0和1两个数字，因此每个分类有205个样本。尽管205个样本对深度学习来说太少了，但这是教程，就不管了。
先加载数据（从教程页面上下载，放到源代码目录。）
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings("ignore")


# 加载数据
def loadData():
    x_1 = np.load("./X.npy")
    y_1 = np.load("./Y.npy")
    img_size = 64
    plt.subplot(1, 2, 1)
    plt.imshow(x_1[260].reshape(img_size, img_size))
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(x_1[900].reshape(img_size, img_size))
    plt.axis("off")
    plt.savefig("./output/data.png")
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/data.png)
把数据连接起来，并创建标签。
```python
    # 把数据连接起来，并创建标签
    X = np.concatenate((x_1[204:409], x_1[822:1027]), axis = 0)
    z = np.zeros(205)
    o = np.ones(205)
    Y = np.concatenate((z, o), axis = 0).reshape(X.shape[0], 1)
    print(X.shape)
    print(Y.shape)
```

X的大小是(410, 64, 64)，即410个图片，每个图片的大小是64×64
Y的大小是(410, 1)，即有410个标签。
现在将数据划分为训练集和测试集，其中训练集占85%。

```python
    # 划分训练集和测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.15, random_state = 42)
    number_of_train = X_train.shape[0]
    number_of_test = X_test.shape[0]
```

将三维数据变换到二维(flatten)
```python
    #将三维数据变换到二维
    X_train_flatten = X_train.reshape(number_of_train, X_train.shape[1]*X_train.shape[2])
    X_test_flatten = X_test.reshape(number_of_test, X_test.shape[1]*X_test.shape[2])
    print("X_train_flatten", X_train_flatten.shape)
    print("X_test_flatten", X_test_flatten.shape)
```
```python
X_train_flatten (348, 4096)
X_test_flatten (62, 4096)
```

将数据倒置
```python
    x_train = X_train_flatten.T
    x_test = X_test_flatten.T
    y_train = Y_train.T
    y_test = Y_test.T
    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)
```
```python
(4096, 348)
(4096, 62)
(1, 348)
(1, 62)
```

数据准备好了，下面开始干活。
一想到二分类问题我们首先想到的是逻辑回归。实际上逻辑回归是一个非常简单的神经网络。神经网络和深度学习是一回事。
计算图(computation graph)的概念
数学表达式的可视化。这个我这只能看到图片的一部分，折腾半天没弄下来，大家到网站上看吧。
逻辑回归同样有计算图。参数是权重(weight)和偏差值(bias)。权重是每个点的系数，偏差值是截距。
z = (w.t)x+b
另一个说法：z = b+px1w1+px2w2+...+px4096*w4096
yhead = sigmoid(z)
sigmoid使得z在[0,1]区间内。即一个概率值。
sigmoid函数的计算图
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/02.jpg)
为什么我们使用sigmoid函数？它返回一个概率性的结果，它是可微的，因此我们可以使用梯度下降算法。
下面我们初始化参数。
输入的数据是有4096个点的图像，每个点都有其自己的权重值。第一步是将每个点乘以其自己的权重值。初始权重值的设置有不同的方法，这里设置为0.01。偏差值为0。
下面是代码。
```python
# 初始化参数
def init_params(dimension):
    w = np.full((dimension, 1), 0.01)
    b = 0.0
    return w, b
```
下面看前向传播过程：从输入点数据到成本的所有步骤称为前向传播(Forward Propagation)。
z = (w.T)x + b，w和b都知道了（.T是转置），可以算出z。将z输入sigmoid函数得到返回的概率值yhat。然后计算损失/误差函数(loss/error)。所有损失值之和就是成本。
下面撸代码：
先定义sigmoid函数。
```python
# 定义sigmoid函数
def sigmoid(z):
    y_head = 1/(1+np.exp(-z))
    return y_head
```
然后计算损失函数，使得当模型预测正确时损失值很小，而当预测错误时损失值很大。
下面实现前向传播过程。
```python

# 前向传播过程
def fp(w, b, x_train, y_train):
    z = np.dot(w.T, x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head) - (1-y_train)*np.log(1-y_head)
    # 平均成本
    cost = (np.sum(loss))/x_train.shape[1]
    return cost
```

采用梯度下降的优化算法
我们需要降低成本。首先初始化权重和偏置值，这决定了初始成本。然后要更新权重和偏置值。这项技术称为梯度下降。
更新的方法，用老的参数值减去在该点的梯度，将该值作为参数的新的值。计算梯度的方法，是求损失函数在该点对该参数的偏导数。梯度同时确定了迭代的大小和方向。在迭代的时候，梯度要乘以一个学习率α。w' = w - α∂L/∂w 学习率是需要权衡的，太小，学习得太慢，但不容易错过最低值。太大，学习得快，但容易错过最低值。学习率也被称为超参数(hyperparameter)，是需要选择和调参的。因此前向过程就是从参数到成本，反向过程就是从成本到参数，更新参数。怎么计算梯度及更新参数，就是数学内容了。直接上结果吧。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/03.png)
```python
# 前后向传播过程
def fbp(w, b, x_train, y_train):
    # 前向传播
    z = np.dot(w.T, x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head) - (1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[1]
    # 后向传播过程
    dw = (np.dot(x_train, ((y_head-y_train).T)))/x_train.shape[1]
    db = np.sum(y_head-y_train)/x_train.shape[1]
    gradients = {"dw":dw, "db":db}
    return cost, gradients
```

下面更新参数。
```python
# 更新参数
def update(w, b, x_train, y_train, learning_rate, number_of_iteration):
    cost_list = []
    cost_list2 = []
    index = []
    # 更新(学习)
    for i in range(number_of_iteration):
        cost, gradients = fbp(w, b, x_train, y_train)
        cost_list.append(cost)
        # 更新
        w = w - learning_rate * gradients["dw"]
        b = b - learning_rate * gradients["db"]
        if i % 10 == 0:
            cost_list2 .append(cost)
            index.append(i)
            print("第%i次迭代后的成本:%f" % (i, cost))
        
    parameters = {"weight":w, "bias":b}
    plt.plot(index, cost_list2)
    plt.savefig("./output/learning_curve.png")
    return parameters, gradients, cost_list
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/04.png)
下面进行预测。
```python
# 进行预测
def predict(w, b, x_test):
    z = sigmoid(np.dot(w.T, x_test)+b)
    Y_prediction = np.zeros((1, x_test.shape[1]))
    for i in range(z.shape[1]):
        if z[0, i] <= 0.5:
            Y_prediction[0, i] = 0
        else:
            Y_prediction[0, i] = 1
           
    return Y_prediction
```

最后用测试数据进行预测。
```python
    # 进行预测
    y_pred_test = predict(parameters["weight"], parameters["bias"], x_test)
    y_pred_train = predict(parameters["weight"], parameters["bias"], x_train)
    # 计算准确率
    train_accuracy = 100 - np.mean(np.abs(y_pred_train - y_train))*100
    test_accuracy = 100 - np.mean(np.abs(y_pred_test - y_test))*100
    print("训练集预测准确率%f" % (train_accuracy))
    print("测试集预测准确率%f" % (test_accuracy))
训练集的准确率为93.68%，测试集的准确率为95.16%。
    # 用sklearn进行
    from sklearn import linear_model
    logreg = linear_model.LogisticRegression(random_state = 42, max_iter = 150)
    print("sklearn算法")
    print("训练集预测准确率%f" % (logreg.fit(x_train.T, y_train.T).score(x_train.T, y_train.T)))
    print("测试集预测准确率%f" % (logreg.fit(x_train.T, y_train.T).score(x_test.T, y_test.T)))
```
准确率分别为100%和96.8%。


人工神经网络(Artificial Neural Network, ANN)
又称深度神经网络(deep neural network）或深度学习(deep learning)。最基础的人工神经网络为将逻辑回归进行至少两次。在逻辑回归中，只有输入层和输出层，而在神经网络中，有至少一个隐藏层在输入层和输出层之间。“深度(deep)”是隐藏层的层数很多，有多少是一个相对的概念，随着硬件的发展不断增加。“隐藏”的意思是它们不能直接看到输入的训练数据。
如下图，有一个隐藏层，这样的神经网络有2层，在计算层数的时候输入层被忽略。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/05.jpg)
隐藏层有3个节点，数量的选择是随意的，没有理由。节点的数量就像学习率一样，是一个超参数。输入和输出层的情况和逻辑回归中一样。其中用到了tanh函数，用作激活函数，比sigmoid产生的输出更加集中。它还能增加非线性，使得模型学习得更好。隐藏层是输入层的输出，是输出层的输入。
下面就来具体研究2层神经网络。
层数和参数的初始化。
将权重初始化为0.01，偏差为0。
```python
# 初始化参数和层数
def init_nn_parameters(x_train, y_train):
    parameters = {
        "weight1" : np.random.randn(3, x_train.shape[0])*0.1,
        "bias1" : np.zeros((3, 1)),
        "weight2" : np.random.randn(y_train.shape[0], 3)*0.1,
        "bias2" : np.zeros((y_train.shape[0], 1))
    }
    return parameters
```
前向传播过程与逻辑回归基本一样，唯一的不同采用tanh函数，进行两次。
```python
# 神经网络前向传播过程
def fp_NN(x_train, parameters):
    Z1 = np.dot(parameters["weight1"], x_train) + parameters["bias1"]
    A1 = np.tanh(Z1)
    Z2 = np.dot(parameters["weight2"], A1) + parameters["bias2"]
    A2 = sigmoid(Z2)
   
    cache = {
        "Z1" : Z1,
        "A1" : A1,
        "Z2" : Z2,
        "A2" : A2
    }


    return A2, cache
```
损失函数跟逻辑回归一样，用交叉熵函数。

```python
# 神经网络的损失函数
def cost_NN(A2, Y, parameters):
    logprobs = np.multiply(np.log(A2), Y)
    cost = -np.sum(logprobs)/Y.shape[1]
    return cost
```

后向传播过程，即意味着求导。要了解数学内容，去看其它材料吧。逻辑跟逻辑回归是一样的。

```python
# 神经网络后向传播过程
def bp_NN(parameters, cache, X, Y):
    dZ2 = cache["A2"] - Y
    dW2 = np.dot(dZ2, cache["A1"].T)/X.shape[1]
    db2 = np.sum(dZ2, axis = 1, keepdims = True)/X.shape[1]
    dZ1 = np.dot(parameters["weight2"].T, dZ2)*(1-np.power(cache["A1"], 2))
    dW1 = np.dot(dZ1, X.T)/X.shape[1]
    db1 = np.sum(dZ1, axis = 1, keepdims = True)/X.shape[1]
    grads = {
        "dweight1" : dW1,
        "dbias1" : db1,
        "dweight2" : dW2,
        "dbias2" : db2
    }
    return grads
```

更新参数，跟逻辑回归里一样的。
```python
# 更新神经网络参数
def update_NN(parameters, grads, learning_rate = 0.01):
    parameters = {
        "weight1" : parameters["weight1"] - learning_rate*grads["dweight1"],
        "bias1" : parameters["bias1"] - learning_rate*grads["dbias1"],
        "weight2" : parameters["weight2"] - learning_rate*grads["dweight2"],
        "bias2" : parameters["bias2"] - learning_rate*grads["dbias2"]
    }
    return parameters
```

进行预测
```python
# 进行预测
def predict_NN(parameters, x_test):
    A2, cache = fp_NN(x_test, parameters)
    Y_pred = np.zeros((1, x_test.shape[1]))
    for i in range(A2.shape[1]):
        if A2[0, i] <= 0.5:
            Y_pred[0, i] = 0
        else:
            Y_pred[0, i] = 1
            
    return Y_pred
```

最后，建立神经网络
```python
# 建立两层神经网络
def NN(x_train, y_train, x_test, y_test, num_iterations):
    cost_list = []
    index_list = []
    # 初始化参数
    parameters = init_nn_parameters(x_train, y_train)
    
    for i in range(0, num_iterations):
        A2, cache = fp_NN(x_train, parameters)
        cost = cost_NN(A2, y_train, parameters)
        grads = bp_NN(parameters, cache, x_train, y_train)
        parameters = update_NN(parameters, grads)
        
        if i % 100 == 0:
            cost_list.append(cost)
            index_list.append(i)
            print("第%i次迭代后的成本:%f" % (i, cost))
    
    plt.figure()
    plt.plot(index_list, cost_list)
    plt.savefig("NN_LC.png")
    plt.close()
    # 进行预测
    y_pred_test = predict_NN(parameters, x_test)
    y_pred_train = predict_NN(parameters, x_train)
    # 计算准确率
    train_accuracy = 100 - np.mean(np.abs(y_pred_train - y_train))*100
    test_accuracy = 100 - np.mean(np.abs(y_pred_test - y_test))*100
    print("训练集预测准确率%f" % (train_accuracy))
    print("测试集预测准确率%f" % (test_accuracy))
```

最后，看结果。
```python
parameters = NN(x_train, y_train, x_test, y_test, num_iterations = 2500)
```
训练集预测准确率100.000000
测试集预测准确率95.161290
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/06.png)

不比逻辑回归好啊？
L层神经网络(L layer neural network)
当隐藏层数量增加是，它能探测到更复杂的特征。
有许多超参数需要我们选择，如学习率，隐藏层层数，迭代次数，激活函数类型等。
用keras实现L层神经网络，老调不对，先摆着，看第二篇文章，讲pytorch的。
https://www.kaggle.com/kanncaa1/pytorch-tutorial-for-deep-learning-lovers
pytorch是numpy的替代品，可以充分利用GPU的运算能力，是一个深度学习研究平台，提供了最大程度的扩展性和速度。
Pytorch基础
在pytorch中，矩阵（数组）被称为张量(tensors)。
先看numpy数组的例子
```python
# numpy数组
def numpy_array():
    array = [[1, 2, 3], [4, 5, 6]]
    first_array = np.array(array)
    print(type(first_array))
    print(np.shape(first_array))
    print(first_array)
```
```python
<class 'numpy.ndarray'>
(2, 3)
[[1 2 3]
[4 5 6]]
```
下面看张量
```python
import torch
# 张量
def pytorch_tensor(array):
    tensor = torch.Tensor(array)
    print(tensor.type)
    print(tensor.shape)
    print(tensor)
```
```python
<built-in method type of Tensor object at 0x7f555a14b690>
torch.Size([2, 3])
tensor([[1., 2., 3.],
        [4., 5., 6.]])
```

张量与numpy数组的转换
```python
# 张量与数组的转换
def transform():
    array = np.random.rand(2, 2)
    print("{} {}\n".format(type(array), array))
    
    from_numpy_to_tensor = torch.from_numpy(array)
    print("{}\n".format(from_numpy_to_tensor))
    
    tensor = from_numpy_to_tensor
    from_tensor_to_numpy = tensor.numpy()
    print("{} {}\n".format(type(from_tensor_to_numpy), from_tensor_to_numpy))
```
```python
<class 'numpy.ndarray'> [[0.22831416 0.2857514 ]
[0.26072294 0.01614062]]


tensor([[0.2283, 0.2858],
        [0.2607, 0.0161]], dtype=torch.float64)


<class 'numpy.ndarray'> [[0.22831416 0.2857514 ]
[0.26072294 0.01614062]]
```

pytorch基础数学
```python
# 基础数学
def basic_math():
    # 创建tensor
    tensor = torch.ones(3, 3)
    print("\n", tensor)
    # 改变大小
    print("{}{}\n".format(tensor.view(9).shape, tensor.view(9)))
    # 加
    print("加:{}\n".format(torch.add(tensor, tensor)))
    # 减
    print("减:{}\n".format(tensor.sub(tensor)))
    # 乘
    print("乘:{}\n".format(torch.mul(tensor, tensor)))
    # 除
    print("除:{}\n".format(torch.div(tensor, tensor)))
    # 均值
    tensor = torch.Tensor([1, 2, 3, 4, 5])
    print("均值:{}".format(tensor.mean()))
    # 均值
    print("标准差:{}".format(tensor.std()))
```
```python
tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]])
torch.Size([9])tensor([1., 1., 1., 1., 1., 1., 1., 1., 1.])


加:tensor([[2., 2., 2.],
        [2., 2., 2.],
        [2., 2., 2.]])


减:tensor([[0., 0., 0.],
        [0., 0., 0.],
        [0., 0., 0.]])


乘:tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]])


除:tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]])


均值:3.0
标准差:1.5811388492584229
```

变量(Variables)
它能积累梯度。在神经网络的反向传播过程中，我们将计算梯度。因此我们需要处理梯度。变量与张量的区别是变量能够自动累积梯度。变量同样的也能进行那些数学运算。为了完成反向传播我们需要变量。
假设我们有方程y = x^2，定义变量x = [2,4]，计算后我们发现y = [4,16]，Recap o方程（Recap o equation，不知道咋翻）是o = (1/2)sum(y) = (1/2)sum(x^2)，o的导数为o = x，因此梯度为[2,4]。下面用程序来实现。

```python
from torch.autograd import Variable
# 求y = x^2 在x = [2, 4]的梯度
def grad():
    var = Variable(torch.ones(3), requires_grad = True)
    print(var)
    array = [2, 4]
    tensor = torch.Tensor(array)
    x = Variable(tensor, requires_grad = True)
    y = x**2
    print("y=", y)
   
    o = (1/2)*sum(y)
    print("o=", o)
   
    # 反向传播
    o.backward()
   
    print("梯度:", x.grad)
```
```python
tensor([1., 1., 1.], requires_grad=True)
y= tensor([ 4., 16.], grad_fn=<PowBackward0>)
o= tensor(10., grad_fn=<MulBackward0>)
梯度: tensor([2., 4.])
```

线性回归
y = Ax + B，A为直线斜率，B为偏差值（y截距）。
一个例子：车的价格和销量。
先初始化数据，画图看看。
```python
# 线性回归的例子
def linear_regress():
    # 车价
    car_prices_array = [3, 4, 5, 6, 7, 8, 9]
    car_price_np = np.array(car_prices_array, dtype = np.float32)
    car_price_np = car_price_np.reshape(-1, 1)
    car_price_tensor = Variable(torch.from_numpy(car_price_np))
    # 车销量
    number_of_car_sell_array = [7.5, 7, 6.5, 6.0, 5.5, 5.0, 4.5]
    number_of_car_sell_np = np.array(number_of_car_sell_array, dtype = np.float32)
    number_of_car_sell_np = number_of_car_sell_np.reshape(-1, 1)
    number_of_car_sell_tensor = Variable(torch.from_numpy(number_of_car_sell_np))
    # 可视化
    plt.figure()
    plt.scatter(car_prices_array, number_of_car_sell_array)
    plt.savefig("./output/price_sell.png")
```

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/07.png)

现在要问当车价为100时的销量。用线性回归来解决。要用直线来拟合这些数据，目标是误差最小。
线性回归的步骤：
①创建线性回归类。
②从线性回归类定义模型。
③计算MSE：平均误差平方（Mean Squared Error）
④优化SGD:随机梯度下降（Stochastic Gradient Descent）
⑤反向传播过程。
⑥预测。
下面用Pytorch实现。
```python
    class LinearRegression(nn.Module):
        def __init__(self, input_size, output_size):
            super(LinearRegression, self).__init__()
            self.linear = nn.Linear(input_size, output_size)
       
        def forward(self, x):
            return self.linear(x)
           
    input_dim = 1
    output_dim = 1
    model = LinearRegression(input_dim, output_dim)
    loss_fn = nn.MSELoss()
   
    # 优化器
    learning_rate = 0.02
    optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate)
   
    # 训练模型
    loss_list = []
    iteration_number = 1001
    for iteration in range(iteration_number):
        # 优化
        optimizer.zero_grad()
        # 前向传播获得输出
        results = model(car_price_tensor)
        # 计算损失
        loss = loss_fn(results, number_of_car_sell_tensor)
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 保存损失值
        loss_list.append(loss.data)
        # 打印损失值
        if iteration % 50 == 0:
            print("epoch {}, loss {}".format(iteration, loss.data))
           
    # 画图
    plt.figure()
    plt.plot(range(iteration_number), loss_list)
    plt.savefig("./output/lr_curve.png")
```

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/08.png)

进行了1001次迭代。在1000次迭代后，损失接近为0。现在进行预测。
```python
    # 进行预测
    predicted = model(car_price_tensor).data.numpy()
    plt.figure()
    plt.scatter(car_prices_array, number_of_car_sell_array, color = "red")
    plt.scatter(car_prices_array, predicted, color = "blue")
    plt.savefig("./output/result.png")
    plt.close()
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/09.png)

逻辑回归
对于分类问题，线性回归表现并不好。
线性回归+逻辑方程(softmax)=逻辑回归。
步骤:
①导入库。
②准备数据，采用MNIST，是一些标记为0-9十个数字的28×28的图片，把其转换为一维的256个数据，划分为训练集和测试集，创建tensor变量。batch_size的意思:例如我们有1000个样本，可以把1000个样本拿到一起训练，也可以把样本划分为10组，每组100个样本，依次进行10次训练。batch_size是每组的样本量，在这个例子中，等于100。确定迭代次数(epoch)，即把所有样本训练一次。在本例中，有33600个样本，训练一次要训练33600个样本，分成了336组，进行29次迭代，一共的迭代次数是9744次(接近10000次)。使用TensorDataset()封装数据。DataLoader()将数据和样本结合到一起，也提供了对数据的并行迭代功能。将数据可视化。
③创建逻辑回归模型。
④实例化模型。
输入维度2828， 输出维度10。
⑤计算损失，采用交叉熵(Cross entropy loss)。
⑥定义优化器，采用SGD优化器。
⑦训练模型。
⑧预测。


程序调不对，用[另一个](https://blog.csdn.net/a946971688/article/details/89671885)
```python
# 逻辑回归的例子
def logistic_regress2():
    import torch
    import torch.nn as nn
    import torchvision
    import torchvision.transforms as transforms
    from torchvision.datasets import MNIST
    
    # 定义超参数
    input_size = 784    #输入层神经元大小
    num_classes = 10 #图像类别
    num_epochs = 25  #迭代次数
    batch_size = 100   #每次训练取得样本数
    learning_rate = 0.05 #学习率
    
    # 加载数据
    train_dataset = torchvision.datasets.MNIST(root='./', train=True, transform=transforms.ToTensor(), download=True)
    test_dataset = torchvision.datasets.MNIST(root='./', train=False, transform=transforms.ToTensor(), download=True)
    
    # 创建dataloader
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)
    
    # 创建模型
    model = nn.Linear(input_size, num_classes)
    
    # 损失函数和优化器
    loss_fn = nn.CrossEntropyLoss()#交叉熵损失函数
    optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate)
    # 训练模型
    loss_list = []
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # 将数据变换为[每批大小, 图像大小]
            images = images.reshape(-1, 28*28)
            
            # 前向传播
            outputs = model(images)
            loss = loss_fn(outputs, labels)
            loss_list.append(loss)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if (i+1) % 100 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' .format(epoch+1, num_epochs, i+1, total_step, loss.item()))
                
    plt.figure()
    plt.plot(loss_list)
    plt.savefig("./output/lr_loss.png")
    plt.close()
                
    # 测试
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.reshape(-1, 28*28)
            outputs = model(images)
            _, pred = torch.max(outputs.data, 1)
            total += labels.size()[0]
            correct += (pred == labels).sum()
            
        print("模型预测准确率{}%".format(100*correct.item()/total))
```
模型准确率92%。


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/10.png)

人工神经网络(Artificial Neural Network, ANN)
逻辑回归处理分类问题很好，但当复杂性(非线性)增加时，模型准确性下降。为了增加模型的复杂性，需要增加更多的非线性函数的隐藏层。
具体步骤:
①导入库。
②准备数据。
③创建ANN模型:增加三个隐藏层，用ReLU, Tanh和ELU做为激活函数。
④实例化模型。隐藏层维度150，随便选的。这也是超参数之一。
⑤选择损失函数，跟逻辑回归一样。
⑥优化器也一样。
⑦训练模型。
⑧预测。
```python
# 人工神经网络
def ANN():
    import torch
    import torch.nn as nn
    from torch.autograd import Variable
    from torch.utils.data import DataLoader
    import pandas as pd
    from sklearn.model_selection import train_test_split
    import os
    import torchvision
    import torchvision.transforms as transforms
    from torchvision.datasets import MNIST
    
    print("ANN\n")
    # print(os.getcwd())
    # 加载数据
    train_dataset = torchvision.datasets.MNIST(root='./', train=True, transform=transforms.ToTensor(), download=True)
    test_dataset = torchvision.datasets.MNIST(root='./', train=False, transform=transforms.ToTensor(), download=True)
    
    # 定义超参数
    batch_size = 100
    num_epochs = 100
    
    # 创建dataloader
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)


    
    # 定义模型
    class ANNModel(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(ANNModel, self).__init__()
            # 第一层 784->150
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            # 非线性成分
            self.relu1 = nn.ReLU()
            # 第二层 150-150
            self.fc2 = nn.Linear(hidden_dim, hidden_dim)
            # 非线性成分
            self.tanh2 = nn.Tanh()
            # 第三层 150-150
            self.fc3 = nn.Linear(hidden_dim, hidden_dim)
            # 非线性成分
            self.elu3 = nn.ELU()
            # 第四层 150-10
            self.fc4 = nn.Linear(hidden_dim, output_dim)
            
        # 前向传播
        def forward(self, x):
            out = self.fc1(x)
            out = self.relu1(out)
            out = self.fc2(out)
            out = self.tanh2(out)
            out = self.fc3(out)
            out = self.elu3(out)
            out = self.fc4(out)
            
            return out
            
    # 初始化ANN
    input_dim = 28*28
    hidden_dim = 150 # 这个可以调参的
    output_dim = 10
    
    # 创建ANN
    model = ANNModel(input_dim, hidden_dim, output_dim)
    
    # 超参数
    loss_fn = nn.CrossEntropyLoss()
    learning_rate = 0.02
    optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate) 
    
    # 训练ANN
    count = 0
    loss_list = []
    iteration_list = []
    accuracy_list = []
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            # print(epoch, i)
            train = images.reshape(-1, 28*28)
            labels = Variable(labels)
            # 梯度清零
            optimizer.zero_grad()
            # 前向过程
            outputs = model(train)
            # 计算损失
            loss = loss_fn(outputs, labels)
            # 计算梯度
            loss.backward()
            # 更新参数
            optimizer.step()
            
            count += 1
            if count % 50 == 0:
                # 计算准确率
                correct = 0
                total = 0
                for images, labels in test_loader:
                    test = images.reshape(-1, 28*28)
                    outputs = model(test)
                    pred = torch.max(outputs.data, 1)[1]
                    total += len(labels)
                    correct += (pred == labels).sum()
                    accuracy = 100*correct/float(total)
                loss_list.append(loss.data)
                iteration_list.append(count)
                accuracy_list.append(accuracy)
            if count % 500 == 0:
                print('迭代次数: {}  损失: {}  准确率: {} %'.format(count, loss.data, accuracy))
    
    # 结果可视化
    plt.figure()
    plt.plot(iteration_list,loss_list)
    plt.title("ANN loss")
    plt.savefig("./output/ANN_loss.png")
    plt.figure()
    plt.plot(iteration_list,accuracy_list,color = "red")
    plt.title("ANN accuracy")
    plt.savefig("./output/ANN_accuracy.png")
    plt.close()
```
结果，正确率97.8%，花了大概一小时。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/11.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0234-dp/12.png)

还有卷积神经网络，图像处理用得比较多，先pass了。
总结一下，机器学习也好，深度学习也好，其实质都是拟合数据，拟合的方法(模型)不一样而已。用已知数据训练模型(求出一组参数)，然后用模型对未知数据做出预测。深度学习的模型是神经网络，由神经节组成。每个神经节接受若干输入，经过激活函数(通常为非线性函数，以拟合非线性关系)，产生一个输出。若干个神经节形成一层，前一层的输出作为下一层的输入，一直向前传递直到输出层。用输出结果与真实值对比(用损失函数)计算出损失值(前向传播)。接着，用梯度下降的方法沿着路径反向计算使损失值最小的参数，并更新参数(反向传播)。上述步骤重复若干次，损失值和预测准确率收敛到一定程度，即停止训练，运用模型进行预测。
整个过程，pytorch等框架为我们做了什么呢？数据准备(tensor，便于GPU运算; Variable，自动进行梯度运算并保存结果;dataLoader，便于分组训练)、定义模型(nn.Module，定义神经网络结构，定义前向传播过程，计算出输出值)、进行训练(Optimizer，梯度清零，更新参数;model，前向传播过程，计算输出值;提供损失函数:计算损失值，反向传播过程:backward)。其中核心是自动求导的过程。tensorflow我没了解过，应该也差不多。
这几天听了一个自己实现深度网络框架的课，正在整理笔记，下次奉上。
本文[代码](https://github.com/zwdnet/JSMPwork/blob/main/DP.py)




我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)