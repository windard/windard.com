---
layout: post
title: 配置使用 Aria2 离线下载
description:  aria2 + AriaNg
category: opinion
---

## 起因

挂 PT

## 软件

最好的还是用 qbittorrent

但是在 CentOS 8 上需要手动编译，比较复杂。

使用 Aria2 + AriaNG


但是 byr 不支持使用 Aria2 ，修改 ua 伪装

Aria2 配置

```
peer-id-prefix=-TR2770-
user-agent=Transmission/2.77
enable-rpc=true
rpc-secret=xxxxxxx
rpc-allow-origin-all=true
rpc-listen-all=true
```

## 安装 Aria2c

centos8 支持从 epel 安装

```
# yum install epel-release -y
# yum install aria2 -y
```

但是有点问题，不支持 HTTPS，需要手动安装开启

手动编译安装步骤

**1. 安装依赖包**

```
yum install openssl-devel libssh2-devel c-ares-devel libxml2-devel zlib-devel libsqlite3x-devel pkgconfig cppunit-devel libtool autoconf automake
```

**2. 下载源码**
```
git clone https://github.com/aria2/aria2.git
```

**3. 安装补丁**
```
yum install gettext-devel
```

**4. 自动配置**
```
autoreconf -i
```

**5. 再次配置**
```
./configure ARIA2_STATIC=yes
```

**6. 开始编译**
```
make
```

如果编译遇到问题

```
{standard input}: Assembler messages:
{standard input}:44480: Warning: end of file not at end of a line; newline inserted
{standard input}: Error: open CFI at the end of file; missing .cfi_endproc directive
g++: fatal error: Killed signal terminated program cc1plus
compilation terminated.
make[3]: *** [Makefile:2636: OptionHandlerFactory.lo] Error 1
make[3]: Leaving directory '/root/aria2/src'
make[2]: *** [Makefile:2677: all-recursive] Error 1
make[2]: Leaving directory '/root/aria2/src'
make[1]: *** [Makefile:554: all-recursive] Error 1
make[1]: Leaving directory '/root/aria2'
make: *** [Makefile:465: all] Error 2
```

一般是内存不足的原因，增加交换内存可以解决
```
( umask 0077 &&     dd if=/dev/zero of=/.swap.img bs=1M count=1024 &&     mkswap /.swap.img &&     swapon /.swap.img )
```

**7. 开始使用**  
装好之后，aria2c 的可执行文件在 `/root/aria2/src/aria2c`
> After make, the executable is located at /root/aria2/src/aria2c

加一个软链就可以使用了。

```
ln -s /root/aria2/src/aria2c /usr/local/bin/aria2c
```

现在安装好的 aria2c 就支持 HTTPS 协议了。🚀🚀

## 安装 qbittorrent

去年的时候还不支持，后面支持从 epel 安装

```
# yum install epel-release -y 
# yum install qbittorrent -y
```

## 参考

[Aria2 Centos8 安装配置](https://www.bbsmax.com/A/obzbPw1j5E/)    
[How to Install qBittorrent on CentOS 8/RHEL 8 Desktop & Server](https://www.linuxbabe.com/redhat/install-qbittorrent-centos-8-rhel-8)  
[How to install aria2 on CentOS](http://tutorialspots.com/how-to-install-aria2-on-centos-4179.html)    
[Gentoo GCC failed emerge](https://stackoverflow.com/questions/25575756/gentoo-gcc-failed-emerge/25584112#25584112)   
[Installing lxml: Error: open CFI at the end of file; missing .cfi_endproc directive](https://stackoverflow.com/questions/37128813/installing-lxml-error-open-cfi-at-the-end-of-file-missing-cfi-endproc-direct)  
