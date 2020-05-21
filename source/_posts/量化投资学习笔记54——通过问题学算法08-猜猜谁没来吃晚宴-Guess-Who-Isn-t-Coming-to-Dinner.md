---
title: '量化投资学习笔记54——通过问题学算法08:猜猜谁没来吃晚宴(Guess Who Isn''t Coming to Dinner)'
date: 2020-05-21 14:47:33
tags: [量化投资, 算法, 学习笔记, 最大独立集问题]
categories: 量化投资
---
《programming for the puzzled》第八章
你认识很多人，想办一个晚宴。但是你认识的人中有的是互相敌视的。你要确保邀请的人不会互相打起来搅乱宴会，但同时又要有尽可能多的人参加晚宴。
假设你的社交圈是一个图，每个顶点是一个朋友。如果两个人之间有一条边，说明这两个人至少有一个人不喜欢对方，或者两人互相不喜欢对方。你不希望这两个人同时出现在你的晚宴。链条没有转移性：A不喜欢B，B不喜欢C，不代表A一定不喜欢C。
问题是，给你一个这样的关系图，用算法找出你所能邀请的最大人数。
第一个尝试：用贪心算法。首先选出讨厌的人最少的人，一旦选定，与其互相讨厌的人就被排除了。持续这个过程，直到所有人都被选定或排除。然而这会碰到所有人不喜欢的人数都相等的情况，比如3个人组成的三角。这时算法就没法工作了。
生成所有的组合，再比较。
首先要生成可能的组合。有N个元素，用N位二进制数字来代表，选入，则为1，不选，则为0。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 8.晚宴的人数


# 生成宾客列表的组合
def Combinations(n, guestList):
    allCombL = []
    for i in range(2**n):
        num = i
        cList = []
        for j in range(n):
            if num%2 == 1:
                cList = [guestList[n-1-j]] + cList
            num = num // 2
        allCombL.append(cList)
    return allCombL


if __name__ == "__main__":
    guest = ["A", "B", "C", "D", "E"]
    combL = Combinations(len(guest), guest)
    print(combL)
```
接下来第二步是从组合中排出含有互相讨厌的人的组合。如果互相讨厌的两个人都在一个组合里，这个组合就不符合要求需要被排除。
```python
# 排除不符合的组合
def removeBadCombs(allCombL, dislikePairs):
    allGoodCombs = []
    for i in allCombL:
        good = True
        for j in dislikePairs:
            if j[0] in i and j[1] in i:
                good = False
        if good:
            allGoodCombs.append(i)
    return allGoodCombs
```
最后，找到含有元素最多的组合。
```
# 找到元素最多的组合，就是邀请名单啦
def InviteDinner(guestList, dislikePairs):
    allCombL = Combinations(len(guestList), guestList)
    allGoodCombs = removeBadCombs(allCombL, dislikePairs)
    invite = []
    for i in allGoodCombs:
        if len(i) > len(invite):
            invite = i
    print("邀请名单:", invite)
```
可以用内建的max函数来代替自己查找：invite = max(allGoodCombs, key = len)
内存使用的优化。当n很大时，2^n是一个很大的数。需要占用很多的内存。优化的方法是：只在使用之前才生成组合，而不是先生成所有的组合保存起来。
```python
# 优化内存占用
def InviteDinnerOptimized(guestList, dislikePairs):
    n, invite = len(guestList), []
    for i in range(2**n):
        Combination = []
        num = i
        for j in range(n):
            if (num%2 == 1):
                Combination = [guestList[n-1-j]] + Combination
            num = num // 2
        good = True
        for j in dislikePairs:
            if j[0] in Combination and j[1] in Combination:
                good = False
        if good:
            if len(Combination) > len(invite):
                invite = Combination
    print("邀请名单:", invite)
```
这个问题叫最大独立集问题（maximum independent set）：给定一个图的顶点和边，找到彼此之间没有边连接的顶点数目最多的集合。这是个很难的问题，主要是时间复杂度是指数级的(2^n)。如果不用找最大集，可以用贪心法：重复从讨厌的人数最少的人中选取。
练习1：你喜欢的人的程度是不一样的，宾客列表里除了有名字还有相应的你喜欢其的权重。
```python
# 练习1，带权重的算法
def InviteDinnerWeight(guestList, dislikePairs):
    allCombL = Combinations2(len(guestList), guestList)
    allGoodCombinations = removeBadCombinations2(allCombL, dislikePairs)

    invite = max(allGoodCombinations, key=weight)
    print ('带权重的解法:', invite)
    print ('权重为:', weight(invite))
    
    
def Combinations2(n, guestList):
    allCombL = []
    for i in range(2**n):
        num = i
        cList = []
        for j in range(n): 
            if (num % 2 == 1):
                cList = [guestList[n-1-j]] + cList
            num = num // 2
        allCombL.append(cList)
    return allCombL
    
    
def removeBadCombinations2(allCombL, dislikePairs):
    allGoodCombinations = []
    for i in allCombL:
        good = True
        for j in dislikePairs:
            if member(j[0], i) and member(j[1], i):
                good = False
        if good:
            allGoodCombinations.append(i)          
    return allGoodCombinations
    
    
def member(guest, gtuples):
    for g in gtuples:
        if guest == g[0]:
            return True
    return False
    
    
def weight(comb):
    return sum(c[1] for c in comb)
```
    
练习2，3略。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)