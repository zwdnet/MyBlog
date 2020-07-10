---
title: '量化投资学习笔记74——通过问题学算法20:六度分离(Six Degrees of Separation)'
date: 2020-07-10 14:56:41
tags: [量化投资, 算法, 学习笔记, 图算法, 广度优先搜索]
categories: 量化投资
---
《programming for the puzzled》第20章
涉及到的知识和算法：集合操作，使用集合进行广度优先图遍历。
六度分离理论指任何人与其他任意人的距离间隔在六个人以内，从世界上任何一个人开始，通过一个“从朋友到朋友”的链条可以在最多六步以内找到另一个人。每步是一度分离。“朋友”可以视为随机的两个人。要确定两个人之间的分离度，需要找到他们之间的最短关系。A有一个最好的朋友B，还有一个朋友C，C也是B的朋友，A和B之间通过C的关系的长度是2。A和B之间的分离度为1.
图的分离度是其任意两个节点中的分离度的最大值，也叫图的维度(diameter of the graph)。
问题，给定一个图，要判断其是否违反六度分离理论？
算法：从某个节点S开始，找到从S到其它所有节点的最短路径。这将会计算出S到每个其它节点的分离度。如果分离度为Ks，那么图的分离度d的取值范围为Ks≤d≤2Ks。我们可以从每个点出发进行上述程序，然后找到最大的Ks值。现在是从一个源节点出发，找到到其它节点的最短路径的算法。路径是一个边的序列。边的数量是路径的长度。采用广度优先遍历能满足我们的需要。首先从源节点到达任何一步距离的节点。这些节点形成下次搜索的起点。从这些起点中，再找到所有距离一步的节点。我们不顾虑收集已经访问过的节点——比如源节点。每个节点只纳入一次。当我们抵达所有节点，遍历结束。最后的节点就是从源节点开始的最大分离度。
每一步遍历得到的节点是一个节点的集合。即节点的顺序不重要，节点不重复。在Python中有集合类型，用{}表示。
```python
    # 测试集合操作
    frontier = {"A", "B", "D"}
    frontier.add("F")
    frontier.remove("A")
    print(frontier)
```
用集合来进行广度优先遍历
```python
# 《programming for the puzzled》实操
# 20.六度分离问题


small = {"A":["B", "C"],
                "B":["A", "C", "D"],
                "C":["A", "B", "E"],
                "D":["B", "E"],
                "E":["C", "D", "F"],
                "F":["E"]}
               
               
# 六度分离
def degreesOfSeparation(graph, start):
    if start not in graph:
        return -1
    visited = set()
    frontier = set()
    degrees = 0
    visited.add(start)
    frontier.add(start)
    while len(frontier) > 0:
        print(frontier, ":", degrees)
        degrees += 1
        newfront = set()
        for g in frontier:
            for next in graph[g]:
                if next not in visited:
                    visited.add(next)
                    newfront.add(next)
        frontier = newfront
    return degrees-1


if __name__ == "__main__":
    # 测试集合操作
    frontier = {"A", "B", "D"}
    frontier.add("F")
    frontier.remove("A")
    print(frontier)
    # 广度优先遍历
    degreesOfSeparation(small, "A")
```
再来一个大一点的图
```python
large = {'A': ['B', 'C', 'E'], 'B': ['A', 'C'],'C': ['A', 'B', 'J'], 'D': ['E', 'F', 'G'],'E': ['A', 'D', 'K'], 'F': ['D', 'N'],'G': ['D', 'H', 'I'], 'H': ['G', 'M'],'I': ['G', 'P'], 'J': ['C', 'K', 'L'],'K': ['E', 'J', 'L'], 'L': ['J', 'K', 'S'],'M': ['H', 'N', 'O'], 'N': ['F', 'M', 'O'],'O': ['N', 'M', 'V'], 'P': ['I', 'Q', 'R'],'Q': ['P', 'W'], 'R': ['P', 'X'],'S': ['L', 'T', 'U'], 'T': ['S', 'U'],'U': ['S', 'T', 'V'], 'V': ['O', 'U', 'W'],'W': ['Q', 'V', 'Y'], 'X': ['R', 'Y', 'Z'],'Y': ['W', 'X', 'Z'], 'Z': ['X', 'Y']}
```
从不同的节点开始的结果可能不一样。
```python
    degreesOfSeparation(large, "A")
    degreesOfSeparation(large, "U")
```
接下来，再写个函数计算图的分离度。
```python
# 计算一个图的分离度
def graphDegree(graph):
    vertices = graph.keys()
    maxDegree = degree = 0
    for v in vertices:
        degree = degreesOfSeparation(graph, v)
        if degree > maxDegree:
            maxDegree = degree
    return maxDegree
```

我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)