# coding:utf-8
# 在服务器上创建发布博客文章
import os
import sys
from functools import wraps
import time


# 在服务器上创建博客并发布
def run(gpus, server):
    # 在服务器上创建博客并复制到本地
    if gpus == "create":
        # 运行创建代码
        s = "ssh root@" + server +  " -p 2222 \"python /home/MyBlog/make.py create \"" + sys.argv[2] + "\"" + "\""
        # print("测试:", s)
        os.system(s)
        # 将博客文件传回
        s = "scp ubuntu@" + server + ":~/code/*.md ."
        # print(s)
        os.system(s)
        # 删除服务器上的博客文件
        s = "ssh ubuntu@" + server +  " \"rm  ~/code/*.md\""
        # print("测试:", s)
        os.system(s)
    # 将编辑好的博客文件上传并发表
    elif gpus == "post":
        # 不上传，直接发表
        if len(sys.argv) <= 2:
            s = "ssh root@" + server +  " -p 2222 \"nohup python /home/MyBlog/make.py post " + " >/dev/null 2>&1 & \""
            # print(s)
            os.system(s)
        else:#上传文件并发表
            s = "scp " + sys.argv[2] + ".md ubuntu@" + server + ":~/code"
            # print(s)
            os.system(s)
            s = "ssh root@" + server +  " -p 2222 \"nohup python /home/MyBlog/make.py post \"" + sys.argv[2] + "\" >/dev/null 2>&1 & \""
            # print(s)
            os.system(s)

    # 将博客源码上传至github
    elif gpus == "push":
        s = "ssh root@" + server +  " -p 2222 \"python /home/MyBlog/make.py push\""
        # print(s)
        os.system(s)
    else:
        print("输入错误，第一个参数应为create, post和push之一，第二个参数为博客文章标题。")


if __name__ == "__main__":
    gpus = sys.argv[1]
    # 读取服务器IP地址，自己编辑serverIP.txt去
    with open("serverIP.txt", "rt") as f:
        server = f.read()
    run(gpus, server)
