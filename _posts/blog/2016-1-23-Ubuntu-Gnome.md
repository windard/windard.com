---
layout: post
title: Ubuntu 的一些安装操作 
description: 简单的记录一下，以备不时之需。  
category: blog
---

##PPPoE

××1. ××图形界面下，选择右上角的网络连接，或者在所有应用程序里找到网络连接。选择添加一个新的连接，选择DSL，进行设置就可以了。

××2. ××在终端中输入`sudo pppopconf`然后按照程序指导完成。

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

再用kde-nm-connection-editor可以创建热点，结果还是不行，因为不能使用AD模式。

再一看，使用`ifconfig`只有`eth0 eth1 lo ppp0`，知道了。我的ubuntu的网卡驱动都没有，因为如果有驱动的话，起码应该还能够看到一个`wlan0`这是网卡驱动的接口。

或者是用`iwconfig`就可以查看无线网络的情况，不过我的就显示没有无线网络。

用`lspci`可以看到所有的设备信息，不过没什么卵用，反正我看不懂。

用`lspci | grep -i network`可以看到`06:00.0 Network controller: Broadcom Corporation BCM43142 802.11b/g/n (rev 01)
`这就是我的无线网卡的信息了，Broadcom公司的BCM43142型网卡。

然后竟然在Boradcom的官网里找不到我的网卡的驱动，难道我要自己写驱动么？我勒个擦～～

[这里](https://help.ubuntu.com/community/WifiDocs/WirelessCardsSupported)是ubuntu无线驱动支持一览表。

卧槽，竟然在ubuntu软件中心发现了可以安装驱动，在附加驱动的地方，找到了我的无线网卡确实是缺少了一个驱动了，但愿可以找到一个驱动然后给装上吧。

再次使用`ifconfig`就出现了wlan0，太棒了，折腾了一半天终于装好了驱动，接下来就是使用AP了。

结果没有成功，暂时放弃

##git
与github上传下载

```bash
sudo apt-get install git
```

后续操作看我另外一篇博客

##sublime 
相当好的代码编辑器，或者是你可以用它来编辑任何你想编辑的东西。
具体的看我的另外两篇博客

##vim
竟然系统不自带vim，这个可以有。
具体的vimrc看我的另外一篇博客的配置。

##F.lux
这是我在windows下也用的护眼软件，能够自动的根据时间来调节电脑屏幕的亮度，觉得挺不错的。没想到竟然也有linux版本，肯定要接着使用。

```bush
sudo add-apt-repository ppa:kilian/f.lux
sudo apt-get update
sudo apt-get install fluxgui
```

然后把它加到开机启动项里去，`gnome-session-properties`（启动应用程序）

##shutter
截图工具，虽然用gnome-screenshot 也可以截图，但是这个功能更强大一点。

```bash
sudo apt-get install shutter
```

##ubuntu-tweak 
跟windows下的电脑管家比较类似。

```bash
sudo add-apt-repository ppa:tualatrix/ppa
sudo apt-get update
sudo apt-get install ubuntu-tweak
```

##为知笔记

```bash
sudo add-apt-repository ppa:wiznote-team
sudo apt-get update
sudo apt-get install wiznote
```

##更新LibreOffice
把LibreOffice的英文界面改成中文
```bash
sudo apt-get install libreoffice-l10n-zh-cn libreoffice-help-zh-cn
```


##独显还是集显

貌似看到网上说ubuntu的显卡驱动不太完善，电池耗电量颇大，对电池伤害严重以及图形化界面不稳定等问题。
主要出现在ubuntu的集显和独显双显卡问题上，说是双显卡支持不好。吓得我赶紧照着网上的教程把独显给关了。

查看显卡状态：

```bash
cat /sys/kernel/debug/vgaswitcheroo/switch  
```

我也不知道网上别人的是什么样子，但是我的是这样的，DIS是独显，IGD是集显，其他的我也不知道是什么意思。

```bash
0:DIS: :DynOff:0000:08:00.0
1:IGD:+:Pwr:0000:00:02.0
```

然后使用一下命令先使用root权限，然后切换到集成显卡，最后关掉独立显卡。

>一般集成显卡就是intel自带的显卡，支持的好一些，简称i卡，独立显卡就是nvidia的显卡，简称n卡，跟linux的感情不太好。

```bash
sudo su

echo IGD > /sys/kernel/debug/vgaswitcheroo/switch
echo OFF > /sys/kernel/debug/vgaswitcheroo/switch
```

别人这样之后的效果就是这样，DIS表示的独显已经关闭了。

```bash
0:IGD:+:Pwr:0000:00:02.0
1:DIS: :Off:0000:01:00.0
```

但是我的再看一下结果还是原来的那个样子，并没有变化的说。

```bash
0:DIS: :DynOff:0000:08:00.0
1:IGD:+:Pwr:0000:00:02.0
```

后来又找到说那个DynOff表示的是动态关闭的。好高端～～在ubuntu14.04之后的系统又高级了一些。刚好我的ubuntu就是14.04的LTS版本。。

```bash
OFF: The device is powered off
ON: The device is powered on
DynOff: The device is currently powered off but will be powered on when needed
DynPwr: The device is currently powered on but will be powered off when not needed
```

好吧，如果有使用ubuntu14.04以前的同学可以看一下，还可以把上面那个关闭独显只开集显的命令加入到开机启动里去，这样的话就不用自己的关了。

加入到开机启动里就是把
```bash
echo IGD > /sys/kernel/debug/vgaswitcheroo/switch
echo OFF > /sys/kernel/debug/vgaswitcheroo/switch
```
加入到`/etc/rc.local`里的exit 0之前就可以了。

不过我的独显在ubuntu下确实一般用不到，暂不管他。

##电池管理

说道独显和集显就是因为电池和磁盘容易受损，着实是我也觉得我的电池耗电有点快了。

看到网上有一个教程说是设置磁盘转速，有一个说是设置swap分区使用率。看到用的人好像不太多，想想就算了。

有一个叫TPL的电池管理软件，可以一试。

```bash
sudo add-apt-repository ppa:linrunner/tlp
sudo apt-get update
sudo apt-get install tlp tlp-rdw
sudo tlp start
```


