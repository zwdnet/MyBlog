---
title: '量化投资学习笔记50——通过问题学算法:05请打碎那颗水晶(Please Do Break the Crystal)'
date: 2020-05-10 13:19:52
tags: [量化投资,Python,编程难题,MIT,进制运算]
categories: 量化投资
---
《programming for the puzzled》第五章
涉及到的知识：break语句，基数运算(radix representations)
问题概述：测量一些水晶球的“硬度系数”。2015年完工的上海塔有128层，你要找出从多高的地方扔下这些水晶球，它们不会破碎而是弹起来。返回的结果是满足条件的最高的楼层数。比如你返回的是f，则从f层扔水晶不会破碎，从f+1层扔就会了。水晶球一旦破碎，就不能重复使用。球的速度是决定其是否破碎的唯一因素，随着层数的上升，速度增加。你可以假设当球从x层扔出时没有破碎，那它从小于x的楼层扔出也不会破碎。而从大于x的楼层扔出则肯定会破碎。但你不能坐电梯，因此你希望能最小化扔球的次数。如果只有一个球，从第一层扔着来，如果在n层它碎了，你报告的就是n-1，可能的次数是128次。如果是两个球，第一个在128层扔，碎了，第二个从第一层扔，一直可能到127层，需要扔的次数还是128。一个改进是从中间64层开始扔，碎了，从下扔，没碎，从上扔。最差的情况是扔64次。对于2个球，你能想到办法最大化你的报酬，并在21次尝试之前结束吗？如果你有更多水晶球？如果上海塔突然高度增加了一倍呢？
我自己想的结果:就是二分法查找嘛，但是只用两个球，确实想不到比64次更少的尝试方法。看看作者怎么说。
考虑从20层开始扔，碎了，从1到19层扔，总的次数最坏是20。没碎，可以从40层扔，如此重复。能否找到一个与楼层数n相关的函数func(n)，代表扔的最多少的次数。对于最坏的情况，球一直不破直到最后一次扔，第一个球要在第k,2k,3k,...,(n/k-1)k, (n/k)k层扔出，第一个球要扔n/k次，第二个球要扔k-1次，即总的扔的次数为n/k+k-1次。因此要找到一个k使得n/k+k-1最小。（用求导算一下，f(k) = n/k+k-1, f'(k) = -n/k² +1，当f'(k) = 0时，k = sqrt(n)，书上没有这些。）因此当k为n的平方根时取最小值，对于128层，当k=11时扔的次数最小，最坏的情况下要扔21次。
现在来考虑水晶球数量增加的情况。作者的做法是有d个球就用d位数字来代表，进制r则根据使r^d > n的最小的r来选择。例如对于d = 4个球，3^4 = 81 < 128, 4^4 = 256 > 128，所以r = 4。在1000（四进制）层扔第一个，假设其在第2000（四进制）碎了，扔第二个球从1100（四进制，在十进制中为80层）开始扔，以此类推，搜索范围逐渐变小。扔的最少次数为d(r-1)。
写一个程序，实现上述算法，对于给定的n和d，给出从哪层开始扔，扔的次数最少。然后，根据扔的结果（碎或不碎），程序告诉我们要扔的新的楼层（没碎），或者告诉我们结果（碎了）。最后还要告诉我们扔的总次数。
分析的好复杂啊，尤其用进制那个。直接看作者写的代码吧。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 5.打碎水晶


def howHardIsTheCrystal(n, d):
    r = 1
    while (r**d < n):
        r += 1
    print("选择的基数为", r)
    numDrops = 0
    floorNoBreak = [0]*d
    for i in range(d):
        for j in range(r-1):
            floorNoBreak[i] += 1
            Floor = convertToDecimal(r, d, floorNoBreak)
            if Floor > n:
                floorNoBreak[i] -= 1
                break
            print("从", Floor, "层扔下第", i+1, "个球。")
            yes = input("水晶球裂了吗?(yes/no):")
            numDrops += 1
            if yes == "yes":
                floorNoBreak[i] -= 1
                break
                
    hardness = convertToDecimal(r, d, floorNoBreak)
    print("硬度为:", hardness)
    print("扔球的总数为:", numDrops)
    
    return
    
    
def convertToDecimal(r, d, rep):
    number = 0
    for i in range(d-1):
        number = (number + rep[i])*r
    number += rep[d-1]
    
    return number


if __name__ == "__main__":
    howHardIsTheCrystal(128, 4)
```
练习1到练习3，都是对代码的改动或增加新功能，直接放程序了。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 5.打碎水晶


def howHardIsTheCrystal(n, d):
    r = 1
    while (r**d < n):
        r += 1
    print("选择的基数为", r)
    # 练习1，有时d太大，会跳过第一个球
    # 减少d的值
    newd = d
    while (r**(newd-1) > n):
        newd -= 1
    if newd < d:
        print("只用了", newd, "个球")
    d = newd
   
    numDrops = 0
    # 练习2 输出坏了的球
    numBreaks = 0
    # 练习3，输出正在考虑的楼层区间
    start = 0
    end = n
    floorNoBreak = [0]*d
    for i in range(d):
        for j in range(r-1):
            # 练习3，输出正在考虑的区间
            print("正在考虑", start, "到", end, "的楼层。")
            floorNoBreak[i] += 1
            Floor = convertToDecimal(r,  d, floorNoBreak)
            if Floor > n:
                floorNoBreak[i] -= 1
                break
            print("从", Floor, "层扔下第", i+1, "个球。")
            yes = input("水晶球裂了吗?(yes/no):")
            numDrops += 1
            if yes == "yes":
                floorNoBreak[i] -= 1
                end = Floor-1
                break
            # 练习2
            else:
                numBreaks += 1
                start = Floor+1
               
    hardness = convertToDecimal(r,  d, floorNoBreak)
    print("硬度为:", hardness)
    print("扔球的总数为:", numDrops)
    # 练习2
    print("扔坏了的球的个数为:", numBreaks)
   
    return
   
   
def convertToDecimal(r,  d, rep):
    number = 0
    for i in range(d-1):
        number = (number + rep[i])*r
    number += rep[d-1]
   
    return number


if __name__ == "__main__":
    howHardIsTheCrystal(128, 6)
```
这章的问题感觉比较奇怪，怎么想到用不同进制来代表不同的球数的?看看视频吧。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)