---
title: '量化投资学习笔记47——通过问题学算法:02聚会的最佳时间(the best time to party)'
date: 2020-05-03 09:31:19
tags: [量化投资,Python,编程难题,MIT,列表,排序]
categories: 量化投资
---
《programming for the puzzled》第二章
题目描述:一个聚会不同的人抵达和离开的时间的列表，其中的时间是前闭后开的，即如果你在结束的时间点到达，也会错过这个人。你只有一个小时，找到最佳的参加聚会的时间，使得碰到的人最多。
以一个tuple列表来表示不同的人参加聚会时间区间。
sched = [(6, 8), (6, 12), (6, 7), (7, 8), (7, 10), (8, 9), (8, 10), (9, 12), (9, 10), (10, 11), (10, 12), (11, 12)]
先自己做一下吧。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 参加聚会的最佳时间


# 自己的方法
def bestTime(sched):
    n = len(sched)
    start = []
    end = []
    for t in sched:
        start.append(t[0])
        end.append(t[1])
    minTime = min(start) # 最早的开始时间
    maxTime = max(end) # 最晚的结束时间
    max_time = 0
    result = minTime
    for time in range(minTime, maxTime):
        times = 0
        for i in range(n):
            if time >= start[i] and time+1 <= end[i]:
                times += 1
        if times > max_time:
            max_time = times
            result = time
        times = 0
    print(max_time)
    return result


if __name__ == "__main__":
    sched = [(6, 8), (6, 12), (6, 7), (7, 8), (7, 10), (8, 9), (8, 10), (9, 12), (9, 10), (10, 11), (10, 12), (11, 12)]
    # 自己的方法
    result = bestTime(sched)
    print("最佳时间:", result)
```
用的穷举，两层循环。结果是9点去，可以碰到5个人。
再来看看作者的分析。思路跟我一样的，穷举。
```python
# 作者的第一个算法，也是穷举
def bestTimeToParty(schedule):
    start = schedule[0][0]
    end = schedule[0][1]
    for c in schedule:
        start = min(c[0], start)
        end = max(c[1], end)
        count = celebrityDensity(schedule, start, end)
        maxcount = 0
        for i in range(start, end+1):
            if count[i] > maxcount:
                maxcount = count[i]
                time = i
    print("到达party的最佳时间为", time, "点，有", maxcount, "个人抵达。")
        
        
# 工具函数
def celebrityDensity(sched, start, end):
    count = [0]*(end+1)
    for i in range(start, end+1):
        count[i] = 0
        for c in sched:
            if c[0] <= i and c[1] > i:
                count[i] += 1
    return count
```
运行结果跟我是一样的，几个要点。
输入的数据不能更改，因此用tuple。
那个工具函数是计算到目前为止的时间区间内能遇到的人数，貌似有重复计算的。
程序的问题:如果时间不是整数，而是任意时间，如果精确到分钟，遍历次数会膨胀60倍，如果到秒，微秒呢……考虑一个不依赖时间粒度的算法。
这个我就想不出来了，看作者的程序吧。
```python
# 处理更细的时间
def bestTimeToPartySmart(schedule):
    times = []
    for c in schedule:
        times.append((c[0], "start"))
        timed.append((c[1], "end"))
    sortList(times)
    maxCount, time = chooseTime(times)
    print("到达聚会的最佳时间为{}点，能遇到{}个人。".format(time, maxCount))

# 改进，处理更细的时间段
sched2 = [(6.0, 8.0), (6.5, 12.0), (6.5, 7.0), (7.0, 8.0), (7.5, 10.0), (8.0, 9.0), (8.0, 10.0), (9.0, 12.0), (9.5, 10.0), (10.0, 11.0), (10.0, 12.0), (11.0, 12.0)]
bestTimeToPartySmart(sched2)
```
可以处理更细的时间了，思路是将所有人的赴约计划看成一条时间线，我自己的赴约时间与他们的时间线重合则能与他们相遇。于是只要看时间点的起止就行了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/35/01.png)
先根据日程取出时间区间的起止点，对这个列表排序，在找出赴约时间和能见到的最大人数。输入数据是浮点数而不是整数。
下面实现排序和选择函数
```python
# 对列表排序
def sortList(tlist):
    for ind in range(len(tlist)-1):
        iSm = ind
        for i in range(ind, len(tlist)):
            if tlist[iSm][0] > tlist[i][0]:
                iSm = i
        tlist[ind], tlist[iSm] = tlist[iSm], tlist[ind]
        
        
# 选择时间
def chooseTime(times):
    rcount = 0
    maxcount = time = 0
    for t in times:
        if t[1] == "start":
            rcount += 1
        elif t[1] == "end":
            rcount -= 1
        if rcount > maxcount:
            maxcount = rcount
            time = t[0]
    return maxcount, time
```
排序用的是选择排序，排序完成以后进行选择，方法是挨个取出排序好的列表中的元素，如果是抵达时间，计数器加一，如果是离开时间，计数器减一，并记录当前的最大相遇人数和取到最大值时的时间（因为当取值最大时，一定只能是抵达时间而不是离开时间）。
这样只要对列表遍历一遍就行了，而不是像第一个算法那样遍历两遍。但是选择排序的时间复杂度还是O(n²)。用其它排序方法可以优化到O(nlogn)。
练习1.假如你非常忙，只能在[ystart, yend)时间段内参加聚会，求你能见到的最多的人数。
在chooseTime函数的判断力增加时间限制即可。
if rcount > maxcount  and t[0] >= ystart and t[0] < yend:
练习2.另一个不依赖时间粒度的算法:依次检查每个参加者的时间区间，看这个参加者的到达时间在多少其它参加者的时间区间内。选择最多的那位参与者的抵达时间。
```python
# 练习2.另一种不依赖时间粒度的算法
def bestTimeToPartySmart3(schedule):
    maxCount = 0
    time = 0
    n = len(schedule)
    for i in range(n):
        count = 0
        start = schedule[i][0]
        for j in range(n):
            if schedule[j][0] <= start and schedule[j][1] > start:
                count += 1
        if count > maxCount:
            maxCount = count
            time = start
    print("到达聚会的最佳时间为{}点，能遇到{}个人。".format(time, maxCount))
```
练习3.设想用一个数字表示你有多想见一位嘉宾，用一个三维的tuple表示，如(6.0, 8.0, 3)表示Ta六点到，8点离开，你想见Ta的程度为3。修改程序，找到你的抵达时间，使得权重值最大化（而不是人数）。
```python
# 练习3，使自己见到的嘉宾权重最大
def bestTimeToPartySmart4(schedule):
    maxWeight = 0
    time = 0
    n = len(schedule)
    for i in range(n):
        weight = 0
        start = schedule[i][0]
        for j in range(n):
            if schedule[j][0] <= start and schedule[j][1] > start:
                weight += schedule[j][2]
        if weight > maxWeight:
            maxWeight = weight
            time = start
    print("到达聚会的最佳时间为{}点，最大权重值为{}。".format(time, maxWeight))

# 练习3，使自己见到的嘉宾权重最大
sched3 = [(6.0, 8.0, 2), (6.5, 12.0, 1), (6.5, 7.0, 2), (7.0, 8.0, 2), (7.5, 10.0, 3), (8.0, 9.0, 2), (8.0, 10.0, 1), (9.0, 12.0, 2), (9.5, 10.0, 4), (10.0, 11.0, 2), (10.0, 12.0, 3), (11.0, 12.0, 7)]
bestTimeToPartySmart4(sched3)
```
就是把原来记次的地方改成累加权重。输出的结果是在11点抵达，最大权重值为13。跟书中的结果一样。
本章完成。b站上的课程视频的中文字幕貌似是机器翻译的，还不如没有呢。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)