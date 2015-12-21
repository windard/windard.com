---
layout: post
title: win 10 和Ubuntu 14 双系统
description: win 10的性能比起前几代Windows已经有了很大的提高，但是还是觉得不够。  
category: blog
---

Windows 10或者说Windows操作系统如果长时间的不关机的话，都会变得非常不稳定。在之前还能坚持8天左右，后来就两三天不关机就非常不稳定了，查看系统进程`system`占用内存相当大。           

由于此，萌生了换操作系统的想法，一直在虚拟机里用Linux系统，Ubuntu使用起来感觉还是挺不错的。趁着在周六有时间，花了一下午的时间，装好了Ubuntu 14.0.4 LTS gnome的版本。               

也就不写教程了，网上一搜一堆，相互参照着看。                       

主要步骤：                   
1. Windows 10的磁盘压缩，留出足够的空间来给Ubuntu。                   
2. 制作Ubuntu系统启动盘，就是U盘里面写入Ubuntu的ISO镜像。                   
3. 关机重启。进入BIOS，设置U盘启动。                             
4. Ubuntu的安装设置，在给Ubuntu分区的时候注意给Ubuntu的启动项放对挂载点。                 
5. 使用easyBCD修复系统启动项，使电脑能够开机选择系统。                

但是本人安装的时候出了一点的问题。                  
1. 我的电脑是Dell Inspiron 14 3000 series，但是后来装了一个固态硬盘，在设置U盘启动的时候，找到U盘却无法读取还是什么鬼，停在了`boot start system ...`那个地方，于是就在U盘里写入的文件中找到`syslinux/syslinux.cfg`，打开它，将`default vesamenu.c32`给注释掉。                    

最后就是这样。                              

```
# D-I config version 2.0

include menu.cfg

# default vesamenu.c32

prompt 0

timeout 50

# ui gfxboot bootlogo

```

终于进入了Ubuntu的live CD系统。                            
后来在桌面下找到`Install`的文件，打开了才开始了正常的安装。                    

2. 果然装双系统没有那么简单，最终还是失败了。                               
在已经把easyBCD设置好了以后，在开机时选择开机启动项，但是Ubuntu那里并没有什么卵用，就停在开机的黑屏上了，至今无解。                              
另一位同学也是这个情况，换了一个Ubuntu的版本仍然不行，不知道是什么鬼。                     


参考链接：                                      
[U盘安装Windows 10和Ubuntu Linux双系统图解教程](http://www.linuxdiyf.com/linux/13140.html)

[windows10下安装Ubuntu15.04双系统](http://www.linuxdiyf.com/linux/13395.html)

[U盘安装Windows 10和Ubuntu Linux双系统图解教程](http://www.linuxdiyf.com/linux/13140.html)

[如何安装win10和linux [ubuntu14]双系统](http://jingyan.baidu.com/article/4d58d5411380dd9dd5e9c07e.html)

[win7+ubuntu双系统安装方法](http://blog.csdn.net/xlf13872135090/article/details/24093203)

[Ubuntu14.04 安装及使用：[1]制作安装U盘](http://jingyan.baidu.com/article/59703552e0a6e18fc007409f.html)

[Ubuntu14.04 安装及使用：[2]双系统安装](http://jingyan.baidu.com/article/dca1fa6fa3b905f1a44052bd.html)

[Ubuntu和win7的双系统共存之U盘装机安装图解](http://bbs.uc.cn/thread-1847133-1-1.html)
