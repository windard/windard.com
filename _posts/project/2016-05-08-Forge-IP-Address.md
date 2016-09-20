---
layout: post
title: 通过修改http请求的header请求头来伪造ip
category: project
description: 之前一直想在TCP/IP层伪造ip，但是比较困难，发现可以在http层简单的伪造一下，虽然还是可能被发现。
---

## 前言
在正常的tcp/ip协议中是很难伪造ip的，因为在tcp/ip正式通信之前是有一个三次握手的过程，通过三次握手建立了tcp/ip连接之后再进行正常的通信，所以我之前想用python的scapy库来伪造其他ip的请求包，但是因为三次握手的时候，我的ip是伪造的，我发出去的请求包就没有办法正确的返回找到我，所以无法三次握手就没有tcp/ip正常通信，就失败了。

只要能够在tcp/ip层伪造ip，就是完全的伪造ip，没有任何办法判断，不过我这次的是在http层伪造ip，所以还是可能被发现的，而且也只有在http协议中有用，无法利用在其他地方。

## header

那么如何在http层伪造协议呢？我们先来了解一些http请求中的请求头header，比如说我们在chrome中登陆百度，打开chrome的开发者工具，查看network，就能够看到这次请求百度的header请求头。

Requests Headers

```
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:zh-CN,zh;q=0.8
Connection:keep-alive
Cookie:BIDUPSID=XXX; PSTM=XXX; BAIDUID=XXX:FG=1; BDUSS=XXX; __cfduid=XXX; ispeed_lsm=2; BD_HOME=1; BDRCVFR[Ups602knC30]=XXX; BD_CK_SAM=1; H_PS_PSSID=XXX; BD_UPN=XXX; H_PS_645EC=XXX; locale=XXX; BDSVRTM=0; BD_LAST_QID=XXX
Host:www.baidu.com
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36
```

可以看到这里有很多的请求参数，在我们打开百度的时候，我们先要向百度服务器发送一个请求，而这个请求包含很多附加的关于我们自己的信息，比如说浏览器信息，cookie，接受数据格式等等，百度服务器收到我们的请求之后，返回给我们百度的页面。

> 在我们发送http请求之前，就已经先进行了tcp/ip三次握手，然后再发送http请求，三次握手的过程是非常迅速的，可以用抓包工具 wireshark 查看。

所以 header 请求头主要是一些我们发送请求时附带的我们自己的信息，同时，在看到 header 请求头的时候，也会发现在服务器返回数据的时候也会带有一个 header ，这是返回数据格式的一些信息，包括返回数据的格式，大小，时间等。

## X-Forwarded-For

接下来就是我们伪造ip的核心了，header 请求头中的 X-Forwarded-For 参数 ，这是一个用来识别http代理或负载平衡的原始ip的一个非rfc标准，就是在http请求中有时会使用代理，或者是负载均衡的时候通过了一个转发，这样的话原始ip就被隐藏起来了，这个参数就是为了标注出原始ip，格式是`X-Forwarded-For:client1, proxy1, proxy2 ...` 第一个是原始ip，后面是经过的代理。

本来这个参数是挺好的，可以判断你是否经过代理判断原始ip，不过一般使用代理的人不就是为了不被别人发现自己的真实ip么？所以这个参数也没用成为rfc的标准，默认是没有的，不强制添加。

所以这样的话，我们本来没有使用代理，就是真实ip，是不是就可以通过增加一个这样的 header 参数来伪造自己经过了代理呢？然后加入我们伪造的 ip ，让服务器以为它是真实的ip。

这样的一个思路看起来是挺好的，那么接下来我们看一下服务器是如何得到我们的ip的。

## 服务器如何得到客户ip的

在这里以php为例，在php里有三个值保存客户ip，分别是 `HTTP_CLIENT_IP`,`HTTP_X_FORWARDED_FOR`,`REMOTE_ADDR` 。

`$_SERVER['HTTP_CLIENT_IP']` 如果有代理服务器，一般是代理服务器ip，没有则为空
`$_SERVER['HTTP_X_FORWARDED_FOR']` 如果有代理服务器的话，一般是原始ip，没有则为空，若有多个则也显示代理服务器ip
`$_SERVER['REMOTE_ADDR']` 如果有代理服务器的话，则为最后一个代理的ip，没有则为连接的客户端ip

可以看到有很多的`一般`，也就是说前两个都是可以伪造的，最后的一个倒是很难伪造，不过如果真的有代理的话，最后一个也没有什么用。

所以，如何得到真实的客户端ip也是一个很头疼的问题，现在一般的做法是先取得 `$_SERVER['REMOTE_ADDR']` 然后再判断有没有代理，如果有代理则获得原始ip，如果有，则将原始ip作为客户端的ip，比如说采用这种做法的有discuz。

在 discuz 的当前最新版 X3.2 中，可以在 `/source/class/discuz/discuz_application.php` 中找到其获取客户端ip的函数 `_get_client_ip` ,函数如下。

```php
    private function _get_client_ip() {
        $ip = $_SERVER['REMOTE_ADDR'];
        if (isset($_SERVER['HTTP_CLIENT_IP']) && preg_match('/^([0-9]{1,3}\.){3}[0-9]{1,3}$/', $_SERVER['HTTP_CLIENT_IP'])) {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif(isset($_SERVER['HTTP_X_FORWARDED_FOR']) AND preg_match_all('#\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}#s', $_SERVER['HTTP_X_FORWARDED_FOR'], $matches)) {
            foreach ($matches[0] AS $xip) {
                if (!preg_match('#^(10|172\.16|192\.168)\.#', $xip)) {
                    $ip = $xip;
                    break;
                }
            }
        }
        return $ip;
    }
```

也有用这样的函数来取得客户端的ip，不过想法都是一样的，只是实现不一样。

```
function GetIP(){
    if(!empty($_SERVER["HTTP_CLIENT_IP"]))
        $cip = $_SERVER["HTTP_CLIENT_IP"]
    else if(!empty($_SERVER["HTTP_X_FORWARDED_FOR"]))
        $cip = $_SERVER["HTTP_X_FORWARDED_FOR"]
    else if(!empty($_SERVER["REMOTE_ADDR"]))
        $cip = $_SERVER["REMOTE_ADDR"]
    else
        $cip = "无法获取！";
    return $cip;
}
```

## 总结
测试了一下使用 discuz 的情况，确实是可以伪造ip的，特别是在使用discuz插件投票的时候，可以恶意刷票，不过为了防止这种情况的发生，在服务器端可以通过设置服务器来过滤，这里就不再展开详叙了。
