---
layout: post
title: 给 Nginx 配置 HTTPS
category: project
description: HTPS （HTTP over TLS， HTTP over SSL， HTTP Secure）的简单介绍和应用。
---

## HTTPS

HTTPS 就是 HTTP Secure ，简单来说就是安全的 HTTP 协议，HTTPS 还是经由 HTTP 进行通信，但是通过 SSL/TLS 对数据包进行加密。

因为一开始 HTTP 设计的时候就没有考虑过数据保密性问题，所以在网络上的数据都是以明文形式传输的，HTTPS 的主要目的，就是提供对网络服务器的身份认证，保护交换数据的隐私和完整性，对窃听和中间人攻击提供有效的防护。

HTTP 协议的 URL 由 `http://` 起始并默认使用端口 80 ， HTTPS 协议的 URL 由 `https://` 起始并默认使用端口 443。

目前建议所有网络请求都能是 HTTPS 的，像 Google ， Facebook ， Baidu ， Taobao 等公司，都已经全站启用 HTTPS ，可以在浏览器的地址栏看到一个绿色的锁的标志。

## 工作原理

HTTPS 的核心是 SSL (Secure Socket Layer 安全套接层)/TLS (Transport Layer Security 安全传输层协议) ，其中包含了 对称加密，非对称加密和 HASH 加密等加密方式。

![https_handshake.png](/images/https_handshake.png)

