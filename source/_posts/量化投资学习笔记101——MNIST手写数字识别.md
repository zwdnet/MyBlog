---
title: 量化投资学习笔记101——MNIST手写数字识别
date: 2021-02-25 07:10:11
tags: [量化投资,机器学习,深度学习,MNIST,pytorch,学习笔记]        
categories: 量化投资
---

MNIST是一个开源手写数字(0-9共10个数字)图片数据集，格式为28×28大小的图片灰度值。有60000个训练数据和10000个测试数据。标记值为图片所写的数字。任务是用计算机程序来读取图片数据灰度值，判断所写的数字。就尝试用各种方法来解决这个问题。
导入需要的库
```python
import torch
import torch.nn as nn
from torchvision.datasets import MNIST
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
import torch.utils.data as Data
from torchsummary import summary
import numpy as np
import pandas as pd
import os
# run是用于在服务器上运行代码的工具，
# 如果你在本地运行，可以把所有@run.change_dir等装饰器删掉
import run  
import copy
import tqdm
import matplotlib.pyplot as plt
import joblib


from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from skimage import io,data,transform
```
首先下载数据，用torchvision下载。
```python
# 下载并加载数据
@run.change_dir
def loadData(batch_size = 64):
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    mnist_train = MNIST(os.getcwd(), train=True, download=True, transform=transform)
    mnist_test = MNIST(os.getcwd(), train=False, download=True, transform=transform)
    
    mnist_train, mnist_val = random_split(mnist_train, [55000, 5000])
    
    # 创建 DataLoader
    mnist_train = DataLoader(mnist_train, batch_size)
    mnist_val = DataLoader(mnist_val, batch_size)
    mnist_test = DataLoader(mnist_test, batch_size)
    
    return mnist_train, mnist_val, mnist_test
```
因为还要使用sklearn里的一些算法，还需要numpy.array的数据，自己写了个转换程序，用的最笨的办法。
```python
# 将DataLoader数据转换为numpy数组
def Loader2numpy(Loader):
    X = []
    Y = []
    for x, y in Loader:
        for i in x:
            i = i.view(1, -1).detach().numpy()
            # print("测试", i.shape)
            X.append(i[0])
        for j in y.detach().numpy():
            Y.append(j)
    return np.array(X), np.array(Y)
```
然后在主程序里调用。
```python
if __name__ == "__main__":
    torch.manual_seed(666)
    mnist_train, mnist_val, mnist_test = loadData()
    X_train, Y_train = Loader2numpy(mnist_train)
    X_val, Y_val = Loader2numpy(mnist_val)
    X_test, Y_test = Loader2numpy(mnist_test)
    # 合并训练集和验证集
    X_train = np.concatenate((X_train, X_val), axis = 0)
    Y_train = np.concatenate((Y_train, Y_val), axis = 0)
```
这样数据就准备好了。在为sklearn准备的数据里把训练集和验证集又合并了，因为它可能有自己的划分方式。
先试试最简单的算法:随机瞎猜
```python
# 算法1:随机算法
@run.timethis
def Random_Model(X_train, Y_train, X_test, Y_test):
    y_pred = np.random.randint(low = 0, high = 10, size = Y_test.shape[0])
    acc = accuracy(y_pred, Y_test)
    print("随机算法预测准确率:{}".format(acc))
    return acc
```
结果当然是准确率10%左右了。
```python
算法1:瞎猜                                                    
随机算法预测率:0.1032                                     __main__.Random_Model的运行时间为 : 0.0015346029977081344秒
```
下面尝试机器学习算法。
逻辑回归
[参考:]( https://blog.csdn.net/u011734144/article/details/79717470)
本来逻辑回归只能用于二分类问题，但可以用"one vs rest"方法(即下文模型定义中的"ovr"，将某类与其余类别做为两类，分别进行逻辑回归，取概率最大的分类作为预测结果。
```python
# 算法2:逻辑回归
@run.timethis
def LogisticRegression_Model(X_train, Y_train, X_test, Y_test):
    lor = LogisticRegression(C=100,multi_class='ovr')
    # 训练模型
    lor.fit(X_train,Y_train)
    # score = lor.score(X_std_test, Y_test)
    y_pred = lor.predict(X_test)
    acc = accuracy(y_pred, Y_test)
    print("逻辑回归算法预测准确率:{}".format(acc))
    return acc
```
结果:
```python
算法2:逻辑回归                                               
逻辑回归算法预测准确率:0.9169
__main__.LogisticRegression_Model的运行时间为 : 156.33382360900578
```
准确率达到91.69%，突破90%了。但时间也用了两分多钟。
朴素贝叶斯算法
[参考:]( https://www.cnblogs.com/pinard/p/6074222.html)
```python
# 算法3:朴素贝叶斯
@run.timethis
def Bayes_Model(X_train, Y_train, X_test, Y_test):
    clf = GaussianNB()
    clf.fit(X_train, Y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy(y_pred, Y_test)
    print("朴素贝叶斯算法预测准确率:{}".format(acc))
    return acc
```
结果
```python
算法3:朴素贝叶斯
朴素贝叶斯算法预测准确率:0.556 __main__.Bayes_Model的运行时间为 : 1.8668527510017157
```
准确率55.6%，不过时间只要1.8秒。
支持向量机
[参考:]( https://zhuanlan.zhihu.com/p/42334376)
```python
# 算法4:支持向量机
@run.timethis
def SVM_Model(X_train, Y_train, X_test, Y_test):
    model = SVC()
    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)
    acc = accuracy(y_pred, Y_test)
    print("支持向量机算法预测准确率:{}".format(acc))
    return acc
```
结果
```python
算法4:支持向量机 
支持向量机算法预测准确率:0.9792 __main__.SVM_Model的运行时间为 : 1482.80279673099秒
```
一开始照那篇文章里的用LinearSVC，结果提示有"段错误"，调了半天都不行。于是改用SVC，时间最长，二十多分钟，准确率也最高，近98%。
下面试试knn算法。
算法5:KNN算法 
```python
 KNN算法预测准确率:0.9688 __main__.KNN_Model的运行时间为 : 1802.849214115995
```
用时半小时，准确率目前第二高，96.8%。
接下来，随机森林。
```python
# 算法6:随机森林
@run.timethis
def RF_Model(X_train, Y_train, X_test, Y_test):
    model = RandomForestClassifier()
    model.fit(X_train, Y_train)
    y_pred = model.predict(X_test)
    acc = accuracy(y_pred, Y_test)
    print("随机森林算法预测准确率:{}".format(acc))
    return acc
```
结果
```python
算法6:随机森林算法 
 随机森林算法预测准确率:0.97 __main__.RF_Model的运行时间为 : 127.43228440599341秒
```
准确率97%，训练时间两分钟。这个也比较好。
接下来用深度学习。
先用一般的神经网络。
[参考:](https://www.jianshu.com/p/43478538bbc6)
```python
# 算法7:一般神经网络
class fc_net(nn.Module):
    def __init__(self, batch_size = 64):
        super(fc_net, self).__init__()
        self.layer_1 = nn.Linear(28*28, 200)
        self.layer_2 = nn.Linear(200, 100)
        self.layer_3 = nn.Linear(100, 20)
        self.layer_4 = nn.Linear(20, 10)
        self.batch_size = batch_size
       
    def forward(self, x):
        x = self.layer_1(x)
        nn.ReLU()
        x = self.layer_2(x)
        nn.ReLU()
        x = self.layer_3(x)
        nn.ReLU()
        x = self.layer_4(x)

        return x
   

@run.change_dir
@run.timethis
def NN_Model(mnist_train, mnist_val, mnist_test, batch_size = 64, lr = 0.001):
    epochs = 20
    net = fc_net(batch_size)
    criterion = nn.CrossEntropyLoss()
    optim = torch.optim.Adam(net.parameters(), lr = lr, weight_decay=0.0)
    print(batch_size)
   
    for epoch in range(epochs):
        # 训练过程
        train_loss = []
        for x, y in mnist_train:
            #print(x.shape)
            x = x.view(batch_size, -1)
            y_pred = net.forward(x)
            loss = criterion(y_pred, y)
            train_loss.append(loss.item())
            optim.zero_grad()
            loss.backward()
            optim.step()
        mean_train_loss = torch.mean(torch.tensor(train_loss))
        # 验证过程
        with torch.no_grad():
            val_loss = []
            for x, y in mnist_val:
                x = x.view(batch_size, -1)
                y_pred = net.forward(x)
                # y_pred = torch.max(y_pred.data, 1).indices
                loss = criterion(y_pred, y)
                val_loss.append(loss.item())
            mean_val_loss = torch.mean(torch.tensor(val_loss))
        print("第{}次迭代，训练集平均损失{}，验证集平均损失{}".format(epoch, mean_train_loss, mean_val_loss))
    # 画损失值曲线
    plt.figure()
    plt.plot(train_loss)
    plt.savefig("./output/NN_train_loss.png")
    plt.close()
    plt.figure()
    plt.plot(val_loss)
    plt.savefig("./output/NN_val_loss.png")
       
    # 用测试数据测试
    test_accuracy = 0
    for x, y in mnist_test:
        x = x.view(batch_size, -1)
        y_pred = net.forward(x)
        y_pred = torch.max(y_pred.data, 1).indices
        test_accuracy += (y_pred == y).sum().item()
        # print(test_accuracy, len(mnist_test)*batch_size)
    accuracy = test_accuracy/(len(mnist_test)*batch_size)
    print("一般神经网络算法预测准确率:{}".format(accuracy))
    return accuracy
```
这里有个坑:batch_size要设置了能整除数据总量，否则最后一个batch的数据量与之前的batch不一样，会报错。我调了好久才发现。
迭代20次，最后结果:
```python
一般神经网络算法预测准确率:0.9258
__main__.NN_Model的运行时间为 : 655.4456413289881秒
```
时间很长，但最后结果还不如随机森林呢。
再来试试其它神经网络模型。
卷积神经网络以前只是知道个名称，没仔细了解过，写详细一点。
先看原理，看这两个视频: [1](https://b23.tv/55a0bN) [2](https://b23.tv/MgmQi0)
全连接神经网络的缺点:网络层次越深，计算量越大，多个神经元输出作为下一级神经元输入时，形成多个复杂的嵌套关系。
卷积神经网络包括输入层(input layer)，卷积层(convolutional layer)，池化层(pooling layer)和输出层(全连接层+softmax layer)。
①总有至少1个卷积层，用以提取特征。
②卷积层级之间的神经元是局部连接和权值共享，这样的设计大大减少了权值的数量，加快了训练。
卷积层是压缩提纯的。卷积核在上一层滑动过程中做卷积运算(卷积核w与其所覆盖的区域的数据进行点积)，结果映射到卷积层。
池化层对卷积层输出的特征图进一步特征抽样，池化层主要分为最大池化(max polling)和平均池化(average polling)。即选取池化区域的最大值/平均值作为池化层的输出。
最后输出层用softmax层使得所有输出的概率总和为1。
超参数设置
padding，保持边界信息。
stride步幅，卷积核滑动幅度，默认为1。
下面代码撸起来，参考[这个项目:]( https://github.com/liamlycoder/PyTorch_Primer/tree/master/PyTorch_Primer/05CNNonMNIST)
```python
# 算法8:卷积神经网络
# 需要将数据转换成二维图片形式
class conv_net(nn.Module):
    def __init__(self):
        super(conv_net, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 25, kernel_size = 3),
            nn.BatchNorm2d(25),
            nn.ReLU(inplace = True)
        )
        self.layer2 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(25, 50, kernel_size = 3),
            nn.BatchNorm2d(50),
            nn.ReLU(inplace = True)
        )
        self.layer4 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Sequential(
            nn.Linear(50*5*5, 1024),
            nn.ReLU(inplace = True),
            nn.Linear(1024, 128),
            nn.ReLU(inplace = True),
            nn.Linear(128, 10)
        )
       
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
   
   
@run.change_dir
@run.timethis
def CONV_Model(mnist_train, mnist_val, mnist_test, batch_size = 64, lr = 0.001):
    epochs = 20
    net = conv_net()
    criterion = nn.CrossEntropyLoss()
    optim = torch.optim.Adam(net.parameters(), lr = lr, weight_decay=0.0)
    # print(batch_size)
   
    net.train()
    for epoch in tqdm.tqdm(range(epochs)):
        # 训练过程
        train_loss = []
        accuracy = 0.0
        train_accuracy = []
        for x, y in mnist_train:
            y_pred = net.forward(x)
            loss = criterion(y_pred, y)
            train_loss.append(loss.item())
            optim.zero_grad()
            loss.backward()
            optim.step()
            # 计算预测准确率
            with torch.no_grad():
                y_pred = torch.max(y_pred.data, 1).indices
                accuracy += (y_pred == y).sum().item()
        train_accuracy.append(accuracy/(len(mnist_train)*batch_size))
        mean_train_loss = torch.mean(torch.tensor(train_loss))
        # 验证过程
        with torch.no_grad():
            val_loss = []
            accuracy = 0.0
            val_accuracy = []
            for x, y in mnist_val:
                # x = x.view(batch_size, -1)
                y_pred = net.forward(x)
                # y_pred = torch.max(y_pred.data, 1).indices
                loss = criterion(y_pred, y)
                val_loss.append(loss.item())
                # 计算预测准确率
                y_pred = torch.max(y_pred.data, 1).indices
                accuracy += (y_pred == y).sum().item()
            val_accuracy.append(accuracy/(len(mnist_val)*batch_size))
            mean_val_loss = torch.mean(torch.tensor(val_loss))
        print("第{}次迭代，训练集平均损失{}，预测准确率{}，验证集平均损失{}，预测准确率{}".format(epoch, mean_train_loss, train_accuracy[-1], mean_val_loss, val_accuracy[-1]))
    # 画损失值曲线和正确率曲线
    plt.figure()
    plt.plot(train_loss)
    plt.savefig("./output/CONV_train_loss.png")
    plt.close()
    plt.figure()
    plt.plot(val_loss)
    plt.savefig("./output/CONV_val_loss.png")
    plt.figure()
    plt.plot(train_accuracy)
    plt.savefig("./output/CONV_train_accuracy.png")
    plt.close()
    plt.figure()
    plt.plot(val_accuracy)
    plt.savefig("./output/CONV_val_accuracy.png")
       
    # 用测试数据测试
    net.eval()
    test_accuracy = 0
    for x, y in mnist_test:
        # x = x.view(batch_size, -1)
        y_pred = net.forward(x)
        y_pred = torch.max(y_pred.data, 1).indices
        test_accuracy += (y_pred == y).sum().item()
        # print(test_accuracy, len(mnist_test)*batch_size)
    accuracy = test_accuracy/(len(mnist_test)*batch_size)
    print("卷积神经网络算法预测准确率:{}".format(accuracy))
    return accuracy
```
迭代20次，运行结果:
```python
,随机算法,逻辑回归算法,朴素贝叶斯算法,支持向量机算法,随机森林算法,一般神经网络算法,卷积神经网络算法
0,0.0979,0.9194,0.556,0.9688,0.9701,0.9258,0.9886
```python
卷积网络模型运行时间最长，准确率也最高。但似乎迭代两次跟迭代20次差别不大?
不管了，先这样吧，准确率也蛮高了。
现在进行运用，用程序识别新的手写输入数据。先造一个数据，自己写吧。写了100个。
这是原图。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/01.jpg)
这是用手机相机的文档模式拍的黑白图片。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/02.jpg)
下面就是怎么把图片转换成mnist的28×28灰度值格式的问题了。
先用这个在线工具(http://www.zuohaotu.com/cut-image.aspx)把图像分割成100份，然后人肉删除没分割好的图片，比如只有一半数字，或者两个数字分割到一张图片上的情况。
分割以后是这样的
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/03.jpg)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/04.jpg)
文件名用“序号_标签”的形式命名，比如09_9.jpg。接下来就将图片转换成28×28的数据。
照[这里:]( https://blog.csdn.net/qq_40358998/article/details/79281936)
```python
# 将图片文件转换为MNIST数据
@run.change_dir
def changeData(path = "./mynum/num/"):
    # path = "./mynum/num/"
    dir_or_files = os.listdir(path)
    files = []
    for dir_file in os.listdir(path):
        files.append(dir_file)
        
    MNIST_SIZE = 28
    datas = []
    labels = []
    for file in files:
        # 处理图片
        # print(path+files[0])
        # 读入图片并变成灰色
        img = io.imread(path+file, as_gray=True)
        # 缩小到28*28
        translated_img = transform.resize(img, (MNIST_SIZE, MNIST_SIZE))
        # 变成1*784的一维数组
        flatten_img = np.reshape(translated_img, 784)
        # 1代表黑，0代表白
        result = np.array([1 - flatten_img])
        # 提取标签
        labels.append([int(file[-5])])
        datas.append(result)
        print(file)
    datas = np.array(datas)
    labels = np.array(labels)
    return datas, labels
    
    
# 将数据画图看看
@run.change_dir
def drawData(data):
    plt.figure()
    plt.imshow(data.reshape(28, 28))
    plt.savefig("./output/num.png")
    plt.close()
```
根据文件名提取标签，原始图片是这样。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/05.jpg)
转换以后的数据画图是这样
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/06.png)
差不多，还是能看出来的。
下面就开始用模型预测了。先选取准确率最高的机器学习模型随机森林(逻辑回归准确率更高，但随机森林也差不多而且要快得多)和准确率最高的深度学习模型卷积网络模型作为实际工作模型。先用mnist数据进行训练并保存模型。
```python
# 训练要用的模型并保存，一般只运行一次
@run.change_dir
def doTraining():
    # 准备训练数据
    batch_size = 500
    print("准备数据")
    mnist_train, mnist_val, mnist_test = loadData(batch_size)
    X_train, Y_train = Loader2numpy(mnist_train)
    X_val, Y_val = Loader2numpy(mnist_val)
    X_test, Y_test = Loader2numpy(mnist_test)
    # 合并训练集和验证集
    X_train = np.concatenate((X_train, X_val), axis = 0)
    Y_train = np.concatenate((Y_train, Y_val), axis = 0)
   
    # print("a", X_train.shape)
   
    # 训练机器学习的随机森林模型
    print("训练随机森林模型")
    MLmodel = RandomForestClassifier()
    MLmodel.fit(X_train, Y_train)
    # 保存模型
    joblib.dump(MLmodel, "./MLmodel.pkl")
    print("模型保存完毕")
   
    # 训练深度学习卷积网络模型
    print("训练卷积网络模型")
    epochs = 10
    lr = 0.001
    net = conv_net()
    criterion = nn.CrossEntropyLoss()
    optim = torch.optim.Adam(net.parameters(), lr = lr, weight_decay=0.0)
    # print(batch_size)
   
    net.train()
    for epoch in tqdm.tqdm(range(epochs)):
        # 训练过程
        for x, y in mnist_train:
            # print(x.shape)
            # x = x.view(len(x), 28, 28)
            y_pred = net.forward(x)
            loss = criterion(y_pred, y)
            optim.zero_grad()
            loss.backward()
            optim.step()
   
    # 保存模型
    joblib.dump(net, "./DLmodel.pkl")
    print("模型保存完毕")
```
基本跟前面一样，多了保持模型的步骤。
接下来就可以用保存的模型进行识别了，折腾了几天，主要是数据形状不对。
```python
# 实际运用模型来识别手写数据
@run.change_dir
def work(datas, labels):
    # doTraining()
    # 数据转换
    X_test = datas.reshape(-1, 784)
    Y_test = labels
    # 加载模型并对数据进行识别，得到正确率
    # 随机森林模型
    MLmodel = joblib.load("./MLmodel.pkl")
    y_pred = MLmodel.predict(X_test)
    acc = accuracy(y_pred, Y_test)
    print("随机森林算法实际识别准确率:{}".format(acc))
   
    # 数据转换
    batch_size = 2
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    datas = datas.reshape(-1, 28, 28)
    datas = datas.transpose(1,2,0)
    # print("b-1", datas.shape)
    test_data = transform(datas)
    # print("b", test_data.shape)
    #test_datas = torch.from_numpy(datas)
    labels = torch.from_numpy(labels)
    #print("c_1", test_data.size())
#    print("c_1", labels.size())
    testdataset = Data.TensorDataset(test_data, labels)
    testdata = DataLoader(testdataset, batch_size = batch_size, shuffle = False)
   
    #test_data = test_data.view(-1, 1, 28, 28)
#    print("c", test_data.shape)
    DLmodel = joblib.load("./DLmodel.pkl")
   
    DLmodel.eval()
    test_accuracy = 0
    for x, y in testdata:
        x = x.view(batch_size, 1, 28, 28)
        x = torch.tensor(x, dtype=torch.float32)
        y_pred = DLmodel.forward(x)
        y_pred = torch.max(y_pred.data, 1).indices
        test_accuracy += (y_pred == y).sum().item()
        # print(test_accuracy, len(mnist_test)*batch_size)
    dlaccuracy = test_accuracy/(len(testdata)*batch_size)
    print("卷积神经网络算法实际识别准确率:{}".format(dlaccuracy))
```
运行结果:
```python
随机森林算法实际识别准确率:0.10227272727272728                
卷积神经网络算法实际识别准确率:0.11363636363636363
```
我晕，跟瞎猜差不多，虽然CNN要好一点。这就是运用机器学习的难点之一:测试时很好，运用时很差。由于在研究时用的是独立的测试数据测试的，所以首先怀疑是数据的问题。先换黑白图片看看。
```python
随机森林算法实际识别准确率:0.12359550561797752                
卷积神经网络算法实际识别准确率:0.20224719101123595
```
好一点了，尤其CNN模型，准确率提高了近一倍，不过还是很低。
人肉把一些不太好的图片删了，再看看。
```python
随机森林算法实际识别准确率:0.07692307692307693                
卷积神经网络算法实际识别准确率:0.333333333333333
```
到33%了!哈哈。看来得重新整个手写数据试试。
又重新写了一份，110个数字，认真了一点，并且手动在电脑上截图，尽量把数字放到中央。
像这样:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/07.jpg)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/08.png)
数据转换以后画的图是这样:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/09.png)
还是一样的文件命名方法，再试一次。
```python
随机森林算法实际识别准确率:0.16363636363636364
卷积神经网络算法实际识别准确率:0.9
```
随机森林的准确率依然不高，但是卷积神经网络的准确率提高到90%了!哈哈，看来数据才是最重要的!
输出错误的情况看看:
```python
实际数字为8，预测值为6
实际数字为8，预测值为6
实际数字为9，预测值为1
实际数字为9，预测值为1
实际数字为0，预测值为9
实际数字为8，预测值为6
实际数字为4，预测值为8
实际数字为8，预测值为6
实际数字为0，预测值为9
实际数字为0，预测值为9
实际数字为0，预测值为9
```
都是6跟8，9跟0，4跟8，9跟1混淆了。
那能不能再提高的?或者说让模型对数据不那么挑?看看别人做的吧。
找到[一篇:](https://paperswithcode.com/paper/effective-handwritten-digit-recognition-using)
Yellapragada SS Bharadwaj, Rajaram P, Sriram V.P, et al. Effective Handwritten Digit Recognition using Deep Convolution Neural Network. International Journal of Advanced Trends in Computer Science and Engineering, Volume 9 No.2, March -April 2020. https://doi.org/10.30534/ijatcse/2020/66922020
作者声称模型对MNIST训练集的错误率达到低于0.1%，对真实手写数字的识别准确率达到98.5%。这就是我想要的，还有代码实现，可是用的是tensorflow，我没用过，尝试用pytorch实现一下看看吧。
论文里给的模型参数：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/10.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/11.png)

就按这个移植吧。
迭代次数过多会造成过拟合，因此当准确率达到98%时就停止迭代。
用torchsummary.summary输出了一下模型参数，发现跟论文的好像不对。
尝试了半天，终于改了跟论文上的模型参数一模一样了，再跑了试试。
```python
class improve_conv_net(nn.Module):
    def __init__(self, drop_rate = 0.0):
        super(improve_conv_net, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size = 3),
            # nn.BatchNorm2d(32),
            nn.ReLU(inplace = True)
        )
        self.layer2 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size = 3),
            # nn.BatchNorm2d(64),
            nn.ReLU(inplace = True)
        )
        self.layer4 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # nn.Dropout(p = drop_rate),
            nn.Linear(1600, 128),
            # nn.ReLU(inplace = True),
            nn.Linear(128, 10),
            # nn.Softmax()
        )
        
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        # x = x.view(x.size(0), -1)
        # print(x.shape)
        x = self.fc(x)
        return x
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/72/12.jpg)
尝试了半天，预测正确率84.5%……还不如我自己的。把学习率改小，到0.0001试试。正确率80%……
把学习率改回0.001，减少迭代次数(通过限定当验证集的准确率大于一定值——如98%——时停止迭代)，结果:迭代了3次，预测准确率0.8727272727272727。
把学习率再调高10倍到0.01看看。准确率60%，改回去吧。

论文复现就到这儿吧。看来还是模型过拟合了。这是我第一次复现论文中的算法，也没想象中那么难。不是所有文章都是通篇的公式的。
最后，再来自己探索一下能不能再提高一点吧。主要是解决模型过拟合的问题。找了篇[文章:](https://zhuanlan.zhihu.com/p/58903870)
防止模型过拟合的方法之一是正则化(Regularization)，其目的是要同时让经验风险和模型复杂度较小。
正则化的方法之一，是上面的提前结束迭代。下面试试另一个方法:Dropout。它属于模型集成的一种，在训练过程中随机丢弃一部分输入，对应的参数不再更新。
先在最先的位置增加nn.Dropout，概率20%
迭代了六次，识别准确率82.8%。
换到卷积操作之后，迭代四次，识别准确率86.4%。
概率增加到50%看看。准确率还是86.4%，迭代次数减少到4次。
尝试了几次，貌似都没啥用。下面试试参数正则化。
pytorch的optim里实现了L2正则化，先尝试这个，设置weight_decay参数即可。设为0.01，准确率85.5%。
还用改进前的模型跑一下新数据吧。

[本文代码:](https://github.com/zwdnet/mnist/blob/main/mnist.py)

到这里，所有的改进似乎都失败了，还不如我改进以前的预测准确率高。就先到这吧，本文主要是尝试机器学习的运用过程。首先定义问题，考虑能否使用机器学习模型来解决。尝试各个模型，选择有效的，调参。对实际的新数据进行预测，评估结果。如果不满意，再调参或看看其他人是怎么做的。重复这个过程直到满意。这当中的难点，是对训练和测试数据有效的模型和参数，对实际数据未必有效，甚至效果很差。另外，数据的处理似乎比模型的选择以及调参对预测的结果影响更大。



我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
