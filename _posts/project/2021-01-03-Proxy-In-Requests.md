---
layout: post
title: 在 requests 中使用代理
category: project
description: 比如常见的 HTTP 代理和 HTTPS 代理，还有 socks5 代理。
---

## 代理介绍

对于常见的正向代理有 HTTP 代理和 HTTPS 代理，对于 HTTP 代理只能代理到 HTTP 站点的请求，对于 HTTPS 代理只能代理到 HTTPS 站点的请求。

## 命令行中使用

### 代理参数
有些命令行软件是有代理参数的，比如 `curl` .

```
curl --proxy 23.45.122.54:8763 http://ifconfig.io
curl --proxy 23.45.122.54:8763 https://ifconfig.io
```

实际上，在这里对于具体的代理类型未设置的话，会对 HTTP 请求采用 HTTP 代理，对 HTTPS 请求采用 HTTPS 代理，所以就相当于：

```
curl --proxy http://23.45.122.54:8763 http://ifconfig.io
curl --proxy https://23.45.122.54:8763 https://ifconfig.io
```

一般的正向代理站点都无法接收 HTTPS 的请求代理，对于 NGINX 可以参考 [使用 nginx 进行 HTTPS 的正向代理](https://windard.com/project/2016/11/13/About-Nginx) 正确配置之后，就可以在 HTTPS 代理中使用 HTTP schema 代理 HTTPS 站点请求。

```
curl --proxy http://23.45.122.54:8763 https://ifconfig.io
```

### 环境变量

但是有些命令行软件比如 `wget` 就没有代理参数，这时就可以设置环境变量参数。

```
http_proxy=23.45.122.54:8763 wget http://ifconfig.io
https_proxy=23.45.122.54:8763 wget https://ifconfig.io
```

在这里同样的需要匹配 `HTTP|HTTPS` 请求类型和 `HTTP|HTTPS` 代理类型的，对于未设置代理地址的 schema 时候是会自动生成。

> 在这里因为只是设置环境变量，所以其实换个思路可以用 `wget -e` 的参数 `wget -e http_proxy=23.45.122.54:8763 http://ifconfig.io`

如果需要长期使用，可以写入配置

```
export use_proxy = on
export http_proxy=http://your_ip_proxy:port/
export https_proxy=$http_proxy
export ftp_proxy=$http_proxy
export dns_proxy=$http_proxy
export rsync_proxy=$http_proxy
export no_proxy="localhost,127.0.0.1,localaddress,.localdomain.com"
```

### 其他工具

如果以上都不能满足需求的话，或许可以试下使用其他一些工具来实现，比如 `ProxyChains` 之类的做代理转发，或者 `Caddy`, `Squid` 搭建代理服务器。

## socks 代理

除了常见的 HTTP 代理和 HTTPS 代理之外，还有 socks 代理，常用的比如 socks5 代理。

在 `curl` 可以直接使用

```
curl --socks5 127.0.0.1:1086 ifconfig.io
curl --socks5 127.0.0.1:1086 http://ifconfig.io
curl --socks5 127.0.0.1:1086 https://ifconfig.io
curl --socks5 socks5://127.0.0.1:1086 https://ifconfig.io
```

## requests 中使用

为什么要专门强调在 requests 中使用，因为在 python 里 requests 是使用最广的 HTTP 客户端，我使用 python 发出的 HTTP 请求大部分是由 requests 完成的。

### HTTP 和 HTTPS 代理

在 requests 中使用代理可以通过 `proxies` 参数设置, 同样的 HTTP 请求需要使用 HTTP 代理对应的 HTTP schema。

```python
# -*- coding: utf-8 -*-

import requests


def http_proxy():
    proxies = {"http": "http://23.45.122.54:8763", "https": "https://23.45.122.54:8763"}
    resp = requests.request("GET", "http://httpbin.org/get", proxies=proxies)
    print(resp.status_code)
    print(resp.content)
    resp = requests.request("GET", "https://httpbin.org/get", proxies=proxies)
    print(resp.status_code)
    print(resp.content)


if __name__ == '__main__':
    http_proxy()
```

但是实际上，对于 HTTPS 的请求使用 HTTPS 的代理，但是却可以使用 HTTP 的 schema 。

```python
# -*- coding: utf-8 -*-

import requests


def https_proxy():
    proxies = {"http": "http://23.45.122.54:8763", "https": "http://23.45.122.54:8763"}
    resp = requests.request("GET", "http://httpbin.org/get", proxies=proxies)
    print(resp.status_code)
    print(resp.content)
    resp = requests.request("GET", "https://httpbin.org/get", proxies=proxies)
    print(resp.status_code)
    print(resp.content)


if __name__ == '__main__':
    https_proxy()

```

### socks 代理

在 requests 中使用 socks5 代理有两种方式
1. requests 的 proxies 参数其实支持 socks5 ，但是需要先安装相关依赖包 `pip install "requests[socks]"`
2. 使用 socks 包 hook 发出的 HTTP 请求，全局生效，需要先安装 socks 包 `pip install pysocks`

```python
# -*- coding: utf-8 -*-

import requests


def get_by_proxy():
    proxies = {"http": "socks5://127.0.0.1:1086", "https": "socks5://127.0.0.1:1086"}
    resp = requests.request("GET", "http://httpbin.org/get", proxies=proxies)
    print(resp.status_code)
    print(resp.content)


def hook_proxy():
    import socks
    import socket

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
    socket.socket = socks.socksocket

    resp = requests.request("GET", "http://httpbin.org/get")
    print(resp.status_code)
    print(resp.content)


if __name__ == '__main__':
    get_by_proxy()
    hook_proxy()

```

## 获取代理

1. 自己搭建，无论是 HTTP 代理或者 HTTPS 代理还是 socks5 代理，都是有有办法的。
2. 网上公开的临时资源，可以通过一些工具获取，比如 [ProxyBroker](https://github.com/constverum/ProxyBroker), 或者 [proxy_pool](https://github.com/jhao104/proxy_pool)

## 参考链接

[How to set proxy for wget?](https://stackoverflow.com/questions/11211705/how-to-set-proxy-for-wget)    
[How to make python Requests work via socks proxy](https://stackoverflow.com/questions/12601316/how-to-make-python-requests-work-via-socks-proxy)      
[Python中Request 使用socks5代理的两种方法(个人推荐方法二)](https://doomzhou.github.io/coder/2015/03/09/Python-Requests-socks-proxy.html)       
