---
title: 量化投资学习笔记100——kaggle量化投资比赛记录8-LSTM
date: 2021-01-26 12:14:59
tags: [量化投资,kaggle竞赛,深度学习,LSTM,pytorch,学习笔记]         
categories: 量化投资
---
又尝试了一下神经网络，用的两个隐藏层，用optuna调参，结果如下:
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/01.jpg)

用调出来的最佳参数:
{'hide1_dim': 118, 'hide2_dim': 142, 'optimizer': 'Adam', 'lr': 0.0006778517964352916, 'epochs': 110}
提交看看。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/02.jpg)

哈哈，终于不再是零分了！这是用10%的数据调参的。找个GPU服务器用完整数据试试吧。
用kaggle上的GPU来跑调参程序(每周可以用36小时)，跑了八个多小时，近600次。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/03.jpg)

最佳的是第553次，最佳参数:{'hide1_dim': 192, 'hide2_dim': 10, 'optimizer': 'Adam', 'lr': , 'epochs': 192}，用这些参数在kaggle里提交，结果，3270.173分。
下面想试试传说中时间序列数据分析的神器LSTM。找了一圈资料，看了一头雾水。先实操吧，照[这个](https://zhuanlan.zhihu.com/p/104475016)来:
使用正弦函数和余弦函数构造时间序列，构造模型学习正弦函数与余弦函数之间的映射关系，通过输入的正弦函数值来预测余弦函数值。
如果不考虑时间因素，一个正弦输入值对应多个余弦值，如sin(pi/6)=sin(7pi/6)，但cos(pi/6)≠cos(7pi/6)。这种情况，传统神经网络不太适用。
取正弦值作为LSTM的输入，预测余弦函数的值。1个输入神经元，1个输出神经元，16个隐藏神经元。平均绝对误差(LMSE)作为损失误差，使用Adam优化算法来LSTM神经网络。
```python
import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt




class LstmRNN(nn.Module):
    def __init__(self, input_size, hidden_size = 1, output_size = 1, num_layers = 1):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers)
        self.forwardCalculation = nn.Linear(hidden_size, output_size)
        
    def forward(self, _x):
        x, _ = self.lstm(_x)
        s, b, h = x.shape # seq_len, batch, hidden_size
        x = x.view(s*b, h)
        x = self.forwardCalculation(x)
        x = x.view(s, b, -1)
        return x
        
        
def LSTM():
    # 建立数据
    data_len = 200
    t = np.linspace(0, 12*np.pi, data_len)
    sin_t = np.sin(t)
    cos_t = np.cos(t)
    
    dataset = np.zeros((data_len, 2))
    dataset[:, 0] = sin_t
    dataset[:, 1] = cos_t
    dataset = dataset.astype("float32")
    
    # 划分数据
    train_data_ratio = 0.5
    train_data_len = int(data_len*train_data_ratio)
    train_x = dataset[:train_data_len, 0]
    train_y = dataset[:train_data_len, 1]
    INPUT_FEATURES_NUM = 1
    OUTPUT_FEATURES_NUM = 1
    t_for_training = t[:train_data_len]
    
    test_x = dataset[train_data_len:, 0]
    test_y = dataset[train_data_len:, 1]
    t_for_testing = t[train_data_len:]
    
    # 训练
    train_x_tensor = train_x.reshape(-1, 5, INPUT_FEATURES_NUM) # 分5批
    train_y_tensor = train_y.reshape(-1, 5, OUTPUT_FEATURES_NUM) # 分5批
    train_x_tensor = torch.from_numpy(train_x_tensor)
    train_y_tensor = torch.from_numpy(train_y_tensor)
    
    lstm_model = LstmRNN(INPUT_FEATURES_NUM, 16, output_size = OUTPUT_FEATURES_NUM, num_layers = 1)
    print('LSTM model:', lstm_model)
    print('model.parameters:', lstm_model.parameters)
    
    loss_fn = nn.MSELoss()
    lr = 1e-2
    optimizer = torch.optim.Adam(lstm_model.parameters(), lr)
    
    max_epochs = 10000
    for epoch in range(max_epochs):
        output = lstm_model(train_x_tensor)
        loss = loss_fn(output, train_y_tensor)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
        if loss.item() < 1e-4:
            print('Epoch [{}/{}], Loss: {:.5f}'.format(epoch+1, max_epochs, loss.item()))
            print("The loss value is reached")
            break
        elif (epoch+1) % 100 == 0:
            print('Epoch [{}/{}], Loss: {:.5f}'.format(epoch+1, max_epochs, loss.item()))
            
    # 用模型预测
    # 训练集上
    predictive_y_for_training = lstm_model(train_x_tensor)
    predictive_y_for_training = predictive_y_for_training.view(-1, OUTPUT_FEATURES_NUM).data.numpy()
    
    # 切换为测试状态
    lstm_model = lstm_model.eval()
    # 用测试集预测
    test_x_tensor = test_x.reshape(-1, 5, INPUT_FEATURES_NUM) 
    test_x_tensor = torch.from_numpy(test_x_tensor)
    predictive_y_for_testing = lstm_model(test_x_tensor)
    predictive_y_for_testing = predictive_y_for_testing.view(-1, OUTPUT_FEATURES_NUM).data.numpy()
    
    # 画图
    plt.figure()
    plt.plot(t_for_training, train_x, 'g', label='sin_trn')
    plt.plot(t_for_training, train_y, 'b', label='ref_cos_trn')
    plt.plot(t_for_training, predictive_y_for_training, 'y--', label='pre_cos_trn')


    plt.plot(t_for_testing, test_x, 'c', label='sin_tst')
    plt.plot(t_for_testing, test_y, 'k', label='ref_cos_tst')
    plt.plot(t_for_testing, predictive_y_for_testing, 'm--', label='pre_cos_tst')


    plt.plot([t[train_data_len], t[train_data_len]], [-1.2, 4.0], 'r--', label='separation line') # separation line


    plt.xlabel('t')
    plt.ylabel('sin(t) and cos(t)')
    plt.xlim(t[0], t[-1])
    plt.ylim(-1.2, 4)
    plt.legend(loc='upper right')
    plt.text(14, 2, "train", size = 15, alpha = 1.0)
    plt.text(20, 2, "test", size = 15, alpha = 1.0)
    
    plt.savefig("./output/LSTM.png")




if __name__ == "__main__":
    LSTM()
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/04.png)
结果不错。可以看到整个过程跟传统深度网络差不多的，只是激活函数用了nn.LSTM。
再看看原理，[《理解LSTM网络》](https://blog.csdn.net/Jerr__y/article/details/58598296)
原文是英文，打不开了。这是翻译的。
传统神经网络没有记忆性，学了后面忘了前面。在循环神经网络(RNNs)中，有一个循环操作，使其能够保留之前学到的内容。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/05.jpg)

某一时刻的输入Xt，通过神经节A得到输出ht，同时当前时刻的状态会作为下一个时刻的输入的一部分。可以把RNN看作是普通神经网络多次复制后的叠加。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/06.jpg)
对于只需要短期依赖的问题，RNN表现很好。随着关联信息和预测信息间隔很大的长期依赖的问题，RNN很难把它们关联起来。
长短期记忆网络(Long Short Term Memory networks，LSTMs)是一种特殊类型的RNN。其本质是能够记住很长时期的信息。所有RNN都是由完全相同的模块复制而成。在普通RNN中该模块中的结构很简单，比如是由一个单一的tanh层组成。在LSTM中，该模块较复杂，用了四个相互作用的层。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/07.jpg)


每条线都传递着一个向量，从一个节点到另一个节点。
LSTM的核心思想是模块的状态向量从整个模块穿过，只做少了线性操作。可以实现长时间的记忆保留了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/08.jpg)


通过门(gates)结构实现选择性让信息通过。主要是通过一个sigmoid的神经层和一个逐点相乘的操作来实现的。每个LSTM有三个这样的门结构:遗忘门(forget gate layer)、传入门(input gate layer)、输出门(output gate layer)。
遗忘门:让哪些信息继续通过该模块。输入是h(t-1)和x(t)。输出是值在(0,1)之间的向量，其长度和模块状态C(t-1)一样的。表示让C(t-1)中信息通过的比例，0表示完全不让通过， 1表示让所有信息通过。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/09.jpg)


传入门:决定让多少新信息加入到模块状态中。包括两个步骤。一个sigmoid层决定哪些信息需要更新，一个tanh层生成一个向量，即备选用来更新的内容，C't。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/10.jpg)


通过C(t-1)与遗忘门的结果相乘，把不想保留的信息忘掉。结果与传入门结果相加，这就是要更新的内容。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/11.jpg)


输出门:决定输出的内容。通过一个sigmoid层决定C(t)中哪些部分被输出，然后将C(t)经过tanh，最后两个结果相乘形成输出结果。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/12.jpg)


输出结果复制两份，一份传给下一个模块，一份作为该模块的输出结果。
还有一些变形，就先pass了。
最后，尝试用LSTM来解决我们的问题吧。
[代码](https://github.com/zwdnet/JSMPwork/blob/main/LSTM_work.py)
在本地跑得很好，用0.01%的数据就达到59%的准确率，但发现一个问题:太费内存了。当我改成用2%的数据跑就报内存不够了。再到kaggle上提交，用所有数据，结果告诉我需要25000G的内存……搜了一下，要缩小batch_size的大小，但我已经是1了呀。只得缩小数据规模。用2%的数据。提交……
0分!
改了半天，又加了一层sigmoid，再提交
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/71/13.jpg)

唉，先这样吧。接下来打算从头看书。
比赛还有二十天就截止了，看学习的进度吧，可能继续折腾，也可能就这样了。到最后再看看拿奖的大神的解法吧。








我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地




![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)