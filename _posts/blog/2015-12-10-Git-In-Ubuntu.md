---
layout: post
title: How to use git for github 
description: add git RSA-public-key to github 
category: blog
---

##How to use git in ubuntu or other linux

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

