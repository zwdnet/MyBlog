---
title: '量化投资学习笔记57——通过问题学算法11:请给院子铺瓷砖（Tile That Courtyard, Please）'
date: 2020-06-01 13:10:58
tags: [量化投资, 算法, 学习笔记, 分治策略]
categories: 量化投资
---
《programming for the puzzled》第11章
涉及到的算法和语言问题：理解列表，递归进行分治搜索。
有2^n×2^n大小的院子，要用面积为3的L形的瓷砖铺满
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/39/01.png)
可以在不突破边界，不破坏瓷砖，瓷砖之间也不重叠的情况下完成吗？答案是不行，因为2^n×2^n不能被3整除，只能被2整除。而如果允许有一个方块的地方可以被剩下来，则2^2n-1则可以被3整除。
有没有一个铺砖的算法能够将任意2^n×2^n大小的院子用面积为3的L形的砖铺满只剩一个方块没铺？
归并排序是分治算法的一个例子。
要排序一个序列（如[a, b, c, d]），可以把这个序列分成两个序列([a,b], [c,d])，然后递归地对两个序列进行排序。如果序列长度为2，则比较这两个元素，结束递归。最后用一个合并的函数将两个列表合并到一起。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 11.瓷砖铺地


# 分治法，归并排序
def mergeSort(L):
    # 不加下面这行递归无法结束
    if len(L) < 2:
        return L
    if len(L) == 2:
        if L[0] <= L[1]:
            return [L[0], L[1]]
        else:
            return [L[1], L[0]]
    else:
        middle = len(L)//2
        left = mergeSort(L[:middle])
        right = mergeSort(L[middle:])
        return merge(left, right)
       
       
# 合并函数
def merge(left, right):
    result = []
    i,j = 0,0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


if __name__ == "__main__":
    L = [2, 4, 3, 9, 7, 8, 6, 4, 1, 5, 7, 3]
    res = mergeSort(L)
    print(L, "\n", res)
```
归并排序要比选择排序高效很多，其时间复杂度为nlog2n.
现在来用分治法解决铺瓷砖的问题。
首先看n=1的情况，那是2×2的地方，L形瓷砖可以占满3个，还剩一个。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/39/02.png)
这种情况就是我们分治法递归时的基本情况。
可以这么放第一个
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/39/03.png)
然后就缩小为4个更小规模的问题了。
```python
# 用递归法铺砖
EMPTYPIECE = -1

def recursiveTile(yard, size, originR, originC, rMiss, cMiss, nextPiece):
    quadMiss = 2*(rMiss >= size // 2) + (cMiss >= size // 2)
    if size == 2:
        piecePos = [(0,0), (0,1), (1,0), (1,1)]
        piecePos.pop(quadMiss)
        for (r, c) in piecePos:
            yard[originR+r][originC+c] = nextPiece
        nextPiece = nextPiece + 1
        return nextPiece
       
    for quad in range(4):
        shiftR = size//2*(quad >= 2)
        shiftC = size//2*(quad % 2 == 1)
        if quad == quadMiss:
            nextPiece = recursiveTile(yard, size//2, originR+shiftR, originC+shiftC, rMiss-shiftR, cMiss-shiftC, nextPiece)
        else:
            newrMiss = (size//2-1)*(quad<2)
            newcMiss = (size//2-1)*(quad%2 == 0)
            nextPiece = recursiveTile(yard, size//2, originR+shiftR, originC+shiftC, newrMiss, newcMiss, nextPiece)
        centerPos = [(r + size//2 - 1, c + size//2 - 1) for (r,c) in [(0,0), (0,1), (1,0), (1,1)]]
    centerPos.pop(quadMiss)
    for (r,c) in centerPos:
        yard[originR + r][originC + c] = nextPiece
    nextPiece = nextPiece + 1

    return nextPiece
   
   
def tileMissingYard(n, rMiss, cMiss):
    yard = [[EMPTYPIECE for i in range(2**n)] for j in range(2**n)]
    recursiveTile(yard, 2**n, 0, 0, rMiss, cMiss, 0)
    return yard
   

def printYard(yard):
    for i in range(len(yard)):
        row = ""
        for j in range(len(yard[0])):
            if yard[i][j] != EMPTYPIECE:
                row += chr((yard[i][j] % 26) + ord("A"))
            else:
                row += " "
        print(row)

printYard(tileMissingYard(3,4,6))
```
说实话没太懂。原理懂了，就是分治，缩小问题规模。但具体代码......先这样吧。
本章代码： https://github.com/zwdnet/MyQuant/tree/master/44


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)