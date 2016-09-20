---
layout: post
title: win 10 和Ubuntu 14 双系统
description: win 10的性能比起前几代Windows已经有了很大的提高，但是还是觉得不够。  
category: blog
---

## 安装双系统

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
但是这个失败应该是与我的双硬盘有关，我的电脑里有一个固态硬盘加一个机械硬盘，果然就没有能够装起来，后来我给我的同学装虚拟机，就成功了，他的电脑里只有一个硬盘。                  

3. 在经过一番折腾了之后，终于把双系统装好了。网上的教程都是没有问题的，我用网上的教程给我的同学装双系统，一次就成功了。但是不知道是我的电脑的原因，还是固态硬盘的原因，在我的电脑上遇到了很大阻碍。

因为我的电脑里有机械硬盘和固态硬盘，我的原来的windows是装在固态硬盘上的，然后因为我的固态硬盘的空间满了，也不想把ubuntu和windows装在一起，所以就准备把ubuntu全部装在机械硬盘里。

问题就出现这里。ubuntu当然是可以装在机械硬盘里，但是因为我的电脑的启动项只认固态硬盘，也就是说我的ubuntu可以装在机械硬盘里，不过/boot启动项必须在固态硬盘里，不然就识别不出现，显示找不到。

因为这个原因，我的电脑装了好几遍，最后终于找到问题。把ubuntu的/ ,/home ,swap等几个分区装在机械硬盘里，但是/boot启动项装在固态硬盘里，然后就好了。


参考链接：                                      
[U盘安装Windows 10和Ubuntu Linux双系统图解教程](http://www.linuxdiyf.com/linux/13140.html)

[windows10下安装Ubuntu15.04双系统](http://www.linuxdiyf.com/linux/13395.html)

[如何安装win10和linux [ubuntu14]双系统](http://jingyan.baidu.com/article/4d58d5411380dd9dd5e9c07e.html)

[win7+ubuntu双系统安装方法](http://blog.csdn.net/xlf13872135090/article/details/24093203)

[Ubuntu14.04 安装及使用：[1]制作安装U盘](http://jingyan.baidu.com/article/59703552e0a6e18fc007409f.html)

[Ubuntu14.04 安装及使用：[2]双系统安装](http://jingyan.baidu.com/article/dca1fa6fa3b905f1a44052bd.html)

[Ubuntu和win7的双系统共存之U盘装机安装图解](http://bbs.uc.cn/thread-1847133-1-1.html)
