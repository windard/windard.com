---
layout: post
title: django学习笔记
description: MVC编程模式之django
category: opinion
---

之前在学习php的laravel框架时发现了MVC编程模式，发现这是未来发展发一大趋势，确实感觉叼叼哒，然后在学习其他的框架的时候发现python的django框架和nodejs的express框架也是MVC编程模式，都可以好好的学习一下。

现在这一篇是python的django的学习手册，在看django的官方手册时发现它的手册是django 1.4.3的版本，而我使用的是django1.8的版本，虽然差的不多，但是还是有很多的不同的地方。

比如说，更新数据库，在1.4.3的版本里还可以直接更新数据库，但是在django的1.8的版本里与数据库的更新全部依靠一个新的对象来完成。`python manager.py makemigrations`然后再使用`python manager.py migtate`做数据迁移。  
而以前的写法是`python manager.py sqlall modulename`和`python manager.py syncdb`。

今天发现这个语句`python manager.py syncdb`快没法用了，在django1.9的版本就会被删除了，建议用上面的那个语句。

django的删除数据库资料的语句delete没法用了，现在也不知道用什么。

在一个新的django博客系统里面，使用`python manager.py migrate`可以在数据库建表，但是需要`python manager syncdb`来创建初始用户和`python manager.py createsuperuser`来创建超级用户。

django的默认是在根目录，一般的地方不用再往上数一层了。。。   
那个教程真的有很多的问题吖，它或许只是想表达加粗的意思，所以打了俩\*\*，结果竟然一模一样的写出来了这样很容易误导其他人的吖，还有一个\*号的时候。  

发现一件好玩的事，因为之前看了一篇关于user-agent的文章，那么问题来了，你能分辨出来，下面分别是哪些浏览器么？   

```
Welcome to the page at Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2
Welcome to the page at Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2535.0 Safari/537.36
Welcome to the page at Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0
Welcome to the page at Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240
Welcome to the page at Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
Welcome to the page at Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36 OPR/32.0.1948.69
```
看起来好像是IE最有骨气的感觉~~~
