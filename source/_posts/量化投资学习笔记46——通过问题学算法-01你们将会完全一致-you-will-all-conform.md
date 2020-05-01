---
title: '量化投资学习笔记46——通过问题学算法:01你们将会完全一致(you will all conform)'
date: 2020-05-01 12:31:12
tags: [量化投资,Python,编程难题,MIT,列表,字符串,数据压缩]
categories: 量化投资
---
试了一圈，还是用基于问题学习吧。
看《Programming for the Puzzled》，有中译版的。我看的还是英文版的。MIT还有同名的课程。我看的是b站上搬运的:https://b23.tv/5vyRZk
课程主页： https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-s095-programming-for-the-puzzled-january-iap-2018/index.htm，上面有代码和练习解答。
主要训练的是将解决方案实现为代码。在写代码以前先确定代码的行为。
问题描述:一群球迷戴着球帽排成一排准备入场，他们戴的帽子有两个方向。你要通过对某个位置或者某个位置区间的球迷发布命令让其翻转帽子方向，问题是如何用最少的命令来达到这一目的。一个更难的问题，如何在开始的时候就生成所有的命令?
自己先做一下:
```python
# coding:utf-8
# 01.you will all conform


# 获取最少的命令数
def minCommand(cap):
    n = len(cap)
    # 先把"F"变成"B"
    minTimesB = 0
    bF = False
    for i in range(n):
        if cap[i] == "F":
            bF = True
            if i == n-1:
                minTimesB += 1
            continue
        if bF == True:
            minTimesB += 1
        bF = False
    # 再把"B"变成"F"
    minTimesF = 0
    bB = False
    for i in range(n):
        if cap[i] == "B":
            bB = True
            if i == n-1:
                minTimesF += 1
            continue
        if bB == True:
            minTimesF += 1
        bB = False
    return min(minTimesB, minTimesF)


if __name__ == "__main__":
    # 穷举法
    cap = ["F", "F", "B", "B", "B", "F", "B", "B", "B", "F", "F", "B", "F"]
    result = minCommand(cap)
    print(result)
```
能得到正确结果，但是用了两次循环，而且代码有点繁琐。作者给出的方案是先根据输入得到一个区间的列表，包括每个区间的帽子方向。注意最后一个元素，其并不是以帽子方向翻转为结束的。
最坏的情况下，要喊n/2次（n为偶数）或n/2+1次（n为奇数）命令。
来看看作者给出的解法
```python
# 书中第一个解法，先找出相应区间
def pleaseConform(caps):
    start = forward = backward = 0
    intervals = []
    n = len(caps)
    minNum = n
    for i in range(1, n):
        # 帽子方向变了，区间改变
        if caps[start] != caps[i]:
            intervals.append((start, i-1, caps[start]))
            if caps[start] == "F":
                forward += 1
            else:
                backward += 1
            start = i
    # 处理最后一个区间
    intervals.append((start, len(caps)-1, caps[start]))
    if caps[start] == "F":
        forward += 1
    else:
        backward += 1
    if forward < backward:
        flip = "F"
        minNum = forward
    else:
        flip = "B"
        minNum = backward
    for t in intervals:
        if t[2] == flip:
            print("在位置{}到{}的人，翻转你的帽子".format(t[0], t[1]))
    return minNum
```
运行结果:
在位置2到4的人，翻转你的帽子                                       
在位置6到8的人，翻转你的帽子                                       
在位置11到11的人，翻转你的帽子                                     
3                                   
比我的要长，不过清楚多了，而且只用遍历列表一遍。当然还遍历了一遍区间列表，在极端的情况下还是等于遍历了两遍。然后是用tuple来记录区间起始点及帽子方向的，要会用tuple，不要只会list。
下面尝试代码优化。尽量缩短代码，更小的程序通常更有效率，bug也要更少。
为了避免对结尾的特殊判断，可以在输入的caps列表里加一个“结束标志”
caps = caps + ["END"]
这样对最后一个区间的特殊处理就不用了。另外一个好处是输入空列表程序也不会崩溃了。
```python
# 书中第二个解法，对解法一的优化
def pleaseConform2(caps):
    start = forward = backward = 0
    intervals = []
    # 在数据末尾增加末尾标志
    caps = caps + ["END"]
    n = len(caps)
    minNum = n
    for i in range(1, n):
        # 帽子方向变了，区间改变
        if caps[start] != caps[i]:
            intervals.append((start, i-1, caps[start]))
            if caps[start] == "F":
                forward += 1
            else:
                backward += 1
            start = i
    if forward < backward:
        flip = "F"
        minNum = forward
    else:
        flip = "B"
        minNum = backward
    for t in intervals:
        if t[2] == flip:
            print("在位置{}到{}的人，翻转你的帽子".format(t[0], t[1]))
    return minNum
```
注意别用caps.append("END")，这是在原来的数据上直接添加，当函数返回后数据还是被改变了。而caps = caps + ["END"]是创建一个新的列表，并不改变原来的列表。
现在来解决更难的问题：能不能在第一遍遍历的时候就确定命令的最小子集？
前面的程序还是遍历了两遍才得到命令序列的。这个我真想不出来，下面是书中的答案。
```python
# 一遍遍历的程序
def pleaseConformOnepass(caps):
    caps = caps + [caps[0]]
    minNum = 0
    for i in range(1, len(caps)):
        if caps[i] != caps[i-1]:
            if caps[i] != caps[0]:
                print("位置在", i)
            else:
                print("到", i-1, "的人，翻转你的帽子!")
                minNum += 1
    return minNum
```
原理是两个方向的帽子的区间数只相差1，如果第一个人的帽子是一个方向，该方向的区间数绝不会比另一个方向上的区间数小。（意思应该是最后的答案一定是翻转跟第一个人帽子方向相反的人的帽子）
上面的程序用与第一个人帽子方向相同的方向来标记末尾。当第一次碰到与第一个人帽子方向相反的情况的时候，我们开始记录区间。这意味着我们实际上跳过了第一个区间。该程序的缺点是不好修改，另外也需要额外处理输入数据为空的情况。
所以高效的简洁的程序往往隐藏了更复杂的东西，你要看得出那些东西才能写得出来。
这个问题背后的动机是数据压缩，比如"WWWWWWWWWWWWWBBWWWWWWWWWWWWBBBBB"可以压缩为“13W2B12W5B”，“WBWBWBWBWB”照此算法“压缩”为“1W1B1W1B1W1B1W1B1W1B”，然而更好的算法会压缩为"5(WB)"。
练习
1.对于最后一个区间只有一个元素的情况，会输出“在位置11到11的人，翻转你的帽子 ”，修改程序使其输出为"在位置11的人，翻转你的帽子 "。
改成
```python
if t[0] != t[1]:
                print("在位置{}到{}的人，翻转你的帽子".format(t[0], t[1]))
else:
                print("在位置{}的人，翻转你的帽子".format(t[0], t[1]))
```
即可。
2.修改一次遍历的程序，像练习1一样输出更自然的结果，并且确保输入空列表不会崩溃。
在开始增加判断并像练习一一样输出修改即可。
```python
# 一遍遍历的程序,根据练习2修改版
def pleaseConformOnepass2(caps):
    if len(caps) == 0:
        return 0
    caps = caps + [caps[0]]
    minNum = 0
    start = 0
    for i in range(1, len(caps)):
        if caps[i] != caps[i-1]:
            if caps[i] != caps[0]:
                start = i
            else:
                if start != i-1:
                    print("位置在", start, "到", i-1, "的人，翻转你的帽子!")
                else:
                    print("位置在", start,  "的人，翻转你的帽子!")
                minNum += 1
    return minNum
```
练习3.假设有一些戴“奇异”帽子的人在队列中，以"H"标记，修改程序，跳过这些人，输出正确的命令。
统计的时候直接忽略"H"就行了。
```python
# 练习三，增加"H"帽子的人，忽略
def pleaseConform3(caps):
    start = forward = backward = 0
    intervals = []
    # 在数据末尾增加末尾标志
    caps = caps + ["END"]
    n = len(caps)
    minNum = n
    for i in range(1, n):
        # 帽子方向变了，区间改变
        if caps[start] != caps[i]:
            intervals.append((start, i-1, caps[start]))
            if caps[i-1] == "F":
                forward += 1
            elif caps[i-1] == "B":
                backward += 1
            start = i
    if forward < backward:
        flip = "F"
        minNum = forward
    else:
        flip = "B"
        minNum = backward
    for t in intervals:
        if t[2] == flip:
            if t[0] != t[1]:
                print("在位置{}到{}的人，翻转你的帽子".format(t[0], t[1]))
            else:
                print("在位置{}的人，翻转你的帽子".format(t[0], t[1]))
    return minNum
```
练习4.写一个one pass压缩和解压程序。
```python
# 练习4 压缩和解压程序
# 压缩
def compress(words):
    str_list = list(words)
    str_list.append(str_list[0])
    start = 0
    code = []
    for i in range(1, len(str_list)):
        if str_list[start] != str_list[i]:
            code.append((start, i-1, str_list[start]))
            start = i
    result = []
    for t in code:
        a = t[0]
        b = t[1]
        w = t[2]
        length = b-a+1
        result.append(str(length))
        result.append(w)
    return "".join(result)
   
   
# 解压缩
def decompress(code):
    result = []
    num = []
    char = ""
    for i in range(len(code)):
        if code[i].isalpha() == False:
            num.append(code[i])
        else:
            nums = int("".join(num))
            num = []
            result.append(code[i]*nums)
    return "".join(result)

# 练习四
if __name__ == "__main__":
    s = "BWWWWWBWWWWWWWWWWWAAKKGGP"
    code = compress(s)
    print("原字符串为:", s)
    print("压缩后的字符串为:", code)
    ds = decompress(code)
    print("解压后的字符串为:", ds)
```
本章全部代码 https://github.com/zwdnet/MyQuant/blob/master/44/01/ycac.py
再去看看视频。打算把21个问题都像这么来一遍。主要锻炼自己的编程能力。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)