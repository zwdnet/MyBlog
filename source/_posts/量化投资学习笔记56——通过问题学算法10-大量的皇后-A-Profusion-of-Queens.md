---
title: '量化投资学习笔记56——通过问题学算法10:大量的皇后(A Profusion of Queens)'
date: 2020-05-29 09:06:24
tags: [量化投资, 算法, 学习笔记, N皇后问题,递归]
categories: 量化投资
---
《programming for the puzzled》第十章
涉及到的内容：递归过程，通过递归进行搜索。
在第四章我们解决了8皇后问题，现在要解决N皇后问题，即在N×N的棋盘上放N个皇后使其彼此不能互相攻击。
限制是不能写超过两层的嵌套循环。不但是因为这样的代码非常丑，它也是不能通用的。数据规模变了，你的程序也要改变。可以用递归来解决，递归是用自身定义自身。也可以是函数A调用函数B，函数B又调用函数A。
用递归来解决最大公约数问题:
首先用迭代的欧几里得算法解决：
```python
# 迭代 欧几里得算法求最大公约数
def iGcd(m, n):
    while n > 0:
        m, n = n, m%n
    return m
```
再用递归解决
```python
# 递归版本求最大公约数
def rGcd(m, n):
    if m%n == 0:
        return n
    else:
        gcd = rGcd(n, m%n)
        return gcd
```
注意两点：递归函数并不总是调用其自身，有一个基例，但出现这种情况时，返回。 参数的值随着调用不断减小。
这两点保证了递归函数一定会结束。
另一个递归的应用，斐波那契数列。
```python
# 斐波那契数列
def rFib(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return rFib(x-1) + rFib(x-2)
```
递归算法的问题是有很多重复计算的情况，用迭代算法看看。
```python
# 迭代法计算斐波那契数列
def iFib(x):
    if x < 2:
        return x
    else:
        f, g = 0, 1
        for i in range(x-1):
            f, g = g, f+g
        return g
```
下面用递归算法求解N皇后问题
可以借用8皇后的一些代码。
判断是否冲突的代码，每列用一个数字代表，-1表示该列没有皇后，0代表皇后在第一列，n-1代表皇后在最后一行。
```python
# 迭代法解N皇后问题
def noConflicts(board, current):
    for i in range(current):
        if (board[i] == board[current]):
            return False
        if (current-i == abs(board[current] - board[i])):
            return False
    return False
```
递归搜索过程 
```python
def rQueens(board, current, size):
    if (current == size):
        return True
    else:
        for i in range(size):
            board[current] = i
            if (noConflicts(board, current)):
                done = rQueens(board, current + 1, size)
                if (done):
                    return True
        return False

def nQueens(size):
    board = [-1] * size
    rQueens(board, 0, size)
    print (board)
```
算法的时间复杂度是指数级的。在放棋子的过程中就检查了是否有冲突，如果有冲突就不用接着放了。
练习1，输出棋盘，空的位置画.，下棋的位置画Q。
```python
# 画棋盘
def displayBoard(board):
    n = len(board)
    for i in range(n):
        for j in range(board[i]):
            print(".", end='')
        print("Q", end='')
        for j in range(board[i]+1, n):
            print(".", end='')
        print("\n")
```
本章代码：https://github.com/zwdnet/MyQuant/blob/master/44/10


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)