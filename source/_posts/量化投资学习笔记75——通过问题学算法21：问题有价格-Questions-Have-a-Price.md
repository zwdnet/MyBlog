---
title: 量化投资学习笔记75——通过问题学算法21：问题有价格(Questions Have a Price)
date: 2020-07-13 13:01:46
tags: [量化投资, 算法, 学习笔记, 二叉搜索]
categories: 量化投资
---
《programming for the puzzled》第20章
涉及到的知识和算法：面向对象变成，二叉搜索树
问题描述：你的朋友想一个从1到7的数字，你要用最少的猜测次数猜到这个数。接着你朋友猜你想的数字。猜的次数少的人赢。猜的时候，对方会提示高了，低了，还是正确。
可以用二叉搜索来解决。对于小于7的数字，最多猜3次。
可以用二叉搜索树来表示猜测过程，从中间的数字(4)开始，4为根节点，小于4的数字在左子树，大于4的数字在右子树。你朋友也知道这些内容，因此你们获胜的概率一样。但是后来你发现你的朋友想的数字都是奇数的，因为奇数都在最下一层。于是你给不同的数字不同的概率，根节点4的概率为0，第一层子树(2,6)的概率是0.1,第二层（即底层，1,3,5,7）的概率为0.2。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/49/01.png)
能否创建一个新的二叉搜索树使得可以猜测更少的次数。即构造一个二叉搜索树使得weight = ΣPr(i)(D(i) + 1)， D(i)是数字i在树中的深度。
这是结果：
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/49/02.png)
树的深度是比上面第一颗树大1.
可以使用字典来表示树，key是每个节点，值是这个节点的子节点。
用面向对象的方法封装树的操作。
```python
# 《programming for the puzzled》实操
# 21.猜数字问题


# 封装二叉搜索树操作
class BSTVertex:
    def __init__(self, val, leftChild, rightChild):
        self.val = val
        self.leftChild = leftChild
        self.rightChild = rightChild
       
    def getVal(self):
        return self.val
       
    def getLeftChild(self):
        return self.leftChild
       
    def getRightChild(self):
        return self.rightChild
       
    def setVal(self, newVal):
        self.val = newVal
       
    def setLeftChild(self, newLeft):
        self.leftChild = newLeft
       
    def setRightChild(self, newRight):
        self.rightChild = newRight
       
       
class BSTree:
    def __init__(self, root = None):
        self.root = root
       
    def lookup(self, cVal):
        return self.__lookupHelper(cVal, self.root)
       
    def __lookupHelper(self, cVal, cVertex):
        if cVertex == None:
            return False
        elif cVal == cVertex.getVal():
            return True
        elif (cVal < cVertex.getVal()):
            return self.__lookupHelper(cVal, cVertex.getLeftChild())
        else:
            return self.__lookupHelper(cVal, cVertex.getRightChild())
           
    def insert(self, val):
        if self.root == None:
            self.root = BSTVertex(val, None, None)
        else:
            self.__insertHelper(val, self.root)
           
    def __insertHelper(self, val, pred):
        predLeft = pred.getLeftChild()
        predRight = pred.getRightChild()
        if (predRight == None and predLeft == None):
            if val < pred.getVal():
                pred.setLeftChild((BSTVertex(val, None, None)))
            else:
                pred.setRightChild((BSTVertex(val, None, None)))
        elif (val < pred.getVal()):
            if predLeft == None:
                pred.setLeftChild((BSTVertex(val, None, None)))
            else:
                self.__insertHelper(val, pred.getLeftChild())
        else:
            if predRight == None:
                pred.setRightChild((BSTVertex(val, None, None)))
            else:
                self.__insertHelper(val, pred.getRightChild())
               
    def inOrder(self):
        outputList = []
        return self.__inOrderHelper(self.root, outputList)
       
    def __inOrderHelper(self, vertex, outList):
        if vertex == None:
            return
        self.__inOrderHelper(vertex.getLeftChild(), outList)
        outList.append(vertex.getVal())
        self.__inOrderHelper(vertex.getRightChild(), outList)
        return outList
          


if __name__ == "__main__":
    # 测试二叉搜索树类
    root = BSTVertex(22, None, None)
    tree = BSTree(root)
    print(tree.lookup(22))
    tree.insert(25)
    tree.insert(35)
    tree.insert(9)
    print(tree.lookup(25))
    outres = tree.inOrder()
    print(outres)
```
现在来解决我们的问题。用贪心算法，把概率最大的节点放到根节点。
```python
# 解决猜数字问题
def optimalBST(keys, prob):
    n = len(keys)
    opt = [[0 for i in range(n)] for j in range(n)]
    computeOptRecur(opt, 0, n-1, keys)
    tree = createBSTRecur(None, opt, 0, n-1, keys)
    print("平均最小猜测次数:", opt[0][n-1][0])
    printBST(tree.root)
   
   
def computeOptRecur(opt, left, right, prob):
    if left == right:
        opt[left][left] = (prob[left], left)
        return
    for r in range(left, right+1):
        if left <= r-1:
            computeOptRecur(opt, left, r-1, prob)
            leftval = opt[left][r-1]
        else:
            leftval = (0, -1)
        if r+1 <= right:
            computeOptRecur(opt, r+1, right, prob)
            rightval = opt[r+1][right]
        else:
            rightval = (0, -1)
        if r == left:
            bestval = leftval[0] + rightval[0]
            bestr = r
        elif bestval > leftval[0] + rightval[0]:
            bestr = r
            bestval = leftval[0] + rightval[0]
    weight = sum(prob[left:right+1])
    opt[left][right] = (bestval + weight, bestr)
   
   
def createBSTRecur(bst, opt, left, right, keys):
    if left == right:
        bst.insert(keys[left])
        return bst
    rindex = opt[left][right][1]
    rnum = keys[rindex]
    if bst == None:
        bst = BSTree(None)
    bst.insert(rnum)
    if left <= rindex-1:
        bst = createBSTRecur(bst, opt, left, rindex-1, keys)
    if rindex+1 <= right:
        bst = createBSTRecur(bst, opt, rindex+1, right, keys)
    return bst
   
   
def printBST(vertex):
    left = vertex.leftChild
    right = vertex.rightChild
    if left != None and right != None:
        print("值=", vertex.val, "左子节点=", left.val, "右子节点=", right.val)
        printBST(left)
        printBST(right)
    elif left != None and right == None:
        print("值=", vertex.val, "左子节点=", left.val, "右子节点=", "None")
        printBST(left)
    elif left == None and right != None:
        print("值=", vertex.val, "左子节点=", "None", "右子节点=", right.val)
        printBST(right)
    else:
        print("值=", vertex.val, "左子节点=", "None", "右子节点=", "None")

keys = [i+1 for i in range(7)]
    pr = [0.2, 0.1, 0.2, 0.0, 0.2, 0.1, 0.2]
    optimalBST(keys, pr)
```
这样整本书就完了，基本的数据结构都讲了，跟着书把代码敲了一遍当练习“语感”吧。


我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)