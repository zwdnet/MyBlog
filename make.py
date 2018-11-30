import os
import sys

gpus = sys.argv[1]
if gpus == "test":
    os.system("hexo clean")
    os.system("hexo generate")
    os.system("hexo server")
elif gpus == "post":
    os.system("hexo clean")
    os.system("hexo generate")
    os.system("hexo deploy")
elif gpus == "push":  #向github同步本地项目
    os.system("hexo clean")
    os.system("")
else:
    print("输入错误，参数必须为test或者post，如在本地测试用test，如上传并发布用post\n")
