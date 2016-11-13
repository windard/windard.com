---
layout: post
title: Cent OS 7 下安装 VPN
category: project
description: ss是个好东西，VPN 是个好东西。
---

## 在 Cent OS 7 下 安装 VPN

为什么是 Cent OS 呢？因为一般服务器常用的都是 Cent OS，性能还是可以的，个人电脑上用 Ubuntu ，比如说我，那么 VPN 的客户端连接就是用的 Ubuntu。

为什么是 Cent OS 7 呢？到目前 2016.10.14 为止最新的，虽然说新的容易出现新的问题,但是也意味着修复了很多旧的问题，所以用最新的，安全性有所保障。但是在 Cent OS 7 上有一个很坑的问题，Cent OS 7 的默认防火墙不是常用的 iptables ，而是 firewall ，我们需要先禁止 firewall ，然后安装使用 iptables。

为什么是 VPN？ss ( Shadowsocks ) 的安装教程在 Github 上的 Wiki 上写的清清楚楚明明白白，简单易懂一看就会，ss 在 Github 上 <del>被删除了</del>,相信你能找得到。

## 前言

你可以使用 `cat /etc/redhat-release ` 查看你的 Cent OS 版本，使用 virt-what 查看你的 VPS 的虚拟化机制。

VPN (Virtual Private Network) ，虚拟专用网络， 一般常见的有很多种不同的协议，分别有不同的软件来实现，比如说 PPTP，OpenVPN，L2TP/IPsec 等。

禁用 firewall ，安装使用 iptables。

> 在接下来的操作中都是默认使用 root 权限，如果不是，请加上 sudo

```
yum install iptables-services
systemctl mask firewalld
systemctl enable iptables
systemctl enable ip6tables
systemctl stop firewalld
systemctl start iptables
systemctl start ip6tables
```

iptables 常用命令

```
iptables -L -n                                    #查看iptables现有规则
iptables --list                                   #查看 iptables 现有规则
iptables -P INPUT ACCEPT            			  #先允许所有，不然有可能会杯具
iptables -F                                       #清空所有默认规则
iptables -X                                       #清空所有自定义规则
iptables -Z                                       #所有计数器归0

#允许来自于lo接口的数据包(本地访问)
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT        # 开放22端口
iptables -A INPUT -p tcp --dport 21 -j ACCEPT        # 开放21端口(FTP)
iptables -A INPUT -p tcp --dport 80 -j ACCEPT        # 开放80端口(HTTP)
iptables -A INPUT -p tcp --dport 443 -j ACCEPT       # 开放443端口(HTTPS)
iptables -A INPUT -p icmp --icmp-type 8 -j ACCEPT    # 允许ping
#允许接受本机请求之后的返回数据 RELATED，是为FTP设置的
iptables -A INPUT -m state --state  RELATED,ESTABLISHED -j ACCEPT

iptables -P INPUT DROP            # 其他入站一律丢弃
iptables -P OUTPUT ACCEPT         # 所有出站一律绿灯
iptables -P FORWARD DROP          # 所有转发一律丢弃

iptables -A INPUT -p tcp -s 45.96.174.68 -j ACCEPT    # 如果要添加内网ip信任（接受其所有TCP请求）
iptables -P INPUT DROP                                # 过滤所有非以上规则的请求
iptables -I INPUT -s ***.***.***.*** -j DROP        # 要封停一个IP，使用下面这条命令
iptables -D INPUT -s ***.***.***.*** -j DROP        # 要解封一个IP，使用下面这条命令
```

## PPTP

### 检测系统是否支持 PPTP 

```
[root@VM_1_214_centos conf.d]# cat /dev/ppp
cat: /dev/ppp: No such device or address
[root@VM_1_214_centos conf.d]# modprobe ppp-compress-18 && echo ok
ok
[root@VM_1_214_centos conf.d]# cat /dev/net/tun
cat: /dev/net/tun: File descriptor in bad state
```

如上结果即为可以安装 PPTP 。

### 安装组件

```
yum install -y ppp iptables pptpd
```

### 修改配置

编辑修改 `/etc/ppp/options.pptpd` ，将以下字段前的 `#` 号去掉并修改

```
#ms-dns 10.0.0.1
#ms-dns 10.0.0.2
```

改为 Google 的 DNS 服务器

```
ms-dns 8.8.8.8
ms-dns 8.8.4.4
```

编辑修改 `/etc/pptpd.conf`，将以下字段前的 `#` 号去掉即可

```
localip 192.168.0.1
remoteip 192.168.0.234-238,192.168.0.245
```

编辑修改 `/etc/ppp/chap-secrets` 按照以下格式输入你的账号和密码

```
username pptpd password *
```

或者是使用 `vpnuser add username password` 也可以。

编辑修改 `/etc/sysctl.conf` ，加入以下一句，使其支持路由转发

```
net.ipv4.ip_forward = 1
```

然后是修改即刻生效

```
sysctl -p
```

打开防火墙 1723 端口，设置 iptables 转发规则

```
iptables -I INPUT -p tcp --dport 1723 -j ACCEPT
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
```

重启 pptpd

```
service pptpd restart
```

然后就可以通过 PPTP 连接 VPN 了。

可以使用 `iptables save` 保存转发规则，使用 `chkconfig pptpd on` 设置 VPN 开机启动。

> 2016-11-13 最后防火墙规则不对，关闭防火墙可上，不关防火墙上不了。

## OpenVPN

安装 EPEL (Extra Packages for Enterprise Linux)，因为 OpenVPN 不在 Cent OS 的默认软件包里，不过奇怪的是好像腾讯云的服务器里有。。。

```
yum install epel-release
```

####