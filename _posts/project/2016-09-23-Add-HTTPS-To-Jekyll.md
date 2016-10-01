---
layout: post
title: 给 Jekyll 配置 HTTPS
category: project
description: Github Pages 如果使用它的域名，即 *.github.io 是自带 HTTPS 的，但是一旦你使用自定义域名，就没有 HTTPS了。
---

Github 是个好东西，不仅有免费的代码托管，而且还能为你托管的代码提供一个运行环境，即 Github Pages，现在有很多人 Github Pages 做自己的博客网站，比如我。一般可以用 Jekyll ， Hexo ， Octopress 等，使用这些框架可以更快的搭建一个 Github Pages 可以解析的静态博客网站。

HTTPS 是 HTTP Secure，即更安全的 HTTP 协议，目前建议是所有的网络请求都能是 HTTPS 的，像 Google ， Facebook ， Baidu ， Taobao 等公司，都已经全站启用 HTTPS ，可以在浏览器的地址栏看到一个绿色的锁的标志，而且 Google 会优先选择 HTTPS 网页而不是等效的 HTTP 网页作为规范网址，优先收录。

在使用 Github Pages 搭建博客网站还有一个好处就是 Github 会提供给你一个免费的二级域名，类似于 `*.github.io` ，* 为你在 Github 上的注册名，如果你使用这个域名作为你的博客网站的话，是自带 HTTPS 的，因为 Github 购买了 github.io 的 HTTPS 证书，但是如果你使用自定义域名的话，就没有免费的 HTTPS 了，因为证书只注册给 `github.io` 下的所有子域名，而你的自定义域名是不符合这一规则的。在浏览器上如果你登陆你 HTTPS 的个人域名网站，浏览器会警告该网站证书不可用，因为证书注册域名和你的域名不匹配。

因为 Github Pages 不支持上传证书，且无法配置证书文件，所以无论你是 Jekyll，还是 Hexo，即使申请购买到了 HTTPS 的证书也无法使用。所以如果想要给你的网站配置 HTTPS ，就不能使用一般的静态证书，只能在 DNS 域名解析的时候给你提供一个动态的 HTTPS 证书。

我采用的办法就是 使用 cloudflare 的 DNS 域名解析服务，并绑定动态 HTTPS ， 即不用我申请证书，也不用我保存证书，所有的都是在 DNS 那里动态的加载 HTTPS ，而且更重要的是，这一切都是免费的，你可以在地址栏里看到我的网址前面有一个绿色的锁。

Githu Pages 可以绑定你的 顶级域名，即 `XXX.XX` ，就像我的博客网站 `windard.com` ，或者是类似于 `blog.XXX.XX` 的二级域名。绑定二级域名需要在 DNS 里加一个 CNAME 规则，指向你的 `*.github.io`  就可以。绑定顶级域名则是加一个 A 规则，需要指定 Host 主机，Github Pages 提供了两个[主机](https://help.github.com/articles/setting-up-an-apex-domain/)，随便选择一个就可以，或者是加一个 ANAME 或 ALIAS 规则，可惜我的 DNS 服务商并不支持这两种规则 。

这里假设你的个人博客网站已经搭好了，不带 HTTPS 的自定义域名可以正常访问。那我们开始加 HTTPS 把。

1. 注册 [Cloudflare](https://www.cloudflare.com/) 账号。

2. 在你的域名注册商那里，将 nameservers ( DNS 服务提供商 ) 换为 Cloudflare ，在你注册了 Cloudflare 之后它就会对你的 域名 进行一些检测操作，你就跟着它的步骤来就可以。

3. 在 Cloudflare 的 控制面板里，找到 `Crypto` 下的 `SSL` ，选择 `Flexible SSL` 即可。

在更改完成后大概半个小时 DNS 更新了你就可以访问你的 HTTPS 的网站了，此时你的 HTTP 与 HTTPS 的网站都存在，如果你想要将你的 HTTP 的网站全部转发到 HTTPS 的网站，首先将你的 `_config.yml` 文件中的 `url` 修改一下，并在你的模板文件中，将每一个页面前加上一段 Javascript，将 HTTP 的网站全部跳转 HTTPS 的网站。

_config.yml

```
url: https://www.yoursite.com   # with the https protocol
enforce_ssl: www.yoursite.com   # without any protocol

# For example, my configuration is this:
url: https://windard.com
enforce_ssl: windard.com
```

将以下 Javascript 加到你的网页的 `<head>` 标签中。

```
<script type="text/javascript">
    var host = "yoursite.com";
    if ((host == window.location.host) && (window.location.protocol != "https:"))
        window.location.protocol = "https";
</script>
```

同时将你的网站中所有以 HTTP 形式加载的 文件全部改为 HTTPS ，如 CSS , JS 和图片。

```
<!-- Change this -->
<link rel="stylesheet" href="http://www.yoursite.com/path/to/styles.css">

<!-- to this: -->
<link rel="stylesheet" href="//www.yoursite.com/path/to/styles.css">
```

最后，如果你还要再加强一下 SEO ，告诉网站爬虫你的站已经全面升级为 HTTPS，不要再爬 HTTP 的站了，那就将下面的一句添加你的网页的 `<head>` 标签中。

```
<link rel="canonical" href=" { { site.url } }{ { page.url } }" />
```

最近新看到一个将 HTTP 转 HTTPS 的办法，其实就在 CloudFare 里面，设置一个 `Page Rules ` 页面规则就可以了。

设定 `Always Use HTTPS`,让所有的 `http://windard.com/* `的连接自动跳转到.

参考链接

[Set Up SSL on Github Pages With Custom Domains for Free](https://sheharyar.me/blog/free-ssl-for-github-pages-with-custom-domains/)

[Setting up SSL on GitHub Pages](https://blog.keanulee.com/2014/10/11/setting-up-ssl-on-github-pages.html)
