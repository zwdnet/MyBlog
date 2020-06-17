---
title: 量化投资学习笔记64——通过问题学算法：15计数(Counting the ways you can count change)
date: 2020-06-14 12:39:41
tags: [量化投资, 算法, 学习笔记, 递归算法, 组合算法]
categories: 量化投资
---
《programming for the puzzled》第15章
用到的算法：递归生成组合
你有一堆所有币值的美元：1,2,5,10,20,50,100。你欠别人6美元，你有多少种不同的偿还的方式？
1,1,1,1,1,1
1,1,1,1,2
1,1,2,2
1,5
2,2,2
忽然你发现自己欠别人的是16美元，又有多少种偿还方式？
编程来找吧。
```python
# 《programming for the puzzled》实操
# 15.计数问题


def makeChange(bills, target, sol = []):
    if sum(sol) == target:
        print(sol)
        return
       
    if sum(sol) > target:
        return
       
    for bill in bills:
        newSol = sol[:]
        newSol.append(bill)
        makeChange(bills, target, newSol)
    return

if __name__ == "__main__":
    bills = [1, 2, 5]
    makeChange(bills, 6)
```
结果
```python
[1, 1, 1, 1, 1, 1]
[1, 1, 1, 1, 2] 
[1, 1, 1, 2, 1] 
[1, 1, 2, 1, 1] 
[1, 1, 2, 2] 
[1, 2, 1, 1, 1] 
[1, 2, 1, 2] 
[1, 2, 2, 1] 
[1, 5] 
[2, 1, 1, 1, 1] 
[2, 1, 1, 2] 
[2, 1, 2, 1] 
[2, 2, 1, 1] 
[2, 2, 2] 
[5, 1] 
[Program finished]
```
有问题，相同币值的不同排列被当成了不同的支付方式。
下面就要来消除重复了。做法简单来说就是要去除结果中的非递增序列，像[1,1,1,2,1]这样的。
```python
# 去除重复结果
def makeSmartChange(bills, target, highest, sol = []):
    if sum(sol) == target:
        print(sol)
        return
        
    if sum(sol) > target:
        return
    
    for bill in bills:
        if bill >= highest:
            newSol = sol[:]
            newSol.append(bill)
            # 就这里不一样
            makeSmartChange(bills, target, bill, newSol)
    return
```
更进一步的，要找到给的钞票数量最少的方法呢？可以排序以后选出计数最少的方法。
本文代码：https://github.com/zwdnet/MyQuant/blob/master/44/15


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)