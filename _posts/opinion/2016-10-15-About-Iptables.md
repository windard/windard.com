---
layout: post
title: iptables 防火墙基本配置和使用
description: 防火墙是如此的重要，几乎每一台个人电脑，网络服务器都有网络防火墙，但是想掌握并正确的使用它却不容易。
category: opinion
---

## iptables 

iptables 意味 ip 表，看起来和 路由表，ARP 表挺像的，都是在网络传输过程中做一些查找和转换。在 Linux 上一般默认的防火墙就是 iptables ，但是在 Cent OS 7 中，防火墙变为了 firewall ，还是比较习惯用 iptables，所以把 firewall 换回了 iptables。

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

#### iptables 组成

**四表五链**

##### 表: 

- filter 用于过滤，访问控制、规则匹配 
- nat 用于nat功能，端口映射，地址转发
- mangle 用于用于对特定数据包的修改
- raw  原生的数据，raw 中的数据包不会被系统跟踪

一般前两张表用的比较多

##### 链: 

- INPUT 匹配目的地址为本机的
- OUTPUT 匹配向外转发的
- FORWARD 匹配本机转发的
- PREROUTING 路由前，用于修改目的地址（DNAT）
- POSTROUTING 路由后，用于修改源地址（SNAT）

#### iptables 使用

iptables  [-t 表名 ]  命令 链名 匹配  -j 操作

> 默认使用 filter 表

##### 命令

- `-A` （append）追加一条规则
- `-I` （insert）插入一条规则
- `-D` （delete）删除一条规则，例如 `iptables –D INPUT 3`，删除第三条规
- `-F` （flush）清空规则
- `-L` （list）列出规则，使用`-vnL来显示效果比较好，用 `--line-number` 显示规则序
- `-P` （policy）设置某链默认规则

##### 匹配条件

- `-i` （input）进入接口 如 eth0,wlan0
- `-o` （output）出去接口
- `-s` （source）来源地址，例如 `-s 192.168.1.0/24`，可单IP
- `-d` （destination）目的地址
- `-p` （protocol）协议类型（tcp、udp、icmp）
- `-m` （match）完全匹配 
- `--sport` 来源端口，例如 `--sport 1000` ，匹配源端口1000，也可以1000:3000指定范围
- `--dport` 目的端口
- `--state` 状态 NEW（收到的第一个包），ESTABLISHED（开始连接的包），RELATED（连接稳定的包），INVALID（不正确的包），UNTRACKED（不被显示的包）
- `--mac` 来源MAC地址匹配
- `--limit` 包速率匹配
- `--multiport` 多端口匹配，端口以逗号分隔

##### 操作

- `ACCEPT` 允许数据包通过
- `DROP` 阻止数据包通过
- `REJECT` 拒绝数据包通过，并返回报错信息
- `SNAT` 应用 nat 表的 POSTROUTING 链，进行源地址转换，可单个、一组IP
- `DNAT` 应用 nat 表的 PREROUTING 链，进行目的地址转换，可单个、一组IP
- `MASQUERADE` 动态源地址转换，动态IP时使用

默认 iptables 配置文件位置 `/etc/sysconfig/iptables`

#### 简单使用

关闭 iptables ，开启 iptables，查看 iptables 状态，重启 iptables

```
service iptables stop
service iptables start
service iptables status
service iptables restart
```

iptables 的规则都是立即生效的，但是并没有保存下来，重启就会失效，如果需要长久使用，需要保存 iptables 规则。

```
service iptables save
```

查看现有规则，并清空所有规则

```
iptables -nvL              #查看iptables现有规则
iptables -F                #清空所有默认规则
iptables -X                #清空所有自定义规则
iptables -Z                #所有计数器归0
```

允许本地访问，lo 数据包，并允许 ICMP 协议的数据包（ping）和 正常本地向外连接

```
iptables -I INPUT -i lo -j ACCEPT
iptables -I INPUT -p icmp -j ACCEPT
iptables -I INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
```

允许 22 （ssh） 和 80 （http） 端口的访问

```
iptables -I INPUT -p tcp --dport 22 -j ACCEPT
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
```

防止 CC，DOS 攻击，限制每个 IP 的并发连接数

```
iptables -I INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 30 -j REJECT 
```

防止 DDOS 攻击，限制每个 IP 每秒并发连接数

```
iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
iptables -A FORWARD -p tcp --syn -m limit --limit 1/s -j ACCEPT  
```

除开放的端口外，其他端口都禁止访问

```
iptables -A INPUT -j REJECT
```

在公司内部局域网 10.10.155.0/24, 10.10.188.0/24 能够访问服务器上任何服务。外网可以访问公司 HTTP 服务和 VPN 服务。

```
iptables -I INPUT -i lo -j ACCEPT
iptables -I INPUT -p icmp -j ACCEPT
iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -s 10.10.155.0/24 -j ACCEPT
iptables -A INPUT -s 10.10.188.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 1723 -j ACCEPT
iptables -A INPUT -j REJECT
```

#### 端口转发

NAT( Network Address Translation，网络地址转换 ) ，用来解决 Ipv4 地址不足的问题，可以通过少量的 公有 IP 来代表多数 私有 IP，一般通过 端口转发 来实现，在学校，公司，研究机构等场景应用较为广泛。

NAT 按照寻址方式来分有动态地址转换，静态地址转换，按照转换格式来分有源地址转换，目的地址转换。

- 源地址转换 (Source NAT,SNAT) 用于局域网内的用户向外访问公网，当局域网内部用户访问外网时，网关将其 源地址 的私有 IP 改为公有 IP
- 目的地址转换 (Destination,DNAT) 用于公网用户访问局域网内服务，当公网用户想访问内网服务时，网关将内网服务从 私有 IP 映射到 公有 IP 上，即可进行访问。

在使用 iptables 做 NAT 之前，先要确定一下电脑是否已经开启路由转发

```
cat /proc/sys/net/ipv4/ip_forward
```

如果为 0 则未开启，将其改为 1 即可。这个只是暂时的更改，同样的在重启之后就恢复默认值，若是想永久更改可以在 `/etc/sysctl.conf` 或 `/etc/rc.d/rc.local` 中写入 `echo "1" > /proc/sys/net/ipv4/ip_forward`

#### SNAT

在 有线网卡 eth0 上使用 动态地址转换，所有通过这个网卡的局域网用户都可以访问外网，eth0 。

```
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

静态地址转换

```
iptables –t nat -A POSTROUTING -s [内网IP或网段] -j SNAT --to [公网IP]
```

#### DNAT

通过公网端口映射内网端口来实现公网访问内网。

```
iptables –t nat -A PREROUTING -d [对外IP] -p tcp --dport [对外端口] -j DNAT --to [内网IP:内网端口]
```

这里不用再配 SNAT ，因为系统会根据数据包的来源再返还回去。

还可以做流量劫持，比如你在路由器上，内网设备都通过 `br-lan`，把内网设备网站劫持到你的路由器配置页面。

```
iptables -t nat -A PREROUTING -i br-lan -p tcp --dport 80 -j DNAT --to 192.168.1.1:80
``` 

对 HTTPS 的站无效。

#### 本地端口转发

将本机的 8080 端口的服务转发到 80 端口上，只对外有效，在本机内并不做这个转换。

```
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

#### 负载均衡

端口转发实现负载均衡

```
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8001:8008
```

#### 默认 iptables 配置

```
iptables -nvL              
iptables -F                
iptables -X              
iptables -Z       
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT         
iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
iptables -A INPUT -j DROP
iptables -A OUTPUT -j ACCEPT
```

参考链接

[Iptables小总结](https://yq.aliyun.com/articles/38737) <br>
[→_→ iptables](https://vvl.me/2016/08/iptables-two/) <br>
[初识 iptables](https://vvl.me/2016/08/iptables-one/) <br>
[CentOS 7 安装 iptables 防火墙](http://blog.mimvp.com/2016/07/centos-7-installing-the-iptables-firewall/) <br>
[通过iptables实现端口转发和内网共享上网](http://xstarcd.github.io/wiki/Linux/iptables_forward_internetshare.html) <br>
[iptables学习笔记：端口转发之“内网访问外网”](http://blog.csdn.net/subfate/article/details/52659765)