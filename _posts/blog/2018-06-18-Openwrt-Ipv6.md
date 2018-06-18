---
layout: post
title: Openwrt 使用 IPv6
description: 年轻的时候不用 IPv6 ，离开学校可就没有机会了
category: blog
---

[openwrt](https://openwrt.org/zh/start) 是一款出色的嵌入式 Linux 操作系统，常用作为刷路由器固件，扩展了路由器的可玩性。

一般的路由器都可以刷 openwrt 固件，使用 bootloader 即可，网上教程很多。

路由器刷 openwrt 需注意，查看[支持设备列表](http://wiki.openwrt.org/zh-cn/toh/start)中是否有你的路由器型号，否则需要魔改一番再刷机。

openwrt 是 Linux 操作系统的一种，作为路由器固件通常需要配合 [luci](https://github.com/openwrt/luci) 使用，即路由器后台配置面板。

IPv6 是 IPv4 的下一代互联网协议，可以有效缓解 IPv4 地址不足的问题，理论上可以给地球上的每一颗沙子都能分配一个 IP 地址。

## 更改 LUCI 语言和界面

添加中文语言包和 Material 风格界面。

```
opkg update
opkg install luci-i18n-base-zh-cn
opkg install luci-theme-material
```

如果没有 `luci-theme-material` 软件包，可以按照 [how can i install this theme](https://github.com/LuttyYang/luci-theme-material/issues/31) 手动安装。

![openwrt_chinese_material](/images/openwrt_chinese_material.png)

![openwrt_panel](/images/openwrt_panel.png)

## PPPoE 无法联网

在刷入一些老的 openwrt 系统或者系统恢复初始化设置之后，无法使用 PPPoE 连接。

在 wan 口，wan6 口发送和接收数据包都是0，查看接口时是这样的。

![openwrt_interface_error](/images/openwrt_interface_error.png)

这个的原因是因为 VLAN 设置有误造成的，网络不通。

VLAN （Virtual Local Area Network）虚拟局域网，是在同一物理局域网内用于划分若干个不同广播域（子网）的技术，子网内的主机可以互相通信，不同子网的主机之间不可互相通信。

- vlan0 连接内部的所有 lan 口，作为内网通信。
- vlan1 连接 wan 口，负责对外通信。

这是 openwrt 的网络拓扑图。

![openwrt_internet](/images/openwrt_internet.png)

错误的交换机（switch）配置各有各的错误，比如这样。

![openwrt_switch_error](/images/openwrt_switch_error.png)

网络接口即网卡，进入 openwrt 使用 ifconfig 命令可以看到所有的网卡信息。

- 物理网络接口，如eth0, eth8, radio0, wlan19, .. 这些符号总是代表着真实存在的网络设备
- 虚拟网络接口，如lo, eth0:1, eth0.1, vlan2, br0, pppoe-dsl, gre0, sit0 tun0, imq0, teql0, .. 这些都是不真实存在物理网络设备的虚拟的网络接口，但是linked到一个物理设备（否则他们是没有价值的）

使用虚拟网络接口是为了给予系统管理员配置基于linux的操作系统的最大的灵活性。一个虚拟的网络接口是一般联合一个物理网络接口（eth6）或其他的虚拟网络接口（eth6.9）或是独立的

所以，我们的 wan 口和 wan6 口都应该接到虚拟网卡上，在接口的修改的高级设置的物理设置里，需要注意是这样的。

![openwrt_interface_physical](/images/openwrt_interface_physical.png)

在交换机这里的端口都没有区分 wan 口和 lan 口，需要注意找到正确的 wan 口，然后配置如下。

![openwrt_switch_right](/images/openwrt_switch_right.png)

- VID1，即 vlan0，连接 CPU，将 wan 口设置为关闭，不连接所有的 lan 口，实际上是作为内网通信。
- VID2，即 vlan1，连接 CPU，将 wan 口设置为不关联，关闭所有的 lan 口，实际上是与外网通信。

修改之后别忘了点击 `保存&应用`

配置成功后的结果

![openwrt_interface_right](/images/openwrt_interface_right.png)

## openwrt 配置 ipv6

在网上一开始找到的 ipv6 配置都很复杂，后来才知道在Openwrt 14.07或者更新版本有简单的方式。

安装 kmod-ipt-nat6

```
opkg update
opkg install kmod-ipt-nat6
```

然后配置 iptables

```
ip6tables -t nat -I POSTROUTING -s `uci get network.globals.ula_prefix` -j MASQUERADE
route -A inet6 add 2000::/3 `route -A inet6 | grep ::/0 | awk 'NR==1{print "gw "$2" dev "$7}'`
```

最后在 luci 后台界面配置即可。

在 "网络" -> "接口"

1. `IPv6 ULA-Prefix` 改首字母 f 改为 d

![openwrt_ipv6_prefix](/images/openwrt_ipv6_prefix.png)

在 "网络" -> "接口" -> "LAN" -> "修改" -> "DHCP服务器" -> "IPv6设置"

1. `Router Advertisement-Service` 设为 `服务器模式`
2. `DHCPv6-Service` 和 `NDP-Proxy` 禁用
3. `Always announce default router` 勾选

![openwrt_ipv6_dhcp](/images/openwrt_ipv6_dhcp.png)


这时应该在路由器中的设备都能够获得可用的 ipv6 地址,可以在 `https://test-ipv6.com/` 确定 ipv6 的可用性。

![ipv6_mac](/images/ipv6_mac.png)

![ipv6_phone](/images/ipv6_phone.png)

或者使用工具。

```
$ ifconfig
...
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
    ether dc:a9:04:81:23:9d
    inet6 fe80::66:ba04:9cba:cab3%en0 prefixlen 64 secured scopeid 0x8
    inet 192.168.1.229 netmask 0xffffff00 broadcast 192.168.1.255
    inet6 dd1b:fb31:4326::1434:5c14:85e:fa02 prefixlen 64 autoconf secured
    inet6 dd1b:fb31:4326::391d:8448:7a0e:8897 prefixlen 64 autoconf temporary
    nd6 options=201<PERFORMNUD,DAD>
    media: autoselect
    status: active
...
$ ping6 ipv6.baidu.com
PING6(56=40+8+8 bytes) dded:a37a:818b::b092:b9e8:d18d:9292 --> 2400:da00:2::29
16 bytes from 2400:da00:2::29, icmp_seq=0 hlim=51 time=21.553 ms
16 bytes from 2400:da00:2::29, icmp_seq=1 hlim=51 time=319.632 ms
^C
--- ipv6.baidu.com ping6 statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/std-dev = 21.553/170.593/319.632/149.039 ms
$ ping6 2001:4860:4860::8888
PING6(56=40+8+8 bytes) dded:a37a:818b::b092:b9e8:d18d:9292 --> 2001:4860:4860::8888
16 bytes from 2001:4860:4860::8888, icmp_seq=0 hlim=52 time=64.005 ms
16 bytes from 2001:4860:4860::8888, icmp_seq=1 hlim=52 time=61.982 ms
^C
--- 2001:4860:4860::8888 ping6 statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/std-dev = 61.982/62.993/64.005/1.011 ms
```

> 在 Linux/Mac 下使用 `ping6`，在 Windows 下使用 `ping -6`

可用的 ipv6 地址表示非 `fe80` 开头的 ipv6 地址，在 Linux 机器上会展示 `Scope:Global` 的字样。

`FE80::/64` 地址是 ipv6 的链路本地地址，即 ipv4 中的保留地址 `10.x.x.x` 或者 `192.168.x.x`

```
inet6 addr: dd1b:fb31:4326:0:9415:ea92:5d2f:119e/64 Scope:Global
inet6 addr: fe80::eb8:4d02:c231:5fda/64 Scope:Link
```

可以使用 `ipv6.baidu.com` 来检测 ipv6 的可用性，既然可以使用 ipv6，就肯定想试一下某个网站能不能上，不幸的是 `ipv6.google.com` 这个网址却仍然时而偶尔不能用。。。

不过其 ipv6 DNS 地址是同样可用的

```
2001:4860:4860::8844
2001:4860:4860::8888
```

最后可以为 iptables 设置开机启动项，可以在 luci 后台设置，或者直接修改 `/etc/rc.local`

```
line=0
while [ $line -eq 0 ]
do
  sleep 10
  line=`route -A inet6 | grep ::/0 | awk 'END{print NR}'`
done
ip6tables -t nat -I POSTROUTING -s `uci get network.globals.ula_prefix` -j MASQUERADE
route -A inet6 add 2000::/3 `route -A inet6 | grep ::/0 | awk 'NR==1{print "gw "$2" dev "$7}'`
```

## 参考链接

[OpenWRT下双WAN配置
](https://blog.chionlab.moe/2016/07/13/openwrt-multiwan-configuration/)

[openwrt中br-lan,eth0,eth0.1,eth0.2](https://blog.phpgao.com/openwrt-interface.html)

[Linux 网络接口(Network Interfaces)](http://wiki.openwrt.org/zh-cn/doc/networking/network.interfaces)

[交换机手册(Switch Documentation)](http://wiki.openwrt.org/zh-cn/doc/uci/network/switch)

[网络设置](https://openwrt.org/zh-cn/doc/uci/network)

[校园网 IPv6 路由器设置](https://linux.xidian.edu.cn/wiki/tips/ipv-6-router)

[OpenWRT 路由器作为 IPv6 网关的配置](https://github.com/tuna/ipv6.tsinghua.edu.cn/blob/master/openwrt.md)

[IPV6 NAT WITH OPENWRT ROUTER](http://blog.iopsl.com/ipv6-nat-with-openwrt-router/)

[入手Openwrt路由器，科学上网（VPN/IPv6）](https://spaces.ac.cn/archives/3524)
