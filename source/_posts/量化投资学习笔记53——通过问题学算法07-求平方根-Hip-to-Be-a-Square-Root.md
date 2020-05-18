---
title: '量化投资学习笔记53——通过问题学算法07:求平方根(Hip to Be a Square Root)'
date: 2020-05-18 14:43:48
tags: [量化投资,Python,编程难题,MIT,二分法,分治法]
categories: 量化投资
---
《programming for the puzzled》第七章
涉及到的知识浮点数和算术运算，二分搜索。
问题:找到一组数的平方根。
迭代搜索
已知一个数n是完全平方数，可以从1开始计算其平方值，如果小于n，加一，再重复，直到其平方值等于n。这对于计算机来说是可行的，但还有更快的解法。
先实现这个算法吧。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 7.找平方根


# 线性复杂度算法
def findSquareRoot(n):
    if n < 0:
        print("要输入非负整数")
        return -1
    i = 0
    while i*i < n:
        i += 1
    if i*i == n:
        return i
    else:
        print(n, "不是完全平方数")
        return -1


if __name__ == "__main__":
    n = int(input("输入一个完全平方数:"))
    res = findSquareRoot(n)
    if res != -1:
        print(res,"*", res, "=", n)
    else:
        print("输入有误。")
```
现在进行改进，输入数据包括最小误差，步长，不把答案局限在整数解，求小数解。
```python
# 改进，增加答案精度，指定精度和步长
def findSquareRoot2(n, eps, step):
    if n < 0:
        print("要输入非负整数")
        return -1, 0
    numGuesses = 0.0
    ans = 0.0
    while n - ans**2 > eps:
        ans += step
        numGuesses += 1
    if abs(n - ans**2) > eps:
        # print("求解", n, "的平方根失败")
        print(n, ans**2, n - ans**2, eps)
        return -1, numGuesses
    else:
        print("b")
        # print(ans, "是", n, "的近似平方根")
        return ans, numGuesses
```
有时求解会失败，原因是循环跳过了答案。解决办法是减小每次迭代的递增值。但这会显著增加运行时间。
处理浮点数要注意，它们可能不像你想象的那样运行。
改进方法是用分治法，像上一章那样。
思路是，如果猜了一个数，其平方值比n小，那么所有大于该数的值都排除了，反过来可以排除所有小于该值的值。
```python
# 二分搜索
def bisectionSearchForSquareRoot(n, eps):
    if n < 0:
        print("要输入非负整数")
        return -1, 0
    numGuesses = 0
    low = 0.0
    high = n
    ans = (high + low)/2.0
    while abs(ans**2 - n) >= eps:
        if ans**2 < n:
            low = ans
        else:
            high = ans
        ans = (high + low)/2.0
        numGuesses += 1
    return ans, numGuesses
```
比第一种算法快得多，而且不会出现跳过答案，求解失败的情况。这里面隐含了一个性质，如果x>y>0, x^2>y^2>0。
另一个例子，二分查找。一个有序的数列，要找到一个数是否在这个数列里。
```python
# 线性查找
NOTFOUND = -1
Ls = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
def Lsearch(L, value):
    for i in range(len(L)):
        if L[i] == value:
            return i
    return NOTFOUND
   
   
# 二分查找
def bsearch(L, value):
    lo, hi = 0, len(L) - 1
    while lo <= hi:
        mid = (lo+hi)//2
        if L[mid] < value:
            lo = mid + 1
        elif value < L[mid]:
            hi = mid - 1
        else:
            return mid
    return NOTFOUND
```
在一些问题里，三分查找更方便。
练习1，当n=0.25或者n<1-eps的情况，二分搜索会失败。找到原因并解决。
```python
# 二分搜索改进版
def bisectionSearchForSquareRoot2(n, eps):
    if n < 0:
        print("要输入非负整数")
        return -1, 0
    numGuesses = 0
    low = 0.0
    # high = n
    high = max(n, 1.0)
    ans = (high + low)/2.0
    while abs(ans**2 - n) >= eps:
        if ans**2 < n:
            low = ans
        else:
            high = ans
        ans = (high + low)/2.0
        numGuesses += 1
        # print(low, high, ans, numGuesses, ans**2-n, eps)
        # input("按任意键继续")
    return ans, numGuesses
```
当n小于1时，答案可能不在计算的[low, high]区间里。
练习2.在bsearch里增加一个变量，记录搜索的区间长度。当列表长度小于一定值的时候，使用二分搜索还不如使用顺序搜索。
```python
# 二分查找
def bsearch(L, value):
    lo, hi = 0, len(L) - 1
    length = hi
    while lo <= hi:
        mid = (lo+hi)//2
        if L[mid] < value:
            lo = mid + 1
        elif value < L[mid]:
            hi = mid - 1
        else:
            return mid
        # 练习2
        length = hi-lo
        print("当前搜索区间长度:", length)
    return NOTFOUND
```
练习3.修改bisection程序找到方程x**3+x**2-11的解，误差给定（如0.01）。你也许需要从一个跨过0的区间开始，如[-10, 10]。
```python
# 练习3，求方程的根
def fun(x):
    return x**3 + x**2 - 11
    
    
def findRoot(eps):
    lo, hi = -10, 10
    mid = (hi + lo)/2.0
    count = 0
    while abs(fun(mid)) > eps:
        if fun(lo)*fun(mid) < 0:
            hi = mid
        elif fun(mid)*fun(hi) < 0:
            lo = mid
        mid = (hi + lo)/2.0
        count += 1
        # print(lo, mid, hi, count, abs(fun(mid)))
        # input("按任意键继续")
    return mid
```

我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)