---
title: '量化投资学习笔记59——通过问题学算法12:汉诺塔（The Towers of Brahma with a Twist）'
date: 2020-06-02 16:44:52
tags: [量化投资, 算法, 学习笔记, 递归算法, 汉诺塔]
categories: 量化投资
---
涉及到的算法知识：递归每次减1的搜索。
学计算机的都很熟悉这个问题了：一根柱子上从小到大放着一堆盘子，要通过一个辅助的柱子把盘子转移到另一根柱子上，要求大盘子不能放在小盘子上面。每次只能移动一个盘子。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/40/01.png)
递归的解法，是先把除了最下面最大的盘子以外的其它盘子转移到辅助柱子上，然后把最大的盘子放到目标柱子上，剩下的盘子在重复这个过程，只是盘子数量少了一个。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/40/02.png)
写程序吧
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 12.汉诺塔


def hanoi(numRings, startPeg, endPeg):
    numMoves = 0
    if numRings > 0:
        numMoves += hanoi(numRings-1, startPeg, 6-startPeg-endPeg)
        print("从", startPeg, "到", endPeg, "移动", numRings, "号盘子。")
        numMoves += 1
        numMoves += hanoi(numRings-1, 6-startPeg-endPeg, startPeg)
    return numMoves


if __name__ == "__main__":
    hanoi(3, 1, 3)
```
关键点是，知道了起始的柱号，终止的柱号，用6减去它们两个就是辅助的柱号。（因为三者之和始终是6。）
这么写缺少了基础的情况，即只剩一个盘子时的情况，这时只用移动两次。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 12.汉诺塔


def hanoi(numRings, startPeg, endPeg):
    numMoves = 0
    if numRings == 1:
        print("从", startPeg, "到", 6-startPeg-endPeg, "移动", numRings, "号盘子。")
        print("从", 6-startPeg-endPeg, "到",startPeg , "移动", numRings, "号盘子。")
        numMoves += 2
    else:
        print("从", startPeg, "到", endPeg, "移动", numRings, "号盘子。")
        numMoves += hanoi(numRings-1, startPeg, 6-startPeg-endPeg)
        print("从", startPeg, "到", endPeg, "移动", numRings, "号盘子。")
        numMoves += 1
        numMoves += hanoi(numRings-1, 6-startPeg-endPeg, startPeg)
    return numMoves


if __name__ == "__main__":
    numMoves = hanoi(8, 1, 3)
    print("步数等于:", numMoves)
```
对n个盘子，需要移动的次数是3^n-1次，是指数级的。
本文代码：https://github.com/zwdnet/MyQuant/blob/master/44/12


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)