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

本来看了一下网上的教程，发现竟然可以使用自带的网络连接来创建wifi热点（虽然 windows也可以用自带的程序创建wifi热点），那我想应该比windows下要简单的一些，结果发现弄一半天并不能弄好。

自带的网络连接创建的并不是AP而是AP-hoc，安卓手机或者苹果手机都并不能够使用。那我要你有何用！

后来看到好像用ap-hotspot可以创建wifi热点，结果报错`Your wireless card or driver does not support Access Point mode`

再用kde-nm-connection可以创建热点，结果还是不行，因为不能使用AD模式。

再一看，使用`ifconfig`只有`eth0 eth1 lo ppp0`，知道了。我的ubuntu的网卡驱动都没有，因为如果有驱动的话，起码应该还能够看到一个`wlan0`这是网卡驱动的接口。

或者是用`iwconfig`就可以查看无线网络的情况，不过我的就显示没有无线网络。

用`lspci`可以看到所有的设备信息，不过没什么卵用，反正我看不懂。

用`lspci | grep -i network`可以看到`06:00.0 Network controller: Broadcom Corporation BCM43142 802.11b/g/n (rev 01)
`这就是我的无线网卡的信息了，Broadcom公司的BCM43142型网卡。

然后竟然在Boradcom的官网里找不到我的网卡的驱动，难道我要自己写驱动么？我勒个擦～～

[这里](https://help.ubuntu.com/community/WifiDocs/WirelessCardsSupported)是ubuntu无线驱动支持一览表。

卧槽，竟然在ubuntu软件中心发现了可以安装驱动，在附加驱动的地方，找到了我的无线网卡确实是缺少了一个驱动了，但愿可以找到一个驱动然后给装上吧。

再次使用`ifconfig`就出现了wlan0，太棒了，折腾了一半天终于装好了驱动，接下来就是使用AP了。

