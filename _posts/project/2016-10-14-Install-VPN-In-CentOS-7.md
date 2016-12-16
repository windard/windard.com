---
layout: post
title: Cent OS 7 下安装 VPN
category: project
description: ss是个好东西，VPN 是个好东西。
---

## 在 Cent OS 7 下 安装 VPN

为什么是 Cent OS 呢？因为一般服务器常用的都是 Cent OS，性能还是可以的，个人电脑上用 Ubuntu ，比如说我，那么 VPN 的客户端连接就是用的 Ubuntu。

为什么是 Cent OS 7 呢？到目前 2016.10.14 为止最新的，虽然说新的容易出现新的问题,但是也意味着修复了很多旧的问题，所以用最新的，安全性有所保障。

> 但是在 Cent OS 7 上有一个很坑的问题，Cent OS 7 的默认防火墙不是常用的 iptables ，而是 firewall ，本文尽量用给出两种防火的使用策略。

为什么是 VPN？ss ( Shadowsocks ) 的安装教程在 Github 上的 Wiki 上写的清清楚楚明明白白，简单易懂一看就会，ss 在 Github 上 <del>被删除了</del>,相信你能找得到。

## 前言

你可以使用 `cat /etc/redhat-release ` 查看你的 Cent OS 版本，使用 `virt-what` 查看你的 VPS 的虚拟化机制 ，需要虚拟化机制为 Xen 或 KVM 的。

VPN (Virtual Private Network) ，虚拟专用网络， 一般常见的有很多种不同的协议，分别有不同的软件来实现，比如说 PPTP，OpenVPN，L2TP/IPsec 等。

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

### 配置防火墙

#### iptables

打开防火墙 1723 端口，设置 iptables 转发规则

```
iptables -I INPUT -p tcp --dport 1723 -j ACCEPT
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
iptables -I FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
```

但是 iptables 的自带的配置在这里是有问题的，所以需要先清除之前的配置，提供一份完整版的 iptables 配置。

```
iptables -F
iptables -X
iptables -Z
iptables -t nat -F
iptables -t nat -X
iptables -t nat -Z
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 1723 -j ACCEPT
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
iptables -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
``` 

#### firewalld 


### 使用 PPTP

开启 pptpd

```
service pptpd start
```

重启 pptpd

```
service pptpd restart
```

关闭 pptpd

```
service pptpd stop
```

查看状态 pptpd

```
service pptpd status
```

可以使用 `iptables-save > /etc/sysconfig/iptables` 保存转发规则，使用 `chkconfig pptpd on` 设置 VPN 开机启动。

## OpenVPN

安装 EPEL (Extra Packages for Enterprise Linux)，因为 OpenVPN 不在 Cent OS 的默认软件包里，不过奇怪的是好像腾讯云的服务器里有。。。

```
yum install epel-release
```

### 安装 OpenVPN

```
yum install -y openvpn easy-rsa
```

### 配置 OpenVPN

将 OpenVPN 提供的默认配置文件移到 OpenVPN 的配置文件位置

```
cp /usr/share/doc/openvpn-*/sample/sample-config-files/server.conf /etc/openvpn
```

编辑修改配置文件

```
vim /etc/openvpn/server.conf
```

将

```
;push "redirect-gateway def1 bypass-dhcp"
;push "dhcp-option DNS 208.67.222.222"
;push "dhcp-option DNS 208.67.220.220"
;user nobody
;group nobody
;log-append  openvpn.log
```

将 NDS 服务器改为 Google 的 DNS 服务器，连接设备采用 DHCP 分配子网 IP。

```
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
user nobody
group nobody
log-append  openvpn.log
```

准备生成密钥和证书文件

```
mkdir -p /etc/openvpn/easy-rsa/keys
cp -rf /usr/share/easy-rsa/2.0/* /etc/openvpn/easy-rsa
```

编辑修改密钥配置

```
vi /etc/openvpn/easy-rsa/vars
```

配置以下各项的，内容自定义即可

```
export KEY_COUNTRY="CN"
export KEY_PROVINCE="Shaanxi"
export KEY_CITY="Xian"
export KEY_ORG="Windard"
export KEY_EMAIL="windard@windard.com"
export KEY_OU="Windard"

export KEY_NAME="openvpn"

export KEY_CN="openvpn.windard.com"
```

制作证书

```
cp /etc/openvpn/easy-rsa/openssl-1.0.0.cnf /etc/openvpn/easy-rsa/openssl.cnf
cd /etc/openvpn/easy-rsa
source ./vars
./clean-all
./build-ca
```

因为之前已经配置好参数，所以现在只需一路回车就可以。

创建服务器端证书

```
./build-key-server server   
```

同样一路回车，最后需要输入密码，设置密码即可，密码在后面用，在是否签名证书时输入 `y`

```
Sign the certificate? [y/n]:y
```

创建密钥文件

```
./build-dh
```

生成服务器端证书

```
cd  /etc/openvpn/easy-rsa/keys
cp  dh2048.pem  ca.crt  server.crt  server.key   /etc/openvpn
cd  /etc/openvpn/easy-rsa
./build-key client
```

同样的一路回车，在最后的密码的地方输入你前面设置的密码，在最后是否签名证书的时候输入 `y`。

现在一切都已准备就绪了，最后又到了设置路由的地方了。

```
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
```

同样的开启路由转发

```
vi /etc/sysctl.conf
```

写入

```
net.ipv4.ip_forward = 1
```

然后重启网络服务使其生效

```
systemctl restart network.service
```

### 使用 OpenVPN 

开启 OpenVPN

```
systemctl -f enable openvpn@server.service
systemctl start openvpn@server.service
```

查看状态

```
systemctl status openvpn@server.service
```

如果遇到了问题，可以查看 `/etc/openvpn/openvpn.log` 查看日志。

### 配置OpenVPN 客户端

现在客户端需要的文件就是以下三个

```
/etc/openvpn/easy-rsa/keys/ca.crt
/etc/openvpn/easy-rsa/keys/client.crt
/etc/openvpn/easy-rsa/keys/client.key
```

使用客户端连接的时候可以设置这仨的位置，也可以将他们写入到一个 `.ovpn` 的配置文件中。

```
client
dev tun
proto udp
remote 182.254.139.224 1194
resolv-retry infinite
nobind
persist-key
persist-tun
comp-lzo
verb 3
<ca>
ca.crt的内容粘贴到这里
</ca>

<cert>
client.crt的内容粘贴到这里
</cert>

<key>
client.key的内容粘贴到这里
</key>
```

然后使用 

```
sudo openvpn --config ~/path/to/client.ovpn
```

就可以使用了。



## L2TP

这个是最安全的 VPN 解决方案，因为它是基于 IP 层的加密隧道，采用 IPsec 加密机制。

同时它的限制也比较多，除了上面出现过的使用 openVZ 虚拟化的服务器必须支持 TUN 和 PPP 模块之外，还要求服务器必须有自己的固定公网 IP，而不能是弹性公网IP。

### 前言

1. 如何检测是否支持TUN模块？

执行命令：

```
cat /dev/net/tun
```
如果返回信息为：`cat: /dev/net/tun: File descriptor in bad state` 说明正常

2. 如何检测是否支持ppp模块？

执行命令：
```
cat /dev/ppp
```

如果返回信息为：`cat: /dev/ppp: No such device or address` 说明正常

3. 如何检查是否为固定公网 IP？

执行命令

```
ifconfig
```

如果返回网卡信息中有 公网 IP，而说明正常，非常不幸，腾讯云使用的是弹性公网 IP，所以不能搭建 L2TP VPN 服务器。

### 安装 openswan

### 安装 ppp

### 安装 xl2tpd

### 配置 sysctl

### 配置防火墙

### 使用一键脚本

需 root 权限

```
wget --no-check-certificate https://raw.githubusercontent.com/teddysun/across/master/l2tp.sh
chmod +x l2tp.sh
./l2tp.sh
```