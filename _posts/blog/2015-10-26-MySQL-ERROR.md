---
layout: post
title: MySQL数据库错误
description: [ERROR] Fatal error: Can't open and lock privilege tables: Table 'mysql.user' doesn't exist
category: blog
---

这个错误挺难找的，，找到错误并弄好了之后得出了两点结论。
1. 报错了要去看错误日志，以前从来不看那东西的，然而还是要翻出来看一看，错误的原因非常详细的记录在上上面，很重要的。
2. 问题是多变的，网上的答案是不变。在看了别人的解答过程之后，要自己思考根据实际去解决问题。

>如果再加一点的话，就是，没事不要在Windows上装直接MySQL。

一开始我本来是想简简单单在Windows上装个MySQL而已的，结果发现它装上之后就成了自启动服务了，占了我的3306端口不说，而且开机自启动。   
这一点非常不好，我决定要把它关掉。  

也是在网上找了很多资料，终于在MySQL的官方文档里找到了，（这里说一点，很多官方文档都是英文的，习惯去看。），发现了这个语句`mysql -u root shutdown;`当然，此时你在MySQL里面。  
>cmd登陆mysql的语句就是`mysql -u uername -p passwd`  

好了，成功的关掉了，结果就再也没有打开了。  

这里补充说明一下我的MySQL的情况，因为我一般不喜欢把软件装在C盘，所以就把MySQL放在D盘`D:\Program Files (x86)`下，看了网上的安装教程，好像转好了之后需要配置一下my.ini，（这里有一点非常坑爹吖！这个配置文件是什么鬼，好像在Linux下是叫做my.cof么？还是版本太老的原因），将`basedir`和`datadir`设为你自己想要放的文件的位置。  

结果我就欢喜也设定在了D盘相同的位置下。  
```shell
basedir = D:\\Program Files (x86)\\MySQL\\MySQL Server 5.7
datadir = D:\\Program Files (x86)\\MySQL\\MySQL Server 5.7\\data
```
而且我看很多的网上教程里没有说的关于斜杠`\`与反斜杠`/`的问题，但是我在MySQL的官方文档里面看到是要按照我的这种写法，在Windows下。  

然后我想再次开启MySQL的时候就悲剧了，先是在普通的cmd下启动MySQL，提示错误`发生系统错误 5。拒绝访问。`我想在cmd里打开mysql也报错`ERROR 2003 (HY000): Can't connect to MySQL server on 'localhost' (10061)`  

在网上搜了一下，发生这个问题的原因是在MySQL中没有安装mysqld服务的原因，需要在cmd的管理员身份下进入MySQL的bin目录，安装mysqld.`mysqld --iinstall`我记得好像在一开始我是安装过了的，果然回复我已安装了这个，然后网上教程是用`net start mysql`这是正常的开启MySQL的语句（当然，还是在cmd管理员身份下）。  
所以之前的拒绝访问的原因应该是我没有管理员身份权限吧，ERROR2003应该是我还没有开数据库。那现在应该差不多了吖~~  
结果，新的报错，`MySQL启动失败，服务器未给出任何错误原因`，卧槽！，怎么会这样，竟然没有任何错误原因啊！那你为什么开不了吖！  
我还以为是因为cmd有缓存，关掉cmd重开了一个（因为有的时候，更改了电脑的某些设置，确实是在当前的cmd中没有反应的，比如说环境变量，需要关掉再开就好了），结果还是不行。  

开不了就算了，竟然还不报错，你这让我去网上搜也搜不到吖！  
正准备放弃，看到了MySQL的错误日志文件，打开看看。实在是好长的错误日志，而且几乎把MySQL事无巨细全部的过程都记录了下来，找到ERROR的位置，虽然在cmd中显示未报错，但是在错误日志中还是如实的写下来错误的原因，是什么导致它不能够正常启动。  
`[ERROR] Fatal error: Can't open and lock privilege tables: Table 'mysql.user' doesn't exist`  
于是有问题就好办了嘛，把这个问题直接丢到谷歌里面去搜，找到一些解决办法，但是都是在Linux下的，有一个在Windows下的也比较简略，想了一想最后自己解决了。

**解决办法**
虽然在`my.ini`文件里的`datadir`是你设置的在某个地方，但是在一开始的时候，Windows会默认把它放在`C:\ProgramData\MySQL\MySQL Server 5.7`目录下，这是一个隐藏目录，注意查看。  
所以在你的第一次使用的时候data数据放在了这里，关掉再次启动的时候就会去找你设定的新位置，当然就找不到了  
把这里的data移到你设定的`datadir`的地方，再次在管理员的cmd里面执行`net start mysql `就可以了~~

哦也\\(\^o\^)/ over。


:-(
最后附上一个忘记密码更改MySQL密码的方法，希望大家不会用到。
1. 以管理员身份启动cmd。
```
#先关掉MySQL服务
net stop mysql
#以安全模式运行MySQL
mysqld --skip-grant-tables  
```
2. 不要关闭，再启动一个新的cmd命令窗口,可以是管理员身份或者一般身份
```
#使用储存密码的数据库
use mysql;
#更改密码
update user set authentication_string=password("123456") where user="root";  
```
此处我在网上的教程里面看到有的在`authentication_string`处用的是`password`，不知道是什么原因，但是我的MySQL里面没有`password`这一项。  
3. 关闭以上两个窗口，启动MySQL服务，即以管理员身份运行cmd。
```
net start mysql
```

>在Linux下基本一致，除了启动和关闭MySQL的方法有一些区别，和第一步以安全模式运行MySQL，在Linux下是`mysqld_safe --skip-grant-tables &  `

