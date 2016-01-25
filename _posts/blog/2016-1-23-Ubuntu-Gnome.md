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

具体的看我的另外两篇博客。友情提示，sublime需要用到python，所以sublime 2就对应python2.X，sublime 3就对应python3.X 还是有一定区别的，推荐sublime2。

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

##一些快捷方式的调整
有一些常用的在windows下非常习惯的快捷方式在ubuntu下有的不一样，这个肯定要改过来。

比如说锁屏，在windows下是home键加L键，可是在ubuntu上确实home键加Alt键加L键，果断改之。

还有我的电脑，在windows下是home键加E键，在ubuntu下没有这个选项，自己创建一个快捷方式好了，就是`nautilus /home/windard`。

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

##虽然ubuntu-gnome的字体很好看，但是我的wps work里面用到了大量的微软雅黑字体，还是需要装一下的，本来以为很麻烦，结果就是在windows系统下的`C://Windows/fonts`下找到msyh.ttf就是微软雅黑字体了，然后装上就可以，因为我的ubuntu-gnome自带一个叫字体查看器的软件，可以用那个装字体。

so easy的装好了字体之后，把sublime换成了微软雅黑的字体，还是挺漂亮的。

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

有一个叫TLP的电池管理软件，可以一试。

```bash
sudo add-apt-repository ppa:linrunner/tlp
sudo apt-get update
sudo apt-get install tlp tlp-rdw
sudo tlp start
```

顺便可以调整一下电池充电阈值，好的充电阀值参数能更好维护电池的寿命。

编辑默认设置。

```bash
sudo gedit /etc/default/tlp
```

将
```
#START_CHARGE_THRESH_BAT0=50
#STOP_CHARGE_THRESH_BAT0=99
```
去掉注释，并改为你想要的值。我在第一个写的是50，第二个是90。
```bash
sudo tlp ac 此命令意思为开启电源模式.
sudo tlp bat 此命令意思为开启电池模式.
sudo tlp stat 查看TLP工作情况
sudo tlp-stat -C 查看TLP配置情况
sudo tlp usb 开启USB电池管理模式
```

最后，因为我不确定这个是不是开机启动的，所以我把它加到了开机启动。

sudo hdparm -B /dev/sda 可见硬盘/dev/sda的APM_level值为254,表示硬盘性能最大化,这需要保持高水平的硬盘转速,硬盘发热量自然就大. 

如果返回/dev/sda: APM_level = not supported,则表示你的硬盘不支持APM(高级电源管理). 

APM_level的全称为Advanced Power Management level,即(硬盘)高级电源管理级别. 

该值的取值范围为1~255,值越大,硬盘性能越高,其中255表示关闭硬盘/dev/sda的电源管理,254表示在开启电源管理下的最高性能,1表示最低的硬盘性能但最省电。

这个值在1~127区间时允许spin-down,在128~254这个区间则禁止spin-down. 
>spin-down是指在闲置时挂起硬盘,停止转动,但是频繁的spin-down和spin-up会使硬盘寿命变短. 

在上面的tlp设置里面有这个选项，我把第一个设为了192，第二个设为了128.

```bash
 DISK_APM_LEVEL_ON_AC="192 192"
 DISK_APM_LEVEL_ON_BAT="128 128"
```