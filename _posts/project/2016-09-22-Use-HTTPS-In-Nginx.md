---
layout: post
title: 在 Nginx 上配置 HTTPS
category: project
description: HTPS （HTTP over TLS， HTTP over SSL， HTTP Secure）的简单介绍和应用。
---

## HTTPS

HTTPS 就是 HTTP Secure ，简单来说就是安全的 HTTP 协议，HTTPS 还是经由 HTTP 进行通信，但是通过 SSL/TLS 对数据包进行加密。

因为一开始 HTTP 设计的时候就没有考虑过数据保密性问题，所以在网络上的数据都是以明文形式传输的，HTTPS 的主要目的，就是提供对网络服务器的身份认证，保护交换数据的隐私和完整性，对窃听和中间人攻击提供有效的防护。

HTTP 协议的 URL 由 `http://` 起始并默认使用端口 80 ， HTTPS 协议的 URL 由 `https://` 起始并默认使用端口 443。

目前建议所有网络请求都能是 HTTPS 的，像 Google ， Facebook ， Baidu ， Taobao 等公司，都已经全站启用 HTTPS ，可以在浏览器的地址栏看到一个绿色的锁的标志。

HTTPS 的核心是 SSL (Secure Socket Layer 安全套接层)/TLS (Transport Layer Security 安全传输层协议) ，其中包含了 对称加密，非对称加密和 HASH 加密等加密方式。

在 HTTPS 协议中建立连接的时候，需要 HTTPS 证书，这个证书一般是由权威的第三方机构分发 ( Certificate Authorities )，然后在你的浏览器的网址栏里就会有一把绿色的锁，证书也可以自己生成，浏览器就会警告这是不受信任的机构分发的证书，地址栏加上一个带叉的红色的锁。

一般的证书都是要花钱购买的，不过有两个可以申请到免费的个人证书的机构，[沃通数字证书在线申请](https://buy.wosign.com/free/?lan=cn) ，这个是中国的，而且证书分发很快，在线申请，一两天就能拿到，[StartSSL™ Certificates; Public Key Infrastructure](https://www.startssl.com/) ，这个是外国的。

证书只在一开始建立连接协商密钥的时候用到，所以用自己生成的证书也可以，在证书生成之后将证书导入到浏览器之后，就不会再有警告了，虽然那个锁还是红色的。

接下来我们来生成一个 HTTPS 证书把。在 Cent OS 7 上，使用 Nginx 服务器。

## 制作使用证书

### 查看 Nginx 是否支持 ssl

```
nginx -V
```

查看 Nginx 安装的模块，寻找是否有 `http_ssl_module` 模块，一般使用 yum 安装的话会有，自行编译安装的话，需要自己装上。

### 生成证书

我们将证书放在 `/etc/nginx` 下

```
cd /etc/nginx
```

创建服务器私钥 key，这里会需要输入一个口令。

```
openssl genrsa -des3 -out server.key 1024
```

创建签名请求的证书 csr ，在 `Common Name` 的地方输入你的服务器域名。

```
openssl req -new -key server.key -out server.csr
```

在 Nginx 加载证书时无法输入口令，所以在这里需要去掉口令，虽然在上一步里必须让我们输入口令。

```
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key
```

好，这个 csr 文件与我们从网上申请购买的证书格式是一样的，接下来就可以安装了。

### 安装证书

```
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

### 配置 Nginx

修改 Nginx 配置文件 `/etc/nginx/nginx.conf`

```
server {
    server_name YOUR_DOMAINNAME_HERE;
    listen 443;
    ssl on;
    ssl_certificate /etc/nginx/server.crt;
    ssl_certificate_key /etc/nginx/server.key;
}
```

检测一下是否配置正确，注意 `ssl on;` 后面有一个分号。

```
nginx -t
```

重启 Nginx

```
sudo service nginx restart
```

你的 HTTPS 网站就可以访问了，虽然浏览器会警告证书不受信任，但还是一样有安全效果的。

修改 Nginx 以下部分，将 HTTP 的请求跳转到 HTTPS 。

```
server {
    listen 80;
    server_name ww.yousite.com;
    rewrite ^(.*) https://$server_name$1 permanent;
}
```

接下来，你可以将生成的 csr 证书导入到你电脑的证书里，这样的话就不会有警告了，但是还是红色的锁的标志，或者是使用 Cloudflare 的 CDN 加速，开启 SSL 证书。
