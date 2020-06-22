---
title: 量化投资学习笔记67——通过问题学算法17：异位词（Anagramania）
date: 2020-06-22 14:02:26
tags: [量化投资, 算法, 学习笔记, 异位词, 哈希算法]
categories: 量化投资
---
《programming for the puzzled》第17章
涉及到的数据结构：字典基础，哈希。
异位词是字母顺序变化而形成的另外的词。如cinema和iceman。我们有庞大的词语库，我们的工作是将所有的异位词找出来。我们需要将词语库划分为一些组，每组含有彼此为异位词的词语。一种方法是将词语库排序，异位词就彼此相邻。
先用最直观的算法：
对于列表中的每个词v，依次检查列表中每个与v不同的词w，如果v和w是异位词，将w移动到v之后。
```python
# 《programming for the puzzled》实操
# 17.异位词问题


def anagramGrouping(input):
    output = []
    seen = [False] * len(input)
    for i in range(len(input)):
        if seen[i]:
            continue
        output.append(input[i])
        seen[i] = True
        for j in range(i+1, len(input)):
            if not seen[j] and anagram(input[i], input[j]):
                output.append(input[j])
                seen[j] = True
               
    return output


def anagram(str1, str2):
    return sorted(str1) == sorted(str2)


if __name__ == "__main__":
    input = ["ate", "but", "eat", "tub", "tea"]
    output = anagramGrouping(input)
    print(output)
```
对于n个词，平均长度m个字母，效率为n2m log m
另一个方法，是将每个词按字母顺序排序，如果结果一样，就是异位词了。
看代码。
```python
# 排序字母法
def anagramSortChar(input):
    canonical = []
    for i in range(len(input)):
        canonical.append((sorted(input[i]), input[i]))
    canonical.sort()
    output = []
    for t in canonical:
        output.append(t[1])
    return output
```
对于n个词，平均长度m个字母，效率为nm(log m + log n)。
接下来再用哈希算法，给每个字母赋一个值，将每个词的字母的数值相加，一致的就是异位词。
```python
# 哈希算法
chToprime = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89, 'y': 97, 'z': 101 }


def primeHash(str):
    if len(str) == 0:
        return 1
    else:
        return chToprime[str[0]] * primeHash(str[1:])
        
        
def anagramHash(input):
    output = sorted(input, key=primeHash)
    return output
```
本文代码：https://github.com/zwdnet/MyQuant/blob/master/44/17


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)