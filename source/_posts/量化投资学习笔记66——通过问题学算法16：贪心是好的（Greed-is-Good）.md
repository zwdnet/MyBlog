---
title: 量化投资学习笔记66——通过问题学算法：贪心是好的（Greed is Good）
date: 2020-06-17 15:52:52
tags: [量化投资, 算法, 学习笔记, 贪心算法]
categories: 量化投资
---
《programming for the puzzled》第16章
涉及到的语言和算法知识：函数作为参数，贪心算法。
贪心算法是在每步都选择局部最优解，希望于能找到全局最优解。在很多问题里贪心算法并不能得到全局最优解。
问题描述：根据课程安排（以一个[a,b)区间列表给出，a,b是一天中的小时数，前闭后开意味着另一门课可以从b开始。），选出最多的课程。
贪心法流程：
①使用一些法则选择一个课程c。
②排除所有与c冲突的课程。
③如果剩余课程集合不为空，重复第一步。
其中第一步有很多方法：
最短时间算法：选剩下的课程中时间最短的。但并不总是有效的。
最早开始算法：选剩下的课程中开始时间最早的，也不是总有效。
最小冲突法：选剩下的课程中与其它课程冲突最少的，还是不行。
最早结束算法：选剩下课程结束时间最早的，可以了。（通过数学归纳法证明的。）
下面上代码
```python
# 《programming for the puzzled》实操
# 16.选课问题，贪心算法


def executeSchedule(courses, selectionRule):
    selectedCourses = []
    while len(courses) > 0:
        selCourse = selectionRule(courses)
        selectedCourses.append(selCourse)
        courses = removeConflictingCourses(selCourse, courses)
    return selectedCourses
   
   
def removeConflictingCourses(selCourse, courses):
    nonConflictingCourses = []
    for s in courses:
        if s[1] <= selCourse[0] or s[0] >= selCourse[1]:
            nonConflictingCourses.append(s)
    return nonConflictingCourses
   
   
def shortDuration(courses):
    shortDuration = courses[0]
    for s in courses:
        if s[1] - s[0] < shortDuration[1] - shortDuration[0]:
            shortDuration = s
    return shortDuration
   
   
def leastConflicts(courses):
    conflictTotal = []
    for i in courses:
        conflictList = []
        for j in courses:
            if i == j or i[1] <= j[0] or i[0] <= j[1]:
                continue
            conflictList.append(courses.index(j))
        conflictTotal.append(conflictList)
    leastConflict = min(conflictTotal, key = len)
    leastConflictCourse = courses[conflictTotal.index(leastConflict)]
    return leastConflictCourse
   
   
def earliestFinishTime(courses):
    earliestFinishTime = courses[0]
    for i in courses:
        if i[1] < earliestFinishTime[1]:
            earliestFinishTime = i
    return earliestFinishTime


if __name__ == "__main__":
    mycourses = [[8,9], [8,10], [12,13], [16,17], [18,19], [19,20], [18,20], [17,19], [13,20], [9,11], [11,12], [15,17]]
    print("最短时间间隔", executeSchedule(mycourses, shortDuration))
    print("最早结束时间", executeSchedule(mycourses, earliestFinishTime))
```
不同的选择算法通过函数参数传递给算法。
贪心算法能得到图的最短路径，见第20个问题。
本章代码：本文代码：https://github.com/zwdnet/MyQuant/blob/master/44/16


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)