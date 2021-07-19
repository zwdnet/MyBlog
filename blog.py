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
        # print(s)
        os.system(s)
        # 将博客文件传回
        s = "scp ubuntu@" + server + ":~/code/*.md ."
        # print(s)
        os.system(s)
    # 将编辑好的博客文件上传并发表
    elif gpus == "post":
        s = "scp " + sys.argv[2] + ".md ubuntu@" + server + ":~/code"
        # print(s)
        os.system(s)
        s = "ssh root@" + server +  " -p 2222 \"nohup python /home/MyBlog/make.py proxy >/dev/null 2>&1 & \""
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
        
    
# 工具函数，在上传到服务器上运行时改变当前目录
def change_dir(func):
    @wraps(func)
    def change(*args, **kwargs):
        oldpath = os.getcwd()
        newpath = "/home/code/"
        os.chdir(newpath)
        r = func(*args, **kwargs)
        os.chdir(oldpath)
        return r
    return change
    
    
# 工具函数，计算函数运行时间    
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{}的运行时间为 : {}秒'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper
    