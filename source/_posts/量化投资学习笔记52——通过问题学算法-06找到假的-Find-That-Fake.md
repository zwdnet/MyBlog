---
title: '量化投资学习笔记52——通过问题学算法:06找到假的(Find That Fake)'
date: 2020-05-16 16:18:28
tags: [量化投资,Python,编程难题,MIT,分治策略]
categories: 量化投资
---
《programming for the puzzled》第六章
涉及到的知识：案例分析，分治法。
在9个硬币中找到一个赝品。假的比真的重一些，你的任务是使称重的次数最少。你需要称几次?
穷举，选出一个硬币与其它八个依次对比，最差需要称八次。
用分治法可以做得更好。先从9个硬币中选出四个，分两组称。有三种情况:相等，则赝品在剩下的五个硬币中。前一组较重，或后一种较重，赝品在这两个硬币中的一个，再比较一次即可确定赝品。在后两种情况中，称两次即可确定。第一种情况，从五个硬币中选出4个，再比较，又有三种情况。相等的情况，赝品是多余那个，一共比较了两次。如果不想等，又比较一次，共比较了三次。这是不是最优的结果呢？可以把九个硬币分三份，称重结果一样的。
用递归来实现分治法。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 6.找假币


# 比较函数
def compare(groupA, groupB):
    if sum(groupA) > sum(groupB):
        result = "left"
    elif sum(groupA) < sum(groupB):
        result = "right"
    else:
        result = "equal"
    return result
   
   
# 将n个硬币划分为三组，假设n为3的倍数
def splitCoins(coinsList):
    length = len(coinsList)
    group1 = coinsList[0:length//3]
    group2 = coinsList[length//3:length//3*2]
    group3 = coinsList[length//2:length]
    return group1, group2, group3
   
   
# 找到有假币那组
def findFakeGroup(group1, group2, group3):
    result1and2 = compare(group1, group2)
    if result1and2 == "left":
        fakeGroup = group1
    elif result1and2 == "right":
        fakeGroup = group2
    elif result1and2 == "equal":
        fakeGroup = group3
    return fakeGroup
   
# 现在进行分治了
def CoinComparison(coinsList):
    counter = 0
    currList = coinsList
    while len(currList) > 1:
        group1, group2, group3 = splitCoins(currList)
        currList = findFakeGroup(group1, group2, group3)
        counter += 1
    fake = currList[0]
    print("假币为第", coinsList.index(fake)+1, "个硬币")
    print("比较次数:", counter)


if __name__ == "__main__":
    coinsList = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10]
    CoinComparison(coinsList)
```
通过分治法不断减小问题规模可以最小化比较次数。我们也可以顺着整个硬币序列依次比较，但在最坏的情况下我们需要比较整个序列。
练习1.如果给一个所有硬币都相同（即没有假币）的列表，程序会返回第一个硬币是假币，解决这个bug。
用找来的"假币"重量与输入的列表的第一个值和最后一个值对比就行了。如果都一样，那就是没有假币。
```python
# 现在进行分治了
def CoinComparison(coinsList):
    counter = 0
    currList = coinsList
    while len(currList) > 1:
        group1, group2, group3 = splitCoins(currList)
        currList = findFakeGroup(group1, group2, group3)
        counter += 1
    fake = currList[0]
    # 练习1
    if fake == coinsList[0] and fake == coinsList[-1]:
        print("没有假币。")
    else:
        print("假币为第", coinsList.index(fake)+1, "个硬币")
    print("比较次数:", counter)
```

本章代码
https://github.com/zwdnet/MyQuant/blob/master/44/06/fz.py


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)