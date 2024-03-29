---
layout: post
title: 安装使用 Jekyll 和 Hexo
category: project
description: 在 Github 上托管，免费的静态博客系统。
---

## Jekyll

### ruby

```
sudo apt-get install ruby-full
```

Ubuntu 截止到目前是 安装 1.9.3 的版本，所以推荐用下面的 rvm ( Ruby Version Manager ) 安装。在 Ubuntu 上可以安装 ruby2.2 ,`sudo apt-get install ruby2.2 ruby2.2-dev`

```
sudo yum install ruby
```

#### rvm

```
curl -L https://get.rvm.io | bash
```

这样的话 rvm 就安装好了

```
$ ./install.sh
Downloading https://github.com/rvm/rvm/archive/master.tar.gz

Installing RVM to /home/pi/.rvm/
    Adding rvm PATH line to /home/pi/.profile /home/pi/.mkshrc /home/pi/.bashrc /home/pi/.zshrc.
    Adding rvm loading line to /home/pi/.profile /home/pi/.bash_profile /home/pi/.zlogin.
Installation of RVM in /home/pi/.rvm/ is almost complete:

  * To start using RVM you need to run `source /home/pi/.rvm/scripts/rvm`
    in all your open shell windows, in rare cases you need to reopen all shell windows.

# Gogs,
#
#   Thank you for using RVM!
#   We sincerely hope that RVM helps to make your life easier and more enjoyable!!!
#
# ~Wayne, Michal & team.

In case of problems: https://rvm.io/help and https://twitter.com/rvm_io

```

#### ruby

安装 ruby

```
$ rvm install 2.4.0
```

ruby 加速

```
gem source -a https://gems.ruby-china.org
```

设为默认版本

```
rvm use 2.4.0 --default
```

### jekyll

修改 gem 源

```
gem sources --remove https://rubygems.org/
gem sources -a http://mirrors.ustc.edu.cn/rubygems/
```

#### 安装

```
gem install jekyll
gem install bundler
```

#### 建站

```
jekyll new blog
cd blog
bundle install
bundle exec jekyll serve
```

建好之后的目录结构一般是这样的

```
.
├── about.md
├── _config.yml
├── css
│   └── main.scss
├── feed.xml
├── Gemfile
├── Gemfile.lock
├── index.html
├── _posts
│   └── 2016-09-21-welcome-to-jekyll.markdown
└── _site
    ├── about
    │   └── index.html
    ├── css
    │   └── main.css
    ├── feed.xml
    ├── Gemfile
    ├── Gemfile.lock
    ├── index.html
    └── jekyll
        └── update
            └── 2016
                └── 09
                    └── 21
                        └── welcome-to-jekyll.html

10 directories, 15 files
```

_config.yml

网站的配置文件，也可以在命令行中设置

_posts

你的文章就写在这里，主要文章格式

_site

一旦 Jekyll 完成转换，就会默认将生成的页面放在这里。这个目录也你的 .gitignore 文件中。

.gitignore

git 默认忽略的文件，主要是 _site .sass-cache .jekyll-metadata

index.html about.md

你的主页 和 关于 页面，可以修改删除。还可以有 404 或者其他的页面，404 页面如果在根目录下会自动默认设为网站的 404 页面。

css

你的 CSS 文件夹，如果你还需要 js ，images 等文件夹 ，也是在 根目录下自己创建文件夹，然后会被默认转换到 _site 下。

Gemfile Gemfile.lock

jekyll 需要使用的插件扩展，使用 `bundle install` 安装

其实还有一个 _layout 文件夹，包含 jekyll 使用的主题，因为默认的 主题是包含在 jekyll 中，所以没有关于主题的文件夹，如果你自己创建 _layout 文件夹，并写主题文件的话，会覆盖自带的主题。

#### 使用

启动服务器，默认端口 4000.

```
jekyll serve
```

![jekyll_demo](/images/jekyll_demo.png)

显得有些问题，css 和 js 不见了，那就在 `_config.yml` 配置一下 `url` 。

![jekyll_fina](/images/jekyll_fina.png)

## Hexo

快速、简洁且高效的博客框架

### node

node 在 Ubuntu 14.04 的软件源中的版本是 0.10.25，在 Ubuntu 12.04 中的版本是 0.6.12 简直不要再低，node 最新的版本已经到了 6.2.0 的好么，稳定版也是 4.5.0 的了，在 Ubuntu 16.04 的软件源中终于正常了一些，终于回到了 4.2.6 ，但是在你想试一下最新版的时候就没有办法了。

所以我们需要 NVM ( Node Version Manager ) 可以随时下载和使用任何版本的 node ，无缝切换，还是很有用的。

#### nvm

```
curl https://raw.github.com/creationix/nvm/master/install.sh | sh
```

或者

```
wget -qO- https://raw.github.com/creationix/nvm/master/install.sh | sh
```

然后重启终端即可

```
$ nvm

Node Version Manager

Usage:
    nvm help                    Show this message
    nvm --version               Print out the latest released version of nvm
    nvm install [-s] <version>  Download and install a <version>, [-s] from source
    nvm uninstall <version>     Uninstall a version
    nvm use <version>           Modify PATH to use <version>
    nvm run <version> [<args>]  Run <version> with <args> as arguments
    nvm current                 Display currently activated version
    nvm ls                      List installed versions
    nvm ls <version>            List versions matching a given description
    nvm ls-remote               List remote versions available for install
    nvm deactivate              Undo effects of NVM on current shell
    nvm alias [<pattern>]       Show all aliases beginning with <pattern>
    nvm alias <name> <version>  Set an alias named <name> pointing to <version>
    nvm unalias <name>          Deletes the alias named <name>
    nvm copy-packages <version> Install global NPM packages contained in <version> to current version

Example:
    nvm install v0.10.24        Install a specific version number
    nvm use 0.10                Use the latest available 0.10.x release
    nvm run 0.10.24 myApp.js    Run myApp.js using node v0.10.24
    nvm alias default 0.10.24   Set default node version on a shell

Note:
    to remove, delete or uninstall nvm - just remove ~/.nvm, ~/.npm and ~/.bower folders
```

nvm 加速

```
NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/mirrors/node nvm install 4
```

#### node

查看可以安装的 node 版本

```
nvm ls-remote
```

安装最新稳定版

```
nvm install v4.5.0
```

查看已经安装的 node 版本

```
nvm ls
```

NPM (Node Package Manager) 加速

```
npm install koa --registry=http://registry.npm.taobao.org
```

### hexo

#### 安装

```
npm install hexo-cli -g
```

#### 建站

若未指定文件夹，则默认当前文件夹

```
hexo init <folder>
cd <folder>
npm install
```

新建完成后，指定文件夹的目录如下：

```
.
├── _config.yml
├── package.json
├── scaffolds
├── source
|   ├── _drafts
|   └── _posts
└── themes

```

_config.yml

网站的 配置 信息，您可以在此配置大部分的参数。

package.json

应用程序的信息。EJS, Stylus 和 Markdown renderer 已默认安装，您可以自由移除。

```
package.json
{
  "name": "hexo-site",
  "version": "0.0.0",
  "private": true,
  "hexo": {
    "version": ""
  },
  "dependencies": {
    "hexo": "^3.0.0",
    "hexo-generator-archive": "^0.1.0",
    "hexo-generator-category": "^0.1.0",
    "hexo-generator-index": "^0.1.0",
    "hexo-generator-tag": "^0.1.0",
    "hexo-renderer-ejs": "^0.1.0",
    "hexo-renderer-stylus": "^0.2.0",
    "hexo-renderer-marked": "^0.2.4",
    "hexo-server": "^0.1.2"
  }
}
```

scaffolds

模版 文件夹。当您新建文章时，Hexo 会根据 scaffold 来建立文件。

source

资源文件夹是存放用户资源的地方。除 _posts 文件夹之外，开头命名为 _ (下划线)的文件 / 文件夹和隐藏的文件将会被忽略。Markdown 和 HTML 文件会被解析并放到 public 文件夹，而其他文件会被拷贝过去。

themes

主题 文件夹。Hexo 会根据主题来生成静态页面。

#### 使用

生成静态文件

> 选项  描述 <br>
> `-d`, `--deploy`    文件生成后立即部署网站 <br>
> `-w`, `--watch` 监视文件变动 <br>

```
hexo generate
```

启动服务器，默认端口 4000

> 选项  描述 <br>
> `-p`, `--port`  重设端口 <br>
> `-s`, `--static`    只使用静态文件 <br>
> `-l`, `--log`   启动日记记录，使用覆盖记录格式 <br>

```
hexo server
```

![hexo_demo.png](/images/hexo_demo.png)

部署网站 （上传到 github）

> 参数  描述 <br>
> `-g`, `--generate`  部署之前预先生成静态文件 <br>

```
hexo deploy
```

列出网站资料

```
hexo list <type>
```

新建一篇文章。

如果没有设置 layout 的话，默认使用 _config.yml 中的 default_layout 参数代替。如果标题包含空格的话，请使用引号括起来。

```
hexo new [layout] <title>
```

简洁模式

隐藏终端信息。

```
hexo --silent
```

## Flask

Pipy 加速

这些是国内的源，使用时注意在后面加上 /simple 目录

```
http://pypi.douban.com/  豆瓣
http://pypi.hustunique.com/  华中理工大学
http://pypi.sdutlinux.org/  山东理工大学
http://pypi.mirrors.ustc.edu.cn/  中国科学技术大学
```

手动添加

```
pip install web.py -i http://pypi.douban.com/simple
```

默认添加，需要创建或修改文件。Linux 下在 `~/.pip/pip.conf`，Windows 下在 `%HOMEPATH%\pip\pip.ini`,修改为

```
[global]
index-url = http://pypi.douban.com/simple
```





参考链接

[在 CentOS 6 上安装 Jekyll](https://mos.meituan.com/library/22/how-to-install-jekyll-on-centos6/)
