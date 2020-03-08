---
title: 量化投资学习笔记29——《Python机器学习应用》课程笔记03
date: 2020-03-08 13:00:59
tags: [量化投资,Python,机器学习,K-Means算法,聚类,图像分割]
categories: 量化投资
---
聚类的实际应用，图像分割。
利用图像的特征将图像分割为多个不相重叠的区域。
常用的方法有阈值分割，边缘分割，直方图法，特定理论(基于聚类，小波分析等)。
实例:利用k-means聚类算法对图像像素点颜色进行聚类以分割图像。
输出:同一聚类的点以相同颜色表示，不同聚类的像素点以不同的颜色表示。
用PIL库从图片中读取像素点的颜色，转化到[0,1]的范围内。
```python
    f = open(filePath, "rb")
    data = []
    img = image.open(f)
    m,n = img.size
    for i in range(m):
        for j in range(n):
            x, y, z = img.getpixel((i, j))
            data.append([x/256.0, y/256.0, z/256.0])
    f.close()
```
用K-Means算法对像素点颜色数据进行聚类。
```python
    imgData, row, col = loadData("test.jpg")
    km = KMeans(n_clusters = 3)
    label = km.fit_predict(imgData)
    label = label.reshape([row, col])
```
label数据是一维的，转换成与图像相同的形状。
最后输出结果到图片，结果如下:
原图
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/23/01.png)
处理后的图片
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0178-QTLearn/23/02.png)
本文代码:
https://github.com/zwdnet/MyQuant/blob/master/27



我发文章的四个地方，欢迎大家在朋友圈等地方分享，欢迎点“在看”。
我的个人博客地址：https://zwdnet.github.io
我的知乎文章地址： https://www.zhihu.com/people/zhao-you-min/posts
我的博客园博客地址： https://www.cnblogs.com/zwdnet/
我的微信个人订阅号：赵瑜敏的口腔医学学习园地


![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/other/wx.jpg)