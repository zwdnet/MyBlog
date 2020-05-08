---
title: '量化投资学习笔记49——通过问题学算法:04N皇后问题(Keep Those Queens Apart)'
date: 2020-05-08 12:29:31
tags: [量化投资,Python,编程难题,MIT,N皇后问题,穷举,回溯]
categories: 量化投资
---
《programming for the puzzled》第四章
涉及到的问题：二维列表，while循环，continue语句，函数的默认参数，用递归进行搜索，剪枝(Conflict detection)。
就是所谓的“八皇后问题”了，在一个8×8的国际象棋棋盘上放8个皇后，要求它们不能彼此攻击，即：
①没有两个皇后在同一行。
②没有两个皇后在同一列。
③没有两个皇后在同一对角线上。
先考虑小规模的问题，5×5的棋盘上放5个皇后。
我先自己尝试一下，用穷举吧。
```python
# 穷举法
def QJ(n):
    board = [0]*n
    displayBoard(board)
    # 穷举每一种情况
    flag = False
    
    ans = []
    count = 0
    times = 0
    
    for num in range(n**n):
        temp = num
        for i in range(n):
            board[i] = int(temp % n)
            temp = temp / n
        flag = True
        
        for i in range(n):
            for j in range(i+1, n):
                if (board[i] == board[j] or abs(i-j) == abs(board[i] - board[j])):
                    flag = False
                    break
        if flag == True:
            count += 1
        times += 1
    return count, times


if __name__ == "__main__":
    n = int(input("输入问题规模:(>0)"))
    count, times = QJ(n)
    print("答案总数:", count, ",运算次数:", times)
```
还是照网上的抄的，用一维列表表示棋盘上每行放皇后的那列的位置。
再来看书里的解法，用的是二维列表表示棋盘。
关键是判断一个放法是否符合问题的三个要求。
```python
# 工具函数，检查棋子布局是否合规
def noConflicts(board, current, qindex, n):
    for j in range(current):
        if board[qindex][j] == 1:
            return False
            
    k = 1
    while qindex - k >= 0 and current - k >= 0:
        if board[qindex - k][current - k] == 1:
            return False
        k += 1
    k = 1
    while qindex + k < n and current - k >= 0:
        if board[qindex + k][current - k] == 1:
            return False
        k += 1
    
    return True
```
qindex是已经放了棋子的行的位置，相应的列的位置是current。
我自己照着书敲，老是出错，结果不对。把书的代码复制粘贴过来运行才发现是棋盘初始化出错了。
```python
# 工具函数 输出二维棋盘
def displayBoard(board):
    n = len(board)
    for i in range(n):
        print(board[i])
    print("\n")


#This procedure places 4 Queens on a board so they don't conflict
#It assumes n = 4 and won't work with other n!
def FourQueens(n=4):
    #Initialize the board to be empty
    board = [ [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0] ]
    # 照下面两行初始化会出错
    # board = [[0]*n]*n
    # print(len(board), len(board[0]))
   
    #Place a queen a column at a time beginning with leftmost column
    count, times = 0, 0
    for i in range(n):
        board[i][0] = 1
        for j in range(n):
            board[j][1] = 1
            if noConflicts(board, 1, j, n):
                for k in range(n):
                    board[k][2] = 1
                    if noConflicts(board, 2, k, n):
                        for m in range(n):
                            board[m][3] = 1
                            if noConflicts(board, 3, m, n):
                                displayBoard(board)
                                count += 1
                            times += 1
                            board[m][3] = 0
                    board[k][2] = 0
            board[j][1] = 0
        board[i][0] = 0
    return count, times
```
2维数组代表棋盘是一个很自然的想法，但由于我们在每一列仅放一个皇后（每一行也是一样的），我们可以用一维数组代表某一列放皇后的位置，而其取值代表了在该列所放皇后的行数。
每个元素的取值范围为[-1,3]，-1意味着这一列没有放棋子，0代表放在该列的第一行，3代表放在该列的最后一行。
```python
# 判断布局是否违反规则   
def noConflicts2(board, current):
    for i in range(current):
        # 每行一个
        if (board[i] == board[current]):
            return False
        # 对角线
        if (current - i == abs(board[current] - board[i])):
            return False
    return True
```
现在来做八皇后问题。
```python
# 八皇后 回溯
def EightQueens(n=8):
    board = [-1]*n
    count = 0
    for i in range(n):
        board[0] = i
        for j in range(n):
            board[1] = j
            if not noConflicts2(board, 1):
                continue
            for k in range(n):
                board[2] = k
                if not noConflicts2(board, 2):
                    continue
                for l in range(n):
                    board[3] = l
                    if not noConflicts2(board, 3):
                        continue
                    for m in range(n):
                        board[4] = m
                        if not noConflicts2(board, 4):
                            continue
                        for o in range(n):
                            board[5] = o
                            if not noConflicts2(board, 5):
                                continue
                            for p in range(n):
                                board[6] = p
                                if not noConflicts2(board, 6):
                                    continue
                                for q in range(n):
                                    board[7] = q
                                    if noConflicts2(board, 7):
                                        print(board)
                                        count += 1
    return count
```
跟前面穷举法相比，一旦遇到有冲突的落子方案，直接就pass了，快很多。
每次落子，都要调用监测是否有冲突的判断函数。
这是全书中“最丑”的代码了。可以改进的。用递归代码，在问题10的时候。
算法的核心思想是遍历所有可能的下棋方法，不遗漏任何一个可能。
另一种方法是在将布局完成后才检测其是否违反规则，而不是在下棋的过程中就检测。这种方法就是真正的穷举了，效率非常低。时间复杂度是指数级的O(n^n)。
练习1.增加一个变量，记录解的个数。我已经在上面做了。
练习2.修改代码，传入一个一维列表的下棋方式，如[-1,4,-1,-1,-1,-1,-1,0]，有两个位置已经下了棋了，输出可能的下棋方式。
增加一个判断，等于-1则按原来的赋值，如果不等于-1就跳过赋值，下下一列。但老也调不对。这种八个循环在一起是比较"丑"，过了。
本章代码： https://github.com/zwdnet/MyQuant/blob/master/44/04


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)