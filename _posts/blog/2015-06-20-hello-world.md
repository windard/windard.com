---
layout: post
title: 使用Github Pages建独立博客
description: Github本身就是不错的代码社区，他也提供了一些其他的服务，比如Github Pages，使用它可以很方便的建立自己的独立博客，并且免费。
category: blog
---


## Hello world  !

这是第一篇文章的吧，关于 这样用 `Jekyll` 搭建一个网站，首先你需要安装以下软件

- Ruby v 1.9.3
- RubyGems
- NodeJS
- Python 2.7

尽管官方并不推荐在 Windows 上部署，但是只要环境配置好了，我在 Windows 10 上也是可以基本正常的使用 `Jekyll` .

```
C:\tmp
λ mkdir jekyll

C:\tmp
λ cd jekyll\

C:\tmp\jekyll
λ ls

C:\tmp\jekyll
λ gem install jekyll
Fetching: forwardable-extended-2.6.0.gem (100%)
Successfully installed forwardable-extended-2.6.0
Fetching: pathutil-0.14.0.gem (100%)
Successfully installed pathutil-0.14.0
Fetching: colorator-1.1.0.gem (100%)
Successfully installed colorator-1.1.0
Fetching: jekyll-3.2.1.gem (100%)
Successfully installed jekyll-3.2.1
Parsing documentation for forwardable-extended-2.6.0
Installing ri documentation for forwardable-extended-2.6.0
Parsing documentation for pathutil-0.14.0
Installing ri documentation for pathutil-0.14.0
Parsing documentation for colorator-1.1.0
Installing ri documentation for colorator-1.1.0
Parsing documentation for jekyll-3.2.1
Installing ri documentation for jekyll-3.2.1
Done installing documentation for forwardable-extended, pathutil, colorator, jekyll after 4 seconds
4 gems installed

C:\tmp\jekyll
λ ls

C:\tmp\jekyll
λ jekyll.bat new linux
New jekyll site installed in C:/tmp/jekyll/linux.

C:\tmp\jekyll
λ ls
linux/

C:\tmp\jekyll
λ cd linux\

C:\tmp\jekyll\linux
λ ls
Gemfile  _config.yml  _posts/  about.md  css/  feed.xml  index.html

C:\tmp\jekyll\linux
λ bun
bundle.bat   bundler.bat  bunzip2.exe
C:\tmp\jekyll\linux
λ bundle install
Fetching gem metadata from https://rubygems.org/............
Fetching version metadata from https://rubygems.org/...
Fetching dependency metadata from https://rubygems.org/..
Resolving dependencies...
Using colorator 1.1.0
Installing ffi 1.9.14
Using forwardable-extended 2.6.0
Installing sass 3.4.22
Using rb-fsevent 0.9.7
Installing kramdown 1.12.0
Using liquid 3.0.6
Installing mercenary 0.3.6
Installing rouge 1.11.1
Using safe_yaml 1.0.4
Installing minima 1.1.0
Using bundler 1.11.2
Installing rb-inotify 0.9.7
Using pathutil 0.14.0
Installing jekyll-sass-converter 1.4.0
Installing listen 3.0.8
Installing jekyll-watch 1.5.0
Using jekyll 3.2.1
Bundle complete! 2 Gemfile dependencies, 18 gems now installed.
Use `bundle show [gemname]` to see where a bundled gem is installed.

C:\tmp\jekyll\linux
λ bundle exec jekyll serve
Configuration file: C:/tmp/jekyll/linux/_config.yml
            Source: C:/tmp/jekyll/linux
       Destination: C:/tmp/jekyll/linux/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in 0.614 seconds.
  Please add the following to your Gemfile to avoid polling for changes:
    gem 'wdm', '>= 0.1.0' if Gem.win_platform?
 Auto-regeneration: enabled for 'C:/tmp/jekyll/linux'
Configuration file: C:/tmp/jekyll/linux/_config.yml
jekyll 3.2.1 | Error:  Permission denied - bind(2) for 127.0.0.1:4000
```

在第一次启动 Jekyll 的时候，发现没有权限，使用管理员权限的 cmd 也无法运行，不知道为什么，改用 5001 或者其他端口就可以了。

```
C:\tmp\jekyll\linux
λ bundle exec jekyll serve
Configuration file: C:/tmp/jekyll/linux/_config.yml
            Source: C:/tmp/jekyll/linux
       Destination: C:/tmp/jekyll/linux/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in 0.453 seconds.
  Please add the following to your Gemfile to avoid polling for changes:
    gem 'wdm', '>= 0.1.0' if Gem.win_platform?
 Auto-regeneration: enabled for 'C:/tmp/jekyll/linux'
Configuration file: C:/tmp/jekyll/linux/_config.yml
    Server address: http://127.0.0.1:5001/
  Server running... press ctrl-c to stop.
[2016-09-08 11:20:00] ERROR `/favicon.ico' not found.

```

`Jekyll` 官方建议在 Windows 上更新一个插件，用来实时监控网站，无法在 Windows 上使用，但是不更新也没有关系，而且我也更新失败了。

![jekyll]({{ "/images/Jekyll_show.png" | prepend: site.baseurl }})

现在我的这个网站已经挂到 `github` 上去了，在外网的网址是 `http://linux.windard.com` 可以和 `github` 完美的使用。

可是 `Jekyll` 的一些奇妙的属性让事情很难办，比如说它的所有页面都是自动生成的，要是我要自己写一个怎么办？还有 它的 css 是用 scaa 动态生成的，真是可怕，让我们来看一下它目前的结构树。

```
│  .gitignore
│  about.md
│  CNAME
│  feed.xml
│  Gemfile
│  Gemfile.lock
│  index.html
│  README.md
│  _config.yml
│
├─.sass-cache
│  ├─185a322b0b47932f9163bb07f05c07e64a1c411b
│  │      _base.scssc
│  │      _layout.scssc
│  │      _syntax-highlighting.scssc
│  │
│  └─9fe61a1e69f7769a9f2d30a4f8a73f43c8a3c643
│          minima.scssc
│
├─css
│      main.scss
│
├─images
│      Jekyll_show.png
│
├─_posts
│      2016-09-07-welcome-to-jekyll.markdown
│      2016-09-08-Install-Jekyll-In-Windows.md
│
└─_site
    │  CNAME
    │  feed.xml
    │  Gemfile
    │  Gemfile.lock
    │  index.html
    │  README.md
    │
    ├─about
    │      index.html
    │
    ├─css
    │      main.css
    │
    ├─images
    │      Jekyll_show.png
    │
    └─jekyll
        ├─update
        │  └─2016
        │      └─09
        │          └─07
        │                  welcome-to-jekyll.html
        │
        └─windows
            └─2016
                └─09
                    └─08
                            Install-Jekyll-In-Windows.html
```

Jekyll 非常高端的可以把这个根目录下的内容全部动态生成 HTML 然后放在 `_site` 里。

对了，我来试一下它能不能代码高亮。


```python
# coding=utf-8

import sys,os

print "hello world"

sys.stdout.write("hello world")

os.system("echo hello world")

```

## 修改自制主题


`Jekyll` 在装好的时候自带一个主题 `minima` ，可是非常神奇的是，这个主题没有主题文件，难道是集成在 `Jekyll` 里，这样的话让我们很难自己制作主题吖。

博客模板，有的什么都帮你做好，自动化生成，自动部署，一开始用的时候感觉很友好，但是用久了就发现它不能够定制化就不好了，而有的博客模板什么都是自己可见的，自己写的，一开始可能觉得不友好，但是用习惯了就学会自己写了，然后就不再用博客模板。

好吧，想办法把自己的模板套上去。

再来试一下语法高亮

```
def show
  @widget = Widget(params[:id])
  respond_to do |format|
    format.html # show.html.erb
    format.json { render json: @widget }
  end
end
```

Jekyll 的 minnama 是自带的，或者其他的的主题文件都不会正常显示在 Jekyll 下，不过，Jekyll 有一个神奇的特性，就是你自己的可以设定页面，来覆盖默认的主题，也就是说，你在根目录下创建目录 `_layout` 或者 `_include` ，在这里面的主题模板文件是会被首先读取的，然后再找安装的主题文件，而如果所有的主题文件都被覆盖了，那么设定使用的书体也就没有任何意义的了。

Github 的自定义域名。在使用二级域名的时候，在设定 主机的时候可以直接写自己 github 网站网址，但是当使用 Jekyll 做顶级域名的时候，就必须要一个主机，这时需要填入 Github 专门准备的两个主机名

192.30.252.153
192.30.252.154

在使用 二级域名的时候，是使用 CNAME ，在使用顶级域名的时候，是修改 A 记录。

在使用 disqus 的评论系统时，在使用通用代码的时候，首先是需要自己的一个 shortname ，如果是在 disqus 的官网拷贝下来的代码，这个shortname 都是已经写好了的，主要是以前的网上的很多博客教程都太老了，最新的 disqus 还需要一个当前页面的 url 和当前页面的 唯一编码，这去哪里找的吖，以前教程都没有写，只好自己试了一下使用 url ，可以使用，就可以了。
