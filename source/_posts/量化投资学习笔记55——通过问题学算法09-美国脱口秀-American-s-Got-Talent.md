---
title: '量化投资学习笔记55——通过问题学算法09:美国脱口秀(American''s Got Talent)'
date: 2020-05-25 14:46:09
tags: [量化投资, 算法, 学习笔记, 集合覆盖问题]
categories: 量化投资
---
《programming for the puzzled》第九章
使用列表表示二维表格。
你计划举办一个脱口秀电视节目，你进行了面试，很多面试者声称有一些特殊技能（跳舞，插花等）。大多数人并不能让你满意，但是还是有一些满意的。现在你有一些至少能表演一次脱口秀的候选者。
你有一张所有候选人和他们的技能的列表，你要在你的节目中安排这些技能。要使节目多样化并降低成本，要有最少的候选者并使技能多样化。因此你要找到能演出所有节目的数量最少的候选人组合。
像这样的表格
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/38/01.png)
可以选择Aly, Bob, Done, Eve，就可以覆盖所有节目。要求找到最少的人数组合。在本例中，Aly, Cal, Eve就行。
解法跟上一章差不多，先找出所有的组合方式，排除不能覆盖所有节目的组合，再从剩下的组合中找出人数最少的。注意用贪心法是不行的。
数据结构，用二维列表表示候选人和其所会的节目。
有一个节目列表，一个候选人列表，以及一个每位候选人所会的节目的二维列表。其顺序与候选人列表的顺序一致。
首先生成所有候选人组合方式
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 9.脱口秀节目


Talents = ["Sing", "Dance", "Magic", "Act", "Flex", "Code"]
Candidates = ["Aly", "Bob", "Cal", "Don", "Eve", "Fay"]
CandidateTalents = [ ['Flex', 'Code'], ['Dance', 'Magic'], ['Sing', 'Magic'], ['Sing', 'Dance'], ['Dance', 'Act', 'Code'], ['Act', 'Code'] ]
                                   
                                
# 生成所有候选人组合
def Hire4Show(candList, candTalents, talentList):
    n = len(candList)
    hire = candList[:]
    for i in range(2**n):
        Combination = []
        num = i
        for j in range(n):
            if (num % 2 == 1):
                Combination = [candList[n-1-j]] + Combination
            num = num // 2

        if Good(Combination, candList, candTalents, talentList):
            if len(hire) > len(Combination):
                hire = Combination

    print ('Optimum Solution:', hire)
           
               
def Good(Comb, candList, candTalents, AllTalents):
    for tal in AllTalents:
        cover = False
        for cand in Comb:
            candTal = candTalents[candList.index(cand)]
            if tal in candTal:
                cover = True
        if not cover:
            return False
    return True

                                   
if __name__ == "__main__":
    Hire4Show(Candidates, CandidateTalents, Talents)
```
这个问题是“集合覆盖问题”的一个例子。这是一个很难的问题，时间复杂度是指数级的。

练习略了。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)