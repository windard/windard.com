---
layout: post
title: Ubuntu 的一些安装操作 
description: 简单的记录一下，以备不时之需。  
category: blog
---

##PPPoE

###1. 图形界面下，选择右上角的网络连接，或者在所有应用程序里找到网络连接。选择添加一个新的连接，选择DSL，进行设置就可以了。

###2. 在终端中输入`sudo pppopconf`然后按照程序指导完成。

```bash
sudo pon dsl-provider	启动pppoe连接
sudo poff				停止pppoe连接
plog					查看日志
ifconfig	ppp0		查看接口信息

```

##WIFI 热点
