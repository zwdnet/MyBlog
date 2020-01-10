---
title: 量化投资学习笔记07——python知识补漏
date: 2020-01-10 08:49:06
tags: [量化投资,python,读书笔记,学习笔记]
categories: 量化投资
---
看《量化投资:以python为工具》这本书，第一部分是python的基础知识。这一部分略读了，只看我还不知道或不熟的。
定义复数
```python
x = complex(2, 5) #2+5j
```
也可以直接定义
```python
y = 3-6j
```
用id()可以得到变量的内存地址
```python
z = 3-6j
print(id(y), id(z))
```python
y和z的内存地址是一样的。
```python
531269809744 531269809744
```
python可以为不可变对象分配固定的内存，减少内存占用。
当两个变量指向同一对象时，is比较结果为True。当两个变量指向的对象值相等时，==为True。
如果函数参数为可变对象，在函数内部改变此对象会影响函数外部。
```python
def testChange(x, y):
  x[0] = "A"
  y = 7
  
 x = ["a", "b", "c", "d"]
 y = 6
 testChange(x, y)
 print(x, y)
```
使用个数不定的参数，可以提前打包，或者使用不定参数传递，方法是在参数前加*
```python
def manyCan(*arg):
  sum = 0
  for i in arg:
   sum = sum+i
  return sum
  
 print(manyCan(1,2,3))
```
匿名函数，无需使用def来定义的函数，使用lambda来定义。
```python
# 匿名函数
 greeting = lambda : print("hello")
 greeting()
```
若字符串中包含单引号或双引号，要将整个字符串用三个引号包含。
文本分析时，应将字符串完全转换成小写再分析。
字典对象的keys()函数查看键值，values()函数返回值。
```python
# 字典测试
 dictest = {"High":5, "Low":1, "Close":3}
 print(dictest)
 for key in dictest.keys():
  print(key)
  print(dictest[key])
```
用del语句可以删除特定键及其对应值，用clear()方法则删除整个字典，返回空字典。
Python集合有set和frozenset两种，均不含重复元素，前者可变，后者不可变。
set用add()和remove()来增删成员。
使用arange创建array是不包含终点值的，要包含终点值，使用linspace。
不知道初始值时，用zeros(), ones()或empty()创建。
通过切片索引提取的array与原array共享内存，通过整型索引提取则不与原数组共享内存。
每个series对象实际上都由两个数组组成:index和values。
时间序列的index属性的取值为时间戳。用Timestamp()来将datetime转换为时间戳。由于其不接受列表等可迭代对象，用to_datetime()函数。
滞后操作:将t期数据换成t-a期数据。
超前操作:将t期数据换成t+a期数据。
标签索引与切片，用loc[行标签,列标签]
位置索引与切片，用iloc[行标签,列标签]
混合上述两者，用ix。(但python提示ix将被废弃)

我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的微信个人订阅号：赵瑜敏的口腔医学学习园地

![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)
