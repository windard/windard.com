---
layout: post
title: linux 下安装 UT
description: 主要是在 Debian 和 CentOS 上安装 uTorrent，Linux 一般常用的都是这两个系统的...
category: opinion
---

utorrent 无愧为当今最好的下载器之一，BitTorrent 收购 μTorrent 之后放弃自我，仅修改 logo， 与 ut 一模一样。

uTorrent 支持完整的 p2p 协议，软件安装包小，系统要求低，支持 ipv6，支持代理，下载速度快。

桌面版本都有界面直接点击下一步安装即可，服务器版本稍微麻烦一点

## Debian

这是 Debian 的 Dockerfile

```
FROM debian:latest

RUN echo "deb http://security.debian.org/debian-security wheezy/updates main">>/etc/apt/sources.list && \
    apt update && \
    apt install -y wget libssl1.0.0 && \
    wget http://download-hr.utorrent.com/track/beta/endpoint/utserver/os/linux-x64-debian-7-0 -O linux-x64-debian-7-0.1.tar.gz && \
    tar -zxvf linux-x64-debian-7-0.1.tar.gz -C /opt/ && \
    chmod -R 755 /opt/utorrent-server-alpha-v3_3/ && \
    ln -s /opt/utorrent-server-alpha-v3_3/utserver /usr/bin/ && \
    mkdir /data

VOLUME /data

EXPOSE 8080

CMD ["utserver", "-settingspath", "/opt/utorrent-server-alpha-v3_3/", "-logfile", "/opt/utorrent-server-alpha-v3_3/utserver.log"]
```

## CentOS

这是 CentOS 的安装脚本

```
#!/bin/bash

yum install -y glibc.i686 openssl098e.i686
ln -s /usr/lib/libssl.so.0.9.8e /lib/libssl.so.0.9.8
ln -s /usr/lib/libcrypto.so.0.9.8e /lib/libcrypto.so.0.9.8
mkdir -p /opt/utserver
wget http://download.utorrent.com/linux/utorrent-server-3.0-25053.tar.gz -O /opt/utserver/utorrent-server-3.0-25053.tar.gz
cd /opt/utserver/
tar -zxvf utorrent-server-3.0-25053.tar.gz
mv /opt/utserver/utorrent-server-v3_0/* /opt/utserver/
rm -rf /opt/utserver/utorrent-server-v3_0

./utserver -settingspath /opt/utserver/ -logfile /opt/utserver/utserver.log -daemon

echo "Browse to http://server:8080/gui and login with user admin and no password."
echo "After logging in, go to settings and setup an admin password."
echo "Want settings?  Google utserver.conf for examples..."
```

services

```
[Unit]
Description=uTorrent Server Daemon
After=network.target

[Service]
Type=forking
ExecStart=/usr/bin/utserver -configfile /etc/utserver.conf -settingspath /srv/utserver/settings/ -pidfile /srv/utserver/utserver.pid -logfile /srv/utserver/utserver.log -daemon
User=utserver
PIDFile=/srv/utserver/utserver.pid

[Install]
WantedBy=multi-user.target
```

## qBittorrent

uTorrent Server 版本在服务器上不好用
1. 没有详细日志
2. 没有 tracker 信息
3. 没有官方最新 centOS 版本
4. 不太稳定，token 返回400
5. [存疑] tracker 主机查询不支持 ipv6

不如用 qbittorrent-nox

```
yum[apt] install -y qbittorrent-nox
```

services

```
[Unit]
Description=qBittorrent Daemon Service
After=network.target

[Service]
Type=forking
User=1000
ExecStart=/usr/bin/qbittorrent-nox -d
ExecStop=/usr/bin/killall -w qbittorrent-nox

[Install]
WantedBy=multi-user.target
```

## 参考链接

[How to install uTorrent v3.3 on 14.04](https://askubuntu.com/questions/530955/how-to-install-utorrent-v3-3-on-14-04)

[uTorrent Server (utserver) on Centos 7 (x86_64)](https://gist.github.com/integrii/71b2fbbd3c48ec776ee6)

[RPM resource libssl.so.0.9.8()(64bit)](https://rpmfind.net/linux/rpm2html/search.php?query=libssl.so.0.9.8()(64bit))

[Setting up qBittorrent on Ubuntu server as daemon with Web interface (15.04 and newer)](https://github.com/qbittorrent/qBittorrent/wiki/Setting-up-qBittorrent-on-Ubuntu-server-as-daemon-with-Web-interface-(15.04-and-newer))