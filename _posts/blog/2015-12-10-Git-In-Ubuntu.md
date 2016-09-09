---
layout: post
title: How to use git for github 
description: add git RSA-public-key to github 
category: blog
---

## How to use git in ubuntu or other linux

Actually,what I want to say it how to add RSA-public-key to github.

Git can be used to push code to github,even it hasn't be authereian.

It just need you post your account username and password each time.

At begin ,I hadn't add my key to github successful,so I need to post my account information each time .

It's too boring.

Now I add it to my github account successful . so push my code to github will be easier 

Great!     

首先，你要有一个github帐号和在你的机器上有git客户端。           

然后，如果你已经有在本地生成过RSA，那就先删掉原有的。

原有的公钥一般在`~/id_rsa.pub`或者是`~/.ssh/id_rsa.pub`这是公钥，就是说可以公开的，也就是这个应该被放到你的github帐号里做双向绑定。

原有的私钥一般在`~/id_rsa`或者是`~/.ssh/id_rsa`这是私钥，也就是说不能让别人知道的，但是你自己可以看一下。无论是公钥还是私钥都是文本文件，可以用`cat`命令查看。

现在我们就可以生成我们自己的RSA密钥了。             

```
ssh-keygen -t rsa -C "email@gmail.com"
```

将邮箱地址换成你自己的邮箱地址。

>在生成密钥的时候会提醒你密钥的保存地点，默认是在`~`下。                    
>在生成密钥的时候也会要求你输入一个密码，但是这个密码不是你的github密码，是用来锁定你的本地账户的，在每次提交项目的时候使用。                              
>在生成密钥之后，你就会发现目录下多了两个文件`id_rsa`和`id_rsa.pub`，前者是私钥，后者是密钥。                                  

然后登录你的github帐号，在右上角的`Settings`里的`SSH keys`选择`Add SSH key`,然后把你的`id_rsa.pub`里的内容放进去。

最后，验证是否加入成功。

```
ssh -T git@github.com
```

如果返回：`Hi XXX! You've successfully authenticated, but GitHub does not provide shell access.`

即说明公钥添加成功。以后你克隆github上的代码就可以使用github专用通道了，每次上传自己的代码也不用再输入用户名和密码了。     

>最后的最后                                  
>或许你还需要设定一个本地用户信息                                     
>`git config --global user.name "yourusername"`                                 
>`git config --global user.email "youremail"`                                

github专用通道即：                                                     
一般克隆代码是`git clone https://github.com/XXX/XXX.git`                               
现在就可以这样`git clone git@github.com:XXX/XXX.git`                             

## 管理多个 git 账号

最近在树莓派上使用 Gogs 搭建了一个私有的 Git 服务器，感觉还是挺方便的，在这么低的配置上跑 Git 服务器没有任何问题，Gogs 是用 Go 语言写的，需要的依赖非常少，可以很轻易的搭建在各种平台上。

不过我平常用 Github 也比较多，这样的话 Github 和 Gogs 两个 Git 账号，不能使用同一个 RSA 密钥，这样的话 Git 账号管理也是一个问题。

虽然还是可以使用 https 协议与 Github 连接，用 http 协议与 Gogs 连接，但是用 Git 还是要好一些。

以下来自于 Windows 10 ，使用 git 和 ssh 。

先来生成两个密钥文件。

```
C:\Users\dell\.ssh
λ ssh-keygen.exe -t rsa -f ./gogs_rsa -C 1106911190@qq.com
C:\Users\dell\.ssh
λ ssh-keygen.exe -t rsa -f ./github_rsa -C 1106911190@qq.com
```

然后分别把 `github_rsa.pub` 和 `gogs_rsa.pub` 里的内容提交到 Github 和 Gogs 上，设定 SSH 密钥。

> 注意提交公钥时不要多加了最后的换行，并没有换行

然后创建一个 配置文件，在不同的站点下使用不同的密钥文件。

```
Host github.com
  hostname github.com
  User windard
  #port 22
  IdentityFile C:\Users\dell\.ssh\id_rsa
  

Host 192.168.0.103
  HostName 192.168.0.103
  User windard
  IdentityFile C:\Users\dell\.ssh\gogs_rsa
```

最后，验证是否加入成功。

```
C:\Users\dell\.ssh
λ ssh -T git@github.com
Enter passphrase for key 'C:\Users\dell\.ssh\id_rsa':
Hi windard! You've successfully authenticated, but GitHub does not provide shell access.
C:\Users\dell\.ssh
λ ssh -T pi@192.168.0.103
Enter passphrase for key 'C:\Users\dell\.ssh\gogs_rsa':
Hi there, You've successfully authenticated, but Gogs does not provide shell access.
If this is unexpected, please log in with password and setup Gogs under another user.
```

即都加入成功
