---
layout: post
title: Ubuntu 的一些安装操作
description: 简单的记录一下，以备不时之需。
category: blog
---

## Ubuntu / Linux 目录结构

 /              根目录
├── bin     存放用户二进制文件
├── boot    存放内核引导配置文件
├── dev     存放设备文件
├── etc     存放系统配置文件
├── home    用户主目录
├── lib     动态共享库
├── lost+found  文件系统恢复时的恢复文件
├── media   可卸载存储介质挂载点
├── mnt     文件系统临时挂载点
├── opt     附加的应用程序包
├── proc    系统内存的映射目录，提供内核与进程信息
├── root    root 用户主目录
├── sbin    存放系统二进制文件
├── srv     存放服务相关数据
├── sys     sys 虚拟文件系统挂载点
├── tmp     存放临时文件
├── usr     存放用户应用程序
└── var     存放邮件、系统日志等变化文件

##PPPoE

1. 图形界面下，选择右上角的网络连接，或者在所有应用程序里找到网络连接。选择添加一个新的连接，选择DSL，进行设置就可以了。

2. 在终端中输入`sudo pppopconf`然后按照程序指导完成。

```bash
sudo pon dsl-provider	启动pppoe连接
sudo poff		停止pppoe连接
plog			查看日志
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

##一些字体的调整
虽然ubuntu-gnome的字体很好看，但是我的wps work里面用到了大量的微软雅黑字体，还是需要装一下的，本来以为很麻烦，结果就是在windows系统下的`C://Windows/fonts`下找到msyh.ttf就是微软雅黑字体了，然后装上就可以，因为我的ubuntu-gnome自带一个叫字体查看器的软件，可以用那个装字体。

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

将SSDVPS

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

##jdk && jre

1. 安装的开源版本的jdk和jre

```bash
sudo apt-get update
sudo apt-get install default-jre
sudo apt-get install default-jdk
```

2. 安装Oracle jdk

```bash
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer
sudo update-java-alternatives -s java-7-oracle
```

或者是jdk8

```bash
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo update-java-alternatives -s java-8-oracle
```

这样的安装过程一般会比较慢，也可以自己先把oracle的tar.gz的源码下载下来放在/var/cache/oracle-jdk8-installer ，然后再安装installer


最后查看是否安装成功

```bash
java -version
javac -version
```

##禁用错误提示
不知道是什么原因，总是一开机就有各种错误提示，可以取消这种提示。

```bash
sudo vim /etc/default/apport
```

将enable的值由1改为0

然后不用重启计算机，只需要重启服务就可以。

```bash
sudo service apport restart
```

##nmon
是一个可以监控当前系统性能的小工具，可以查看网络，内存，cpu，磁盘等的使用情况，感觉还是可以的。

```bash
sudo apt-get install nmon
```

##挂起后不能唤醒
ubuntu好像这个问题比较严重，一般就是当你合上笔记本电脑盖子之后，电脑就进入挂起状态，然后打开盖子就无法唤醒，之前我在网上也简单的看了一些博客，但是都比较复杂，不知道怎么弄。

但是如果笔记本不能合上这是个严重的问题的吖，如果挂起不能唤醒的话，那我们就不要挂起好了，在设置--》电源里面，把合上盖子挂起改为合上盖子忽略就好了。

##shadowsocks

###hosts
如果对翻墙的需求并不太大的情况下推荐使用更改hosts的办法来上google等网站，简单方便快速。
这里提供一个[hosts](../project/hosts)文件以供下载，还有一个稳定提供hosts文件的[站点](https://github.com/racaljk/hosts)。

这里是各种版本的[shadowsocks](https://github.com/shadowsocks/shadowsocks/wiki/Ports-and-Clients)地址

###shadowsocks

这里是shadowsocks在github上的[项目地址](https://github.com/shadowsocks/shadowsocks)，不过已经移除了全部代码。
使用pip下载安装
`sudo pip install shadowsocks`
然后编辑`/etc/shadowsocks.json`
`sudo vim /etc/shadowsocks.json`

将你的shadowsocks的配置文件编辑进去，类似于这样。

```bash
{
    "server":"xx.xx.xx.xx",
    "server_port":xxxx,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"xxxxxxxx",
    "timeout":300,
    "method":"aes-256-cfb",
}
```

各项参数的含义：
- server 服务器 IP (IPv4/IPv6)，注意这也将是服务端监听的 IP 地址
- server_port 服务器端口
- local_port 本地端端口
- password 用来加密的密码
- timeout 超时时间（秒）
- method 加密方法，可选择“bf-cfb”,“aes-256-cfb”,“des-cfb”,“rc4″,等等。默认是一种不安全的加密，推荐用“aes-256-cfb”

为了支持这些加密方式，需要安装python的一个加密模块
`sudo apt-get install python-m2crypto`

然后你就可以使用shadowsocks了，`sudo sslocal -c /etc/shadowsocks.json`

当然如果你的浏览器可能也还需要设定一下代理，或者是直接开启全局代理模式。

###shadowsock-qt5
图形化界面的shadowsocks
```bash
sudo add-apt-repository ppa:hzwhuang/ss-qt5
sudo apt-get update
sudo apt-get install shadowsocks-qt5
```

使用`sudo ss-qt5`

最后在[这里](http://www.socks163.com/?from=techzero)有一些免费的shadowsocks节点可以试一下，或者是自己搭建shadowsocks海外节点把。

## 安装问题
安装ubuntu的时候有时候会卡在`正在完成文件复制`的地方，一般是因为电脑已经联网，在网上下载安装文件，建议断开网络安装会比较快一点，安装好了之后再进入系统更新。