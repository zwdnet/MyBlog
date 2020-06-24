---
title: '量化投资学习笔记68——通过问题学算法18:记忆力很好（Memory Serves You Well）'
date: 2020-06-24 16:05:16
tags: [量化投资, 算法, 学习笔记, 递归算法，回溯法]
categories: 量化投资
---
《programming for the puzzled》第18章
设计到的语言和算法知识：建立和查找字典，异常，在递归搜索中使用查表法。
问题描述：我们有一组硬币排成一排，每个硬币有一个正数值。我们需要挑选一个硬币的子集，使其和最大，但我们不能选择两个相邻的硬币。
如硬币为14,3,27,4,5,15,1，我们应该选择14，跳过3，选择27，跳过4和5，选择15，跳过1。总和为56。采用另外的选法得到的总和都小于56。
首先使用递归算法解决这个问题。我们选择不同的硬币，选择它或跳过它，当跳过一个硬币时，我们可以选择或跳过下一个硬币。如果我们选择一个硬币时，我们必须跳过下一个硬币。最后返回硬币数值之和。
```python
# 《programming for the puzzled》实操
# 18.好记性问题


# 递归法
def coins(row, table):
    if len(row) == 0:
        table[0] = 0
        return 0, table
    elif len(row) == 1:
        table[1] = row[0]
        return row[0], table
    pick = coins(row[2:], table)[0] + row[0]
    skip = coins(row[1:], table)[0]
    result = max(pick, skip)
    table[len(row)] = result
    return result, table


if __name__ == "__main__":
    row = [14, 3, 27, 4, 5, 15, 1]
    table = {}
    result, table = coins(row, table)
    print(result)
    print(table)
```
现在用回溯法试试，看看table有啥用。
```python
def traceback(row, table):
    select = []
    i = 0
    while i < len(row):
        if (table[len(row)-i] == row[i]) or (table[len(row)-i] == table[len(row)-i-2] + row[i]):
            select.append(row[i])
            i += 2
        else:
            i += 1
    print("输入行:", row)
    print("表格:", table)
    print("选择的硬币:", select, "总数:", table[len(row)])
```
这里的table是上一个算法的输出结果。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
