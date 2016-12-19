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

在 HTTPS 协议中建立连接的时候，需要 HTTPS 证书，这个证书一般是由权威的第三方机构分发 ( Certificate Authorities，CA )，然后在你的浏览器的网址栏里就会有一把绿色的锁，证书也可以自己生成，浏览器就会警告这是不受信任的机构分发的证书，地址栏加上一个带叉的红色的锁。

在 HTTPS 中通过 非对称加密算法（公钥和私钥）交换密钥 +  数字证书验证身份（验证公钥是否是伪造的） + 利用密钥对称加密算法加密数据 来保证安全性。

一般的证书都是要花钱购买的，不过有两个可以申请到免费的个人证书的机构，[沃通数字证书在线申请](https://buy.wosign.com/free/?lan=cn) ，这个是中国的，而且证书分发很快，在线申请，一两天就能拿到，[StartSSL™ Certificates; Public Key Infrastructure](https://www.startssl.com/) ，这个是外国的。

证书只在一开始建立连接时协商密钥的时候用到，所以用自己生成的证书也可以，在证书生成之后将证书导入到浏览器之后，就不会再有警告了，虽然那个锁还是红色的。

## HTTPS 的流程

1. 客户端发出请求，你总是忘记在 URL 中加 https 的协议名，而是直接写网址，不过没有关系，一般使用 HTTPS 的站点都会将 HTTP 的请求转发到 HTTPS，所以在你还没有来得及察觉到的时候，你开始了这次的 HTTPS 连接。

2. 服务器端接受请求，返回自己的证书，证书中包括 非对称加密的公钥，一般是采用 RSA 加密，还有证书的颁发机构，过期时间，证书采用的加密方式，权威的证书分发机构的证书签名等。

3. 客户端接收到证书，解析验证证书的有效性。在这里涉及到一个 信任链 的概念，在操作系统或浏览器里是包含了一定的权威证书分发机构验证自己的证书的，这些证书被自签名，称为 根证书，然后其他的一些公司的证书是由这些权威机构分发的，这些证书由根证书签名，所以也被信任，这样信任链一步一步继承往下。虽然在密码学中是避免有绝对可信的第三方机构的，但是在这里为了防止中间人攻击，采用 信任链 来确保安全。所以如果你的证书是由一个受信任的权威分发的，浏览器开始下一步生成随机密钥，而如果你的证书是自签名的，那浏览器就会警告证书来源不受信任，是否继续前往。这里继续前往的话，也会同样的生成随机密钥，然后使用证书中的 公钥 进行加密，将密文返回服务器端。

4. 服务器端接收到密文，用自己的 私钥 解密密文，得到客户端随机生成的密钥，然后用这个密钥，采用对称加密算法开始与客户端通信。

5. 客户端知道自己生成的密钥，即可解密服务器端的数据，而其他人不知道密钥，无法解密数据，保证通信安全。

## 使用 HTTPS

接下来我们来生成一个 HTTPS 证书。在 Cent OS 7 上，使用 Nginx 服务器。

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
    server_name www.yousite.com;
    rewrite ^(.*) https://$server_name$1 permanent;
}
```

接下来，你可以将生成的 csr 证书导入到你电脑的证书里，这样的话就不会有警告了，但是还是红色的锁的标志，或者是使用 Cloudflare 的 CDN 加速，开启 SSL 证书。

在 windows 下 `运行` 里输入 `certmgr.msc` 即可打开证书管理器，linux 下 chrome 的证书管理在 `设置` 中。

在 Cpanel 使用 沃通 的 HTTPS 证书时，可能会出现

```
Certificate verification failed!The system did not find the Certificate Authority Bundle that matches this certificate.
Contact “WoSign CA Limited” to obtain the Certificate Authority Bundle for “WoSign CA Free SSL Certificate G2”.
```

这是因为 Cpanel 中没有 沃通的 HTTPS 根证书，未能形成一个完整的 HTTPS 信任链，需要在 Cpanel 提交 自己的 HTTPS 证书时，在其可选的 `证书颁发机构包: (CABUNDLE)` 内填入沃通提供的 沃通根证书 即可。
