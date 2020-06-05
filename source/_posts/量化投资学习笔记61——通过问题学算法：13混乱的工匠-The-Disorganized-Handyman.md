---
title: 量化投资学习笔记61——通过问题学算法：13混乱的工匠(The Disorganized Handyman)
date: 2020-06-05 13:51:45
tags: [量化投资, 算法, 学习笔记, 分治策略, 快速排序]
categories: 量化投资
---
《programming for the puzzled》第13章
涉及到的算法：原地旋转，递归实现原地排序。
一位工匠有很多不同的螺栓和螺母，每个螺栓匹配一个螺母。但它们在袋子里都混了。如何最好的排序这些螺母以匹配相应的螺栓？
可以任选一个螺母，去依次试所有的螺栓，直到找到匹配的那个。这样，最坏的情况下，一共要试n+(n-1)+...+1次，复杂度为O(n^2)。
直接把螺母分成两部分，递归完成是不行的，因为有可能找不到相匹配的螺栓。在分治策略中，我们必须找到合适的划分方法，将问题划分为与原问题相似但规模较小的多个子问题。这些问题必须能被独立解决。
分治法中的枢纽
我们可以选择一个螺栓做为枢纽，使用它决定哪些螺母比它小，哪个正好合适，哪些比它大。用这个方法把螺母分成3堆，中间的只有一个螺母，就是匹配枢纽的那个。用枢纽螺栓又可以把螺栓分成两堆，比枢纽大的和比枢纽小的。现在我们就有了“大”螺栓和“大”螺母。以及相应的“小”螺栓和“小”螺母。再在两堆中递归执行此过程。
这个算法就是最广泛使用的排序方法：快速排序法。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 13.快速排序


def quicksort(lst, start, end):
    if start < end:
        split = pivotPartition(lst, start, end)
        quicksort(lst, start, split-1)
        quicksort(lst, split+1, end)
       
       
# 划分枢纽的过程
def pivotPartition(lst, start, end):
    pivot = lst[end]
    less, pivotList, more = [], [], []
    for e in lst:
        if e < pivot:
            less.append(e)
        elif e > pivot:
            more.append(e)
        else:
            pivotList.append(e)
    i = 0
    for e in less:
        lst[i] = e
        i += 1
    for e in pivotList:
        lst[i] = e
        i += 1
    for e in more:
        lst[i] = e
        i += 1
    return lst.index(pivot)


if __name__ == "__main__":
    a = [4, 65, 2, -31, 0, 99, 83, 782, 1]
    quicksort(a, 0, len(a) - 1)
    print(a)
```
这个程序可以工作了，但是并没有完全体现快速排序的优势，用了额外的列表，下面试试原地排序。
```python
# 更好的选取枢纽的方法
def pivotPartitionClever(lst, start, end):
    pivot = lst[end]
    bottom = start - 1
    top = end
    done = False
    while not done:
        while not done:
            bottom += 1
            if bottom == top:
                done = True
                break
            if lst[bottom] > pivot:
                lst[top] = lst[bottom]
                break
        while not done:
            top -= 1
            if top == bottom:
                done = True
                break
            if lst[top] < pivot:
                lst[bottom] = lst[top]
                break
    lst[top] = pivot
    return top
```
快速排序是使用最广泛的排序算法，其时间复杂度为O(nlog2n)。
本书未涉及的插入排序、堆排序等，都是原地排序。插入排序的效率是平方级的，但是对小规模数据，几乎有序的数据效率相对高一些。堆排序在最差的情况下效率也是O(nlog2n)。
Python对列表内置了排序函数，比我们写的要快。但是主要原因是它是用更低级的语言写的而且仔细优化过，而不是算法有什么改进。
练习1.增加比较次数的计数器，在排序完成后输出比较次数。
用全局变量就行了。注意在函数里使用要先用global 变量名进行声明。
本文代码：https://github.com/zwdnet/MyQuant/blob/master/44/13


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)