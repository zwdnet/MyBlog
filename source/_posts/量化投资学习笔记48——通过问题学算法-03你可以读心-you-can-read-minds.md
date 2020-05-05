---
title: '量化投资学习笔记48——通过问题学算法:03你可以读心(you can read minds)'
date: 2020-05-05 12:59:13
tags: [量化投资,Python,编程难题,MIT,编码与解码,游戏]
categories: 量化投资
---
《programming for the puzzled》第三章
本章涉及的内容：从用户获取输入，流程控制，编码和解码信息。
问题描述：你是一个魔术师和会读心术的特异功能者。你在屋外时，五位观众从52张一副的扑克里每人选了一张，你的助手收集了这五张牌。助手向所有观众展示其中的4张牌，每次一张。展示每张牌的时候，助手让观众关注在牌上，而你尝试读取他们心里所想的。过几秒后，助手向你展示这张牌。四张牌都展示完后，你离开屋子。助手向所有人展示第五张牌，并藏起来。你回来，并准确说出第五张牌是什么。原因是助手展示四张牌的顺序向你透露了第五张牌是什么。助手（而不是观众）决定展示哪四张牌，藏哪一张牌。
一个例子：假设观众选择了红心10，方块9，红心3，黑桃Q，方块J。
助手先把符号相同的两张牌检出来，五张牌至少有两张是符号相同的。在这个例子中是红心3和红心10.
助手把这两张牌放在如图所示的位置上。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/36/01.png)
任意两张牌之间顺时针的距离在1-6之间。
展示其中一张牌，另一张仍被隐藏。被展示的那张牌是顺时针能在6步或更少的步数到达另一张牌的那张牌。在这个例子里，红心10到红心3顺时针需要5步，因此红心10先被展示。
未被展示的那张牌与第一个被展示的那张牌是一个符号。其位置与第一个被展示的牌的顺时针距离在1-6之间。
所有剩下的牌被赋予一个1-6的数值。魔术师和助手事先确认桌上的牌按不同花色从小到大排列。（梅花A方块A红心A黑桃A梅花2方块2红心2黑桃2...梅花K方块K红心K黑桃K）
根据最后三张牌来赋值，规则为：
(小、中、大） =  1
(小、大、中） =  2
(中、小、大） =  3
(中、大、小） =  4
(大、小、中） =  5
(大、中、小） =  6
助手想传达的数值是6，于是助手展示剩下三张牌的顺序是黑桃Q、方块J、方块9(大中小）。于是魔术师知道从红心10开始，顺时针走六张牌，就是隐藏的红心3了。
总结一下，就是随机摸5张牌，花色相同的两张展示一张，隐藏另一张。就知道隐藏的牌的花色，再用另外三张进行排列，传递花色相同的两张牌的位置信息，就可以确定隐藏的那张牌了。
还是我自己先写，写了好长时间，主要是调试，总有bug。
```python
# coding:utf-8
# 《programming for the puzzled》实操
# 3.参加聚会的最佳时间


from random import sample


# 助手操作，展示
def AssistantOrdersCards(deck):
    choice = chooseCards(deck)
    firstResults = findFirst(choice)
    nextResults = nextCards(deck, choice, firstResults)
    firstCard = restoreData([choice[firstResults[0]]])
    hideCard = restoreData([choice[firstResults[1]]])
    displayCards = (deck[nextResults[0]], deck[nextResults[1]], deck[nextResults[2]])
    print("隐藏的牌为:", hideCard)
    print("展示的四张牌分别为:", firstCard[0], displayCards[0], displayCards[1], displayCards[2])
    return (firstCard[0], displayCards[0], displayCards[1], displayCards[2])
   
   
# 工具函数，选取五张牌，并进行数据转换
def chooseCards(deck):
    # 随机抽五张牌
    choice = sample(deck, 5)
    choice = transformData(choice)
    # 使返回的数据固定，调试用的
    # choice = [[3, 'D'], [4, 'H'], [6, 'C'], [5, 'C'], [11, 'H']]
    return choice
   
   
# 工具函数 将原始数据转换为更容易计算的形式
def transformData(cards):
    # 分割数据
    choice = [[s.split("_")[0], s.split("_")[1]] for s in cards]
    # 数据转换，将第一个数据转换为数字
    for i in range(len(choice)):
        if choice[i][0] == "A":
            choice[i][0] = 1
        elif choice[i][0] == "J":
            choice[i][0] = 11
        elif choice[i][0] == "Q":
            choice[i][0] = 12
        elif choice[i][0] == "K":
            choice[i][0] = 13
        else:     #已经是数字的了
            choice[i][0] = int(choice[i][0])
    return choice
   
   
# 工具函数，找出符号相同的两张牌，以及展示和隐藏的牌
def findFirst(cards):
    symbol = {'C':0, 'D':0, 'H':0, 'S':0}
    hide_card = ''
    for card in cards:
        symbol[card[1]] += 1
    key = max(symbol.keys(),key=(lambda x:symbol[x]))
    first = second = -1
    i = 0
    for card in cards:
        if card[1] == key:
            if first == -1:
                first = i
            elif second == -1:
                second = i
                break
        i += 1
       
    # 找出展示的牌和隐藏的牌。
    v_first = cards[first][0]
    v_second = cards[second][0]
    gap = 0
    if v_first < v_second:
        gap = v_second - v_first
        if gap > 6:
            first, second = second, first
            gap = 13 - gap
    else:
        gap = v_first - v_second
        if gap > 6:
            gap = 13 - gap
        else:
            first, second = second, first
    return (first, second, gap)
   
   
# 根据前两张牌的情况展示另外三张牌
def nextCards(deck, cards, firstResults):
    nextThree = []
    i = 0
    for card in cards:
        if i != firstResults[0] and i != firstResults[1]:
            nextThree.append(card)
        i += 1
    # 将数据恢复成原始的形式
    nextThree = restoreData(nextThree)
    index = []
    # 得到最后三张牌在原数据中的位置，用于区分大中小
    for item in nextThree:
        index.append(deck.index(item))
    result = displayOrder(index, firstResults[2])
    return result
   
   
# 根据gap值计算最后三张牌的展示顺序
def displayOrder(index, gap):
    index = sorted(index)
    small, mid, large = index[0], index[1], index[2]
    # 计算最后三张牌的展示顺序
    result = []
    if gap == 1: # 小中大
        result = [small, mid, large]
    elif gap == 2: # 小大中
        result = [small, large, mid]
    elif gap == 3: # 中小大
        result = [mid, small, large]
    elif gap == 4: # 中大小
        result = [mid, large, small]
    elif gap == 5: # 大小中
        result = [large, small, mid]
    elif gap == 6: # 大中小
        result = [large, mid, small]
    else:
        print("出错了 b")
   
    return result
   
   
# 工具函数，将数据还原会原来的样子。
def restoreData(cards):
    n = len(cards)
    for i in range(n):
        if cards[i][0] == 1:
            cards[i][0] = 'A'
        elif cards[i][0] == 11:
            cards[i][0] = 'J'
        elif cards[i][0] == 12:
            cards[i][0] = 'Q'
        elif cards[i][0] == 13:
            cards[i][0] = 'K'
        else:
            cards[i][0] = str(cards[i][0])
    result = []
    for card in cards:
        s = '_'.join(card)
        result.append(s)
    return result
   
   
# 魔术师根据cards里展示的四张牌猜牌
def MagicianGuessesCard(deck, cards):
    new_cards = [card for card in cards]
    new_cards = transformData(new_cards)
    # 先确定牌的符号，跟第一张牌一样
    symble = new_cards[0][1]
    # 下面确定牌的数值
    gap = getGap(deck, cards)
    # 计算隐藏的牌的数值
    num = new_cards[0][0] + gap
    if num > 13:
        num = num - 13
    # 数值和符号都有了，可以合并得到结果了。
    result = [[num, symble]]
    result = restoreData(result)
    return result
   
   
# 工具函数，根据牌的顺序确定前两张牌的间隔
def getGap(deck, cards):
    index = []
    for i in range(1, 4):
        index.append(deck.index(cards[i]))
    new_index = sorted(index)
    small, mid, large =new_index[0], new_index[1], new_index[2]
    # 根据三张牌排列情况计算gap值
    if index == [small, mid, large]: # 小中大
        gap = 1
    elif index == [small, large, mid]: # 小大中
        gap = 2
    elif index == [mid, small, large]: # 中小大
        gap = 3
    elif index == [mid, large, small]: # 中大小
        gap = 4
    elif index == [large, small, mid]: # 大小中
        gap = 5
    elif index == [large, mid, small]: # 大中小
        gap = 6
    else:
        print("出错了 a")
    return gap
   


if __name__ == "__main__":
    deck = ['A_C','A_D','A_H','A_S',
                  '2_C','2_D','2_H','2_S',
                  '3_C','3_D','3_H','3_S',
                  '4_C','4_D','4_H','4_S',
                  '5_C','5_D','5_H','5_S',
                  '6_C','6_D','6_H','6_S',
                  '7_C','7_D','7_H','7_S',
                  '8_C','8_D','8_H','8_S',
                  '9_C','9_D','9_H','9_S',
                  '10_C','10_D','10_H','10_S',
                  'J_C','J_D','J_H','J_S',
                  'Q_C','Q_D','Q_H','Q_S',
                  'K_C','K_D','K_H','K_S']
    cards = AssistantOrdersCards(deck)
    result = MagicianGuessesCard(deck, cards)
    print("猜牌结果为:", result)
```
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/36/02.png)
终于对了。但是很繁琐，有200多行。再看看作者写的，思路跟我差不多，也是将近200行。就不搬过来了。这种程序，算法不难，调试了好长时间，很多地方都是加一减一的错误。
一个更难的问题，只选四张牌能不能玩这个游戏？因为可能四张牌符号都不同，一个解决方法是把52张牌都放到那个圈里，一定有两张牌小于等于13。具体不再实现了。
练习也pass了，实在不喜欢这个题目。视频课程里现场玩了这个游戏。
本章代码： https://github.com/zwdnet/MyQuant/blob/master/44/03



我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)