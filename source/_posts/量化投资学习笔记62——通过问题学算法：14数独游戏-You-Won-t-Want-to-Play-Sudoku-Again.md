---
title: 量化投资学习笔记62——通过问题学算法：14数独游戏(You Won't Want to Play Sudoku Again)
date: 2020-06-09 12:10:06
tags: [量化投资, 算法, 学习笔记, 递归算法, 数独]
categories: 量化投资
---
《programming for the puzzled》第14章
涉及到的算法：全局变量，集合和集合操作。使用递归进行搜索。
游戏规则：9×9的格子，用1-9一共9个数去填格子，使得每行，每列，以及每个3×3的区域都含有1-9这9个数字。其中一些格子已经包含了数字。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/41/01.png)
基本解决方法：猜一个数，看是否满足条件。不满足，换另一个。
```python
# 《programming for the puzzled》实操
# 14.数独问题


backtracks = 0


# 递归解数独
def solveSudoku(grid, i=0, j=0):
    global backtracks
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            backtracks += 1
    grid[i][j] = 0
    return False


# 找到下一个格子
def findNextCellToFill(grid):
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1
   
   
# 判断i,j格子能否放数字e。
def isValid(grid, i, j, e):
    # 检查行
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        # 检查列
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # 检查小方块
            secTopX, secTopY = 3*(i//3), 3*(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if grid[x][y] == e:
                        return False
            return True
    return False
   
   
# 输出数独
def printSudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print(" ")
        print(row[0:3], " ", row[3:6], " ", row[6:9])
        numrow += 1


if __name__ == "__main__":
    input = [[5, 1, 7, 6, 0, 0, 0, 3, 4],
    [2, 8, 9, 0, 0, 4, 0, 0, 0],
    [3, 4, 6, 2, 0, 5, 0, 9, 0],
    [6, 0, 2, 0, 0, 0, 0, 1, 0],
    [0, 3, 8, 0, 0, 6, 0, 4, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 7, 8],
    [7, 0, 3, 4, 0, 0, 5, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    solveSudoku(input)
    printSudoku(input)
    print("尝试次数:", backtracks)
```
上述解法并没有考虑利用输入的所有信息，比如如上图中第二行和第三行都有8了，而在3×3的小方格中，只有中间那个小方格还没有8，所以第一行的8一定在中间小格，因此只能在第5列的位置。
下面是优化后的数独解法
```python
backtracks2 = 0
# 递归解数独，使用隐含信息
def solveSudokuOpt(grid, i=0, j=0):
    global backtracks2
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True
    for e in range(1, 10):
        if isValid(grid, i, j, e):
            impl = makeImplications(grid, i, j, e)
            if solveSudoku(grid, i, j):
                return True
            backtracks2 += 1
            undoImplications(grid, impl)
    return False
   
   
def undoImplications(grid, impl):
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = 0
       
       
sectors = [[0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3],[0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6],[0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9]]


def makeImplications(grid, i, j, e):
    global sections
    grid[i][j] = e
    impl = [(i, j, e)]
    for k in range(len(sectors)):
        sectinfo = []
        vset = {1,2,3,4,5,6,7,8,9}
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if grid[x][y] != 0:
                    vset.remove(grid[x][y])
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if grid[x][y] == 0:
                    sectinfo.append([x, y, vset.copy()])
        for m in range(len(sectinfo)):
            sin = sectinfo[m]
            rowv = set()
            for y in range(9):
                rowv.add(grid[sin[0]][y])
            left = sin[2].difference(rowv)
            colv = set()
            for x in range(9):
                colv.add(grid[x][sin[1]])
            left = left.difference(colv)
            if len(left) == 1:
                val = left.pop()
                if isValid(grid, sin[0], sin(1), val):
                    grid[sin[0]][sin[1]] = val
                    impl.append((sin[0], sin[1], val))
    return impl
```
空间换效率啊，代码比前一个复杂很多。
本文代码：https://github.com/zwdnet/MyQuant/blob/master/44/14




我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)