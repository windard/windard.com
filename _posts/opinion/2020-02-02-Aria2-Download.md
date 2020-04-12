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

