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
