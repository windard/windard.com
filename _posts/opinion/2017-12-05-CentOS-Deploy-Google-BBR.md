---
layout: post
title: CentOS 上开启 BBR 加速
description: Google TCP BBR 拥塞控制算法做流量控制，快如闪电
category: opinion
---

因为众所周知的原因，要用国外的主机作为节点，但是一直速度都比较慢。

使用过锐速等方式来加速，但是效果都不太理想，很早就听说过 BBR 算法，[Linux Kernel 4.9 中的 BBR 算法与之前的 TCP 拥塞控制相比有什么优势](https://www.zhihu.com/question/53559433/answer/135903103)，终于试了一把，确实不同凡响。

简单的说就是 BBR 算法放弃了原来的TCP连接的窗口重传算法，使用新的流量控制算法，尽可能的占满网络请求带宽。

BBR 算法需要 Linux 4.9 及以上的内核支持，所以想要使用该方式的需要先升级内核版本。

在 Cent OS 7 上的 Linux 内核是 3.10, 使用 `uname -r` 查看内核版本

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# uname -r
3.10.0-327.22.2.el7.x86_64
```

> 据说 OpenVZ 的机器也不支持，使用 virt-what 查看虚拟化方式

## 升级内核版本

安装 eprl 的源

```
sudo rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
sudo rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
```

安装最新的内核版本，截止目前最新的都到 4.14

```
sudo yum --enablerepo=elrepo-kernel install kernel-ml -y
```

看一下系统现在所有的内核 `rpm -qa | grep kernel`

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# rpm -qa | grep kernel
kernel-3.10.0-327.el7.x86_64
kernel-3.10.0-327.22.2.el7.x86_64
kernel-tools-libs-3.10.0-327.el7.x86_64
kernel-tools-3.10.0-327.el7.x86_64
kernel-ml-4.14.3-1.el7.elrepo.x86_64
kernel-headers-3.10.0-514.2.2.el7.x86_64
```

可以看到最新的内核版本 `kernel-ml-4.14.3-1.el7.elrepo.x86_64` 已经安装好了。

现在来修改 grub2 的启动项，设置启动之后选择最新的内核， `sudo egrep ^menuentry /etc/grub2.cfg | cut -f 2 -d \'` .

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# sudo egrep ^menuentry /etc/grub2.cfg | cut -f 2 -d \'
CentOS Linux (4.14.3-1.el7.elrepo.x86_64) 7 (Core)
CentOS Linux (3.10.0-327.22.2.el7.x86_64) 7 (Core)
CentOS Linux (3.10.0-327.el7.x86_64) 7 (Core)
CentOS Linux (0-rescue-7d26c16f128042a684ea474c9e2c240f) 7 (Core)
```

启动顺序已经修改了，但是为了以防万一，我们还是设置一下 `sudo grub2-set-default 0` ，选择第一个为默认启动项。

最后就可以重启机器

```
sudo reboot
```

再次登录机器查看内核版本 `uname -r` ，已经是最新版本

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# uname -r
4.14.3-1.el7.elrepo.x86_64
```

## 开启 BBR

修改配置文件

```
echo 'net.core.default_qdisc=fq' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

现在就已经开启了 BBR ，可以确认一下

```
sudo sysctl net.ipv4.tcp_available_congestion_control
```

输出应该是 `net.ipv4.tcp_available_congestion_control = bbr cubic reno`

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# sudo sysctl net.ipv4.tcp_available_congestion_control
net.ipv4.tcp_available_congestion_control = bbr cubic reno
```

```
sudo sysctl -n net.ipv4.tcp_congestion_control
```

输出应该是 `bbr`

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# sudo sysctl -n net.ipv4.tcp_congestion_control
bbr
```

```
lsmod | grep bbr
```

输出应该是 `tcp_bbr                16384  0`

```
[root@iZ2ze83hhomw2zcf15c3qcZ ~]# lsmod | grep bbr
tcp_bbr                20480  0
```

## 测试一下

```
sudo yum install httpd -y
sudo systemctl start httpd.service
sudo firewall-cmd --zone=public --permanent --add-service=http
sudo firewall-cmd --reload
cd /var/www/html
sudo dd if=/dev/zero of=500mb.zip bs=1024k count=500
```

下载 `http://[your-server-IP]/500mb.zip` 看速度怎么样

除了以上的步骤，还可以直接使用一步安装脚本

```
sudo wget --no-check-certificate https://github.com/teddysun/across/raw/master/bbr.sh && chmod +x bbr.sh && ./bbr.sh
```

## 参考

[How to Deploy Google BBR on CentOS 7](https://www.vultr.com/docs/how-to-deploy-google-bbr-on-centos-7)

[一键安装最新内核并开启 BBR 脚本](https://teddysun.com/489.html)