---
title: 安卓手机python程序开发利器——Pydroid3
date: 2019-02-26 17:09:09
tags: [安卓,python,Pydroid3]
categories: 计算机
---

作为非专业程序员写程序，往往不方便使用电脑，而智能手机几乎人手一部的。我就在想有没有能在安卓手机上写python程序的应用。经过搜索，有好几个办法。一个是安装termux终端，然后在里面安装配置python环境，但是编辑源程序是一个问题，用vim等编辑器毕竟没有在电脑上按键方便。还有一个方法是安装pydroid3应用。在手机自带的应用市场和豌豆荚等第三方应用市场里都搜不到这个应用，在谷歌官方应用市场里有，但是要root手机还要科学上网。我在搜索引擎里搜到apk文件，自行下载后安装了。
安装以后打开是这样
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/01.png)
就可以在里面写python程序了
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/02.png)
点右上文件夹样的图标，选择保存，就可以讲源文件保存到手机内存里了。然后点右下角的那个三角形按钮就可以运行程序了。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/03.png)
OK，中文也可以正常显示的!使用的是免费版，有时会有弹窗(但并不频繁)，点返回键就没了，也没有其它乱七八糟的广告。大家有条件可以购买以支持。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/04.png)
有简单的编辑功能，但自然比不上PC里的IDE啦。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/05.png)
现在再来看看左上那个菜单里的选项
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/06.png)
第一个是python命令行解释器，可以交互式运行python程序。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/07.png)
点左上的白色箭头或者输入exit()就返回了。
第二项是打开一个linux终端
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/08.png)
可以输入Linux命令。
关键是看第三项，是安装库的方法。
很多库可以一键安装
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/09.png)
对于快速安装里没有的库，选搜索库，输入库的名称查找。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/10.png)
然后选安装就行啦。但是并不是每个库能安装成功的，也许是硬件的限制，比如tensorflow就装不了(解决方法在最后)。但是常用的库都能装。
示例里有很多范例程序，甚至还能写安卓界面程序，这个大家感兴趣可以自行尝试。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/11.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/12.png)
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/13.png)
最后再来看看作图，先写一个绘图程序。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/14.png)
运行
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/15.png)
并没有图像出现。我想到一个变通的方法:把图象保存到文件里再手动打开。
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/16.png)
再运行，手机内存里就多了个"hello.png"的文件，打开
![](https://zymblog-1258069789.cos.ap-chengdu.myqcloud.com/blog0103-pydroid3/17.png)
搞定!图例用中文是乱码，要折腾字体，我就有英文做图例吧。
这就是pydroid3的基本使用了。再配合在termux里装个git，就可以用github了。至于装不上tensorflow等库的问题，我现在的解决方法是买vps服务器，在服务器上配置python开发环境和jupyter notebook服务器，在浏览器里输IP地址就可以用了。具体做法限于篇幅就先不说了。
写本文是因为crossin编程教室公众号搞了个征稿活动，我就把这个安卓手机上的python编程利器分享给大家，不是说分享就是最好的学习吗？别再只拿手机吃鸡了!😂
我发文章的三个地方，欢迎大家在朋友圈等地方分享，欢迎点“好看”。谢谢。我是牙医，公众号和博客的内容大多是关于我的专业口腔医学的，计算机的内容在csdn博客里，目前是关于量化投资学习的内容，有七篇了。
我的个人博客地址：https://zwdnet.github.io
我的CSDN博客地址：https://blog.csdn.net/zwdnet
我的微信个人订阅号：赵瑜敏的口腔医学学习园地
