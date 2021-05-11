import os
import sys

gpus = sys.argv[1]
os.system("mv ../code/*.md ./source/_posts/")
if gpus == "test":
    # os.system("hexo clean")
    os.system("hexo generate")
    os.system("hexo server")
elif gpus == "post":
    os.system("hexo clean")
    os.system("hexo generate")
    os.system("hexo deploy")
elif gpus == "push":  #向github同步本地项目
    os.system("rm ./nohup.out")
    os.system("nohup sslocal -c /etc/shadowsocks.json &")
    os.system("git config --global http.proxy \'socks5://127.0.0.1:1080\'")
    os.system("git config --global https.proxy \'socks5://127.0.0.1:1080\'")
    os.system("hexo clean")
    os.system("git add .")
    message = "增加了一篇博文。"
    command = "git commit -a -m"
    command += ' "'
    command += message
    command += '"'
    os.system(command)
    os.system("git push origin master")
    os.system("git config --global --unset http.proxy")
    os.system("git config --global --unset https.proxy")
elif gpus == "proxy":
    os.system("nohup sslocal -c /etc/shadowsocks.json &")
    os.system("git config --global http.proxy \'socks5://127.0.0.1:1080\'")
    os.system("git config --global https.proxy \'socks5://127.0.0.1:1080\'")
    os.system("hexo clean")
    os.system("hexo generate")
    os.system("hexo deploy")
    os.system("git config --global --unset http.proxy")
    os.system("git config --global --unset https.proxy")
elif gpus == "create":
    title = sys.argv[2]
    filename = title + ".md"
    # print(title)
    # print(filename)
    str = "hexo new \"" + title + "\""
    os.system(str)
    str = "mv ./source/_posts/" + filename + " ../code"
    # print(str)
    os.system(str)
    os.system("chown 500:500 ../code/*.md")
else:
    print("输入错误，参数必须为test,post,proxy,create+文章标题，如在本地测试用test，如上传并发布用post,如用代理上传用proxy\n")
