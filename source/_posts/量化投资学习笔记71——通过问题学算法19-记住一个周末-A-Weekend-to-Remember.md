---
title: '量化投资学习笔记71——通过问题学算法19:记住一个周末(A Weekend to Remember)'
date: 2020-06-29 14:50:15
tags: [量化投资, 算法, 学习笔记, 图算法, 深度优先搜索]
categories: 量化投资
---
《programming for the puzzled》第19章
涉及到的算法：使用字典表示图，深度优先遍历图。
你要在连续的两个晚上邀请你的朋友们来聚会，并且想把互相不喜欢的两个人邀请到不同的聚会。即：1.你的每个朋友必须出席两个聚会中的一个；2.如果A不喜欢B或者B不喜欢A，他们不能在同一个聚会中。
可以用图来代表你的社交网络，顶点是你的朋友，两个人之间有边代表两个人彼此讨厌对方。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/46/01.png)
但有的情况下，如下图
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/46/02.png)
FGH三个人就没法安排在两个聚会里。
问题就是找到一个图的分割。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/46/03.png)
如果一个图可以用两种颜色涂顶点，并使有共同边的两个顶点的颜色不一样，这个图就是可二分的。(bipartite)
检查一个图是否是二分图的算法，用深度优先搜索：
1.color = Shaded, 顶点 = 开始顶点w。
2.如果w没有被涂，将w涂上颜色。
3.如果w已经被涂了不同的颜色，图不是可以二分的，返回False。
4.如果w已经被涂正确的颜色，返回True和（未修改的）颜色。
5.翻转颜色：将涂与不涂颜色的顶点翻转到其反面。
6.对w的每个邻顶点v，递归调用该过程，以v和颜色为参数（如到第二步，w = v）。如果任何递归调用返回False，就返回False。
7.图是可二分的，返回True和颜色。
选择数据结构表示图。用Python的字典结构来表示。
像这样：
graph = {'B': ['C'],
'C': ['B', 'D'],
'D': ['C', 'E', 'F'],
'E': ['D'],
'F': ['D', 'G', 'H', 'I'],
'G': ['F'],
'H': ['F'],
'I': ['F']}
```python
# 《programming for the puzzled》实操
# 19.周末聚会问题


# 判断图是否为二分图
def bipartiteGraphColor(graph, start, coloring, color):
    if start not in graph:
        return False, {}
       
    if start not in coloring:
        coloring[start] = color
    elif coloring[start] != color:
        return False, {}
    else:
        return True, coloring
       
    if color == 'Sha':
        newcolor = 'Hat'
    else:
        newcolor = 'Sha'
       
    for vertex in graph[start]:
        val, coloring = bipartiteGraphColor(graph, vertex, coloring, newcolor)
        if val == False:
            return False, {}
       
    return True, coloring


if __name__ == "__main__":
    dangling = {"A":["B", "E"],
                         "B":["A", "E", "C"],
                         "C":["B", "D"],
                         "D":["C", "E"],
                         "E":["A", "B", "D"]}
    res, col = bipartiteGraphColor(dangling, "A", {}, "Sha")
    print(res, col)
```
没啥意思，感觉。还剩两章。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)