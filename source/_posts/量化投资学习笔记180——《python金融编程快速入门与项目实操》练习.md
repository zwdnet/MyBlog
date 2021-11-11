---
title: 量化投资学习笔记180——《python金融编程快速入门与项目实操》练习
date: 2021-11-11 16:36:46
tags: [量化投资, python, 实操]
categories: 量化投资
---
这是我参加高顿的引流课程送的书。python我基本熟悉了，就看看实操项目吧。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/01.jpg)

### 实操1.货币兑换
输入汇率和兑换金额及币种，输出换算金额。
尝试用刚学的测试驱动开发方法进行，先写测试。
```python
# 测试换算程序
def test_currency():
    assert currency(6.0, "3.0CNY") == "0.5USD"
    assert currency(6.0, "5.0USD") == "30CNY"
    assert currency(-3.0, "2.0USD") == "汇率需大于0"
    assert currency(3.0, "-2.0CNY") == "金额需大于0"
    assert currency(3.0, "5.0USA") == "货币单位错误，需为CNY或USD"


# 货币兑换程序
def currency(rate, amount):
    return "测试"
```
运行测试

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/02.jpg)

然后实现currency使测试通过。
```python
# 货币兑换程序
def currency(rate, amount):
    if rate <= 0.0:
        return "汇率需大于0"
    curr = amount[-3:]
    money = eval(amount[0:3])
    if curr != "CNY" and curr != "USD":
        return "货币单位错误，需为CNY或USD"
    if money <= 0.0:
        return "金额需大于0"
    if curr == "CNY":
        return str(money / rate) + "USD"
    elif curr == "USD":
        return str(money * rate) + "CNY"
```
测试通过了，现在写输入程序和主程序。
```python
# 输入程序
def get_input():
    rate = float(input("请输入汇率:"))
    amount = input("请输入换算金额，以CNY/USD结尾:")
    return rate, amount
    
    
if __name__ == "__main__":
    datas = get_input()
    result = currency(datas[0], datas[1])
    print("换算结果为:", result)
```
现在程序可以运行了。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/03.jpg)

但还是有bug，如果除了最后3位输入的不是数字会有问题。再增加测试。
```python
assert currency(6.0, "6.5DUSA") == "输入的金额不是数字"
```
测试失败，还要增加个判断字符串是否是数字的函数:
```python
# 测试字符串判断函数
def test_isdigit():
    assert isdigit("666") == True
    assert isdigit("666.66") == True
    assert isdigit("-555.66") == True
    assert isdigit("655.54+") == False
    assert isdigit("-544gf") == False
        
        
# 判断字符串是否为数字
def isdigit(money):
    if money.count('.') == 1:
        left = money.split(".")[0]
        right = money.split(".")[1]
        if right.isdigit():
            if left.count("-") == 1 and left.startswith("-"):
                num = left[1:]
                if num.isdigit():
                    return True
            elif left.isdigit():
                return True
    elif money.count('.') == 0:
        return money.isdigit()
    return False
```
测试通过了。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/04.jpg)

接下来可以重构，把错误检测的程序提炼成一个函数吧。
```python
# 货币兑换程序
def currency(rate, amount):
    res = judge(rate, amount)
    if res != "OK":
        return res
    curr = amount[-3:]
    money = eval(amount[0:-3])
    if curr == "CNY":
        return str(money / rate) + "USD"
    elif curr == "USD":
        return str(money * rate) + "CNY"
        
        
# 测试判断程序
def test_judge():
    assert judge(6.0, "3.0CNY") == "OK"
    assert judge(6.0, "5.0USD") == "OK"
    assert judge(-3.0, "2.0USD") == "汇率需大于0"
    assert judge(3.0, "-2.0CNY") == "金额需大于0"
    assert judge(3.0, "5.0USA") == "货币单位错误，需为CNY或USD"
    assert judge(6.0, "6.5DUSA") == "输入的金额不是数字"
        
        
# 判断参数是否合法
def judge(rate, amount):
    if rate <= 0.0:
        return "汇率需大于0"
    curr = amount[-3:]
    if isdigit(amount[0:-3]) == False:
        return "输入的金额不是数字"
    if curr != "CNY" and curr != "USD":
        return "货币单位错误，需为CNY或USD"
    money = eval(amount[0:-3])
    if money <= 0.0:
        return "金额需大于0"
    return "OK"
```
基本搞定。
完整程序: https://github.com/zwdnet/gaodun/blob/main/01_currency.py

### 实操2:计算资金的时间价值
套公式，直接写吧。
代码:https://github.com/zwdnet/gaodun/blob/main/02_value.py

### 实操3:期权定价模型
其它实例都是语言的直接运用，pass了。
期权赋予持有人在某一特定日期或该日期之前的任何时间以固定价格购进或出售标的的资产的权利。
看涨期权，也称认购期权，是指期权买方向卖方支付一定数额的权利金之后，即拥有在期权的有效期内，按约定价格向期权卖方买入一定数量的标的资产的权利。对买方为权利，对卖方为义务。看跌期权，也称认沽期权。买方在约定时间内以约定价格向卖方卖出一定量资产的权利。
欧式期权:在约定日当日决定是否行权，美式期权:再约定期前任何交易日觉得是否行权。
直接撸代码吧。
代码:https://github.com/zwdnet/gaodun/blob/main/03_future.py

### 实操4:寻找最优投资组合
期望收益率给定时，寻求风险最小的投资组合;风险给定时，寻求预期收益率最高的投资组合。
模型:马科维茨的均值-方差模型。
实操，用建行、上汽、茅台三只股票的历史数据来构建投资组合。原文是直接读取csv文件数据，但数据要扫码加客服才有(引流……)，我自己下载数据计算每日收益率组成数据，比较了一下，书上用的应该是不复权的数据。
先模拟10000次不同权重的投资组合结果，输出收益率与标准差(风险)的比值:

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/05.jpg)

接着确定投资组合的有效前沿。

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/06.jpg)


加入无风险资产后的最优市场组合

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/149/07.jpg)

最后结果:
[array([0.548, 0.   , 0.452])]
跟原文有差异。
代码:https://github.com/zwdnet/gaodun/blob/main/04_invest.py

看了这本书，感觉对0基础的挺合适，讲得很细。



我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。

我的个人博客地址：https://zwdnet.github.io

我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts

我的微信个人订阅号：赵瑜敏的口腔医学学习园地

