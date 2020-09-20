---
layout: post
title: Nginx 的深入学习
category: project
description: Nginx 着实功能强大，值得好好学习一下
---

Nginx 作为 Linux 下常用的 web 服务器之一，深入了解学习 Nginx 的是十分必要的，同时作为应用最广泛的 Linux 发行版本，Cent OS 的稳定与强大毋庸置疑，本文将主要在 Cent OS 7.0 下进行。

## 编译 Nginx

如果有一些 C 语言基础的话，编译 Nginx 的过程与编译 C 语言代码的过程并无甚区别，链接编译，生成可执行文件而已，Nginx 就是一个大型的 C 语言项目而已，编译工具同样是 gcc 。

### 安装编译工具、依赖包

```
sudo yum -y install gcc gcc-c++ autoconf automake
sudo yum -y install zlib zlib-devel openssl openssl-devel pcre-devel
```

### 新建用户组

一般 Nginx 都是作为 nginx 用户和用户组来运行，在后续的配置中也更为方便

```
sudo groupadd -r nginx
sudo useradd -s /sbin/nologin -g nginx -r nginx
```

### 下载编译安装

下载并解压

```
wget 'http://nginx.org/download/nginx-1.11.2.tar.gz'
tar -xzvf nginx-1.11.2.tar.gz
cd nginx-1.11.2/
```

配置

```
./configure --prefix=/usr/local/nginx --conf-path=/etc/nginx/nginx.conf --user=nginx --group=nginx
```

查看所有的编译选项 `./configure --help` 查看一个已经安装好的了 Nginx 的编译参数 `./nginx -V`

配置完成最后输出

```
...
Configuration summary
  + using system PCRE library
  + OpenSSL library is not used
  + using system zlib library

  nginx path prefix: "/usr/local/nginx"
  nginx binary file: "/usr/local/nginx/sbin/nginx"
  nginx modules path: "/usr/local/nginx/modules"
  nginx configuration prefix: "/etc/nginx"
  nginx configuration file: "/etc/nginx/nginx.conf"
  nginx pid file: "/usr/local/nginx/logs/nginx.pid"
  nginx error log file: "/usr/local/nginx/logs/error.log"
  nginx http access log file: "/usr/local/nginx/logs/access.log"
  nginx http client request body temporary files: "client_body_temp"
  nginx http proxy temporary files: "proxy_temp"
  nginx http fastcgi temporary files: "fastcgi_temp"
  nginx http uwsgi temporary files: "uwsgi_temp"
  nginx http scgi temporary files: "scgi_temp"
```

编译并安装

```
make && make install
```

编译之后的 nginx 可执行文件在 `/usr/local/nginx/sbin/nginx` ，配置文件在 `/etc/nginx/nginx.conf`

### 启动暂停重启

启动

```
./nginx
```

停止和重启

```
./nginx -s stop
./nginx -s reload
```

指定配置文件不重启重新载入

```
./nginx -c /etc/nginx/nginx.conf -s reload
```

一些常用的编译选项

```
--prefix=                                           #nginx安装目录，默认在/usr/local/nginx
--sbin-path=                                        #nginx可执行文件的位置，默认在 /usr/local/nginx/sbin/nginx
--modules-path=                                     #nginx模块的安装位置，默认在 /usr/local/nginx/modules
--conf-path=                                        #nginx配置文件的位置，默认在 /etc/nginx/nginx.conf
--pid-path=                                         #pid文件位置，默认在 /usr/local/nginx/logs/nginx.pid
--lock-path=                                        #lock文件位置，默认在logs目录
--error-log-path=                                   #error 日志文件的位置，默认在 /usr/local/nginx/logs/error.log
--http-log-path=                                    #access日志文件的位置，默认在 /usr/local/nginx/logs/access.log
--user=                                             #编译用户
--group=                                            #编译用户组
--add-module=                                       #为nginx编译第三方模块
--with-ipv6                                         #开启 ipv6 模块。
--with-http_ssl_module                              #开启HTTP SSL模块，以支持HTTPS请求。
--with-http_v2_module                               #开启 HTTP 2 模块
--with-http_dav_module                              #开启WebDAV扩展动作模块，可为文件和目录指定权限
--with-http_flv_module                              #支持对FLV文件的拖动播放
--with-http_realip_module                           #支持显示真实来源IP地址
--with-http_gzip_static_module                      #预压缩文件传前检查，防止文件被重复压缩
--with-http_stub_status_module                      #取得一些nginx的运行状态
--with-mail                                         #允许POP3/IMAP4/SMTP代理模块
--with-mail_ssl_module                              #允许POP3／IMAP／SMTP可以使用SSL／TLS
--with-pcre=../pcre-8.11                            #注意是未安装的pcre路径
--with-zlib=../zlib-1.2.5                           #注意是未安装的zlib路径
--with-debug                                        #允许调试日志
--http-client-body-temp-path                        #客户端请求临时文件路径
--http-proxy-temp-path=                             #设置http proxy临时文件路径
--http-fastcgi-temp-path=                           #设置http fastcgi临时文件路径
--http-uwsgi-temp-path=/var/tmp/nginx/uwsgi         #设置uwsgi 临时文件路径
--http-scgi-temp-path=/var/tmp/nginx/scgi           #设置scgi 临时文件路径
```

使用 `yum install nginx` 安装的 nginx 的编译选项是

```
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_geoip_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-google_perftools_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m64 -mtune=generic' --with-ld-opt='-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E'
```

如果在后续的重新编译安装的时候，如果想保留原来的配置文件的话，仅 `make` 而不 `make install` ，然后将当前目录下生成的 nginx 可执行文件 `./objs/nginx` 替换原来的 nginx 文件即可

## 替换已安装nginx

虽然可以编译安装，但是一般正常情况下，大部分人使用的时候，都是直接使用 `yum install -y nginx` 来自动安装 nginx 的吧。

那么在自动安装完 nginx 后，如果需要再次编辑部分模块，那么如何做编译替换呢？

### 安装编译工具、依赖包

```
sudo yum -y install gcc gcc-c++ autoconf automake
sudo yum -y install zlib zlib-devel openssl openssl-devel pcre-devel
```

### 下载指定版本

查看已安装 nginx 版本，然后下载该版本源代码

```bash
$ nginx -v
nginx version: nginx/1.16.1
$ wget http://nginx.org/download/nginx-1.16.1.tar.gz
$ tar -xzvf nginx-1.16.1.tar.gz
```

### 下载待安装模块

以安装 [ngx_http_proxy_connect_module](https://github.com/chobits/ngx_http_proxy_connect_module) 为例，可以实现 nginx 反向代理 HTTPS 请求。

```bash
$ wget https://github.com/chobits/ngx_http_proxy_connect_module/archive/master.zip
$ unzip master.zip
```

### 打入patch

根据模块说明，找到所需 patch 并打入。

```
$ cd nginx-1.16.1
$ patch -p1 < ../ngx_http_proxy_connect_module-master/patch/proxy_connect_rewrite_101504.patch
```

### 配置编译nginx

根据 `nginx -V` 查看 nginx 原始编译命令，再其基础上再加上本次所需的模块所在目录 ` --add-module=/root/nginx/ngx_http_proxy_connect_module-master`

```
$ nginx -V
nginx version: nginx/1.16.1
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-39) (GCC)
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-stream_ssl_preread_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-http_auth_request_module --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-google_perftools_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m64 -mtune=generic' --with-ld-opt='-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E'
$ ./configure --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-stream_ssl_preread_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-http_auth_request_module --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-google_perftools_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m64 -mtune=generic' --with-ld-opt='-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E' --add-module=/root/nginx/ngx_http_proxy_connect_module-master
```

编译的时候可能会遇到依赖缺失的问题,以下是一些速查

```
./configure: error: the HTTP XSLT module requires the libxml2/libxslt
yum install libxslt-devel -y

./configure: error: the HTTP image filter module requires the GD library.
 yum install gd-devel -y
 
 ./configure: error: perl module ExtUtils::Embed is required
 yum -y install perl-devel perl-ExtUtils-Embed
 
./configure: error: the GeoIP module requires the GeoIP library.
 yum -y install GeoIP GeoIP-devel GeoIP-data
 
./configure: error: the Google perftools module requires the Google perftools
yum install gperftools -y

./configure: error: SSL modules require the OpenSSL library.
yum -y install openssl openssl-devel

checking for --with-ld-opt="-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E" ... not found
./configure: error: the invalid value in --with-ld-opt="-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E"
yum install redhat-rpm-config -y

./configure: error: perl module ExtUtils::Embed is required
yum -y install perl-devel perl-ExtUtils-Embed

在执行make时候的报错：
/root/nginx-auth-ldap/ngx_http_auth_ldap_module.c:33:18: fatal error: ldap.h: No such file or directory
 #include <ldap.h>
yum install -y openldap-devel
```

配置完成之后，开始编译 `make`

***注意，这里只需 `make` 无需 `make install` ；只要编译，不要安装***

```
$ make
```

查看编译产物

```
$ ./objs/nginx -V
```

### 替换原 nginx 

```
$ which nginx
/usr/sbin/nginx
$ mv /usr/sbin/nginx /usr/sbin/nginx.bak
$ ln -s /root/nginx/nginx-1.16.1/objs/nginx /usr/sbin/nginx
```

## 动态引入模块

在 nginx 中只有版本大于 `1.7.5 ` 的才能在 cors 的设置中使用 `always` 字段，来在每一种返回状态中都带上 cors 跨域的响应头，在 nginx 版本还不到 `1.7.5` 的版本只能使用其他的扩展模块来实现添加 cors 请求头，比如 [headers-more-nginx-module](https://github.com/openresty/headers-more-nginx-module)

如果能够动态的加载第三方模块的话，就不用每次都需要重新编译 nginx 了，原生的 nginx 并不支持这样的功能，但是淘宝改良的 [tengine](http://tengine.taobao.org/) 则很早就支持 [动态加载模块](http://tengine.taobao.org/document_cn/dso_cn.html)

### 使用 dso 编译动态链接库

- 在编译 nginx 时某些官方模块暂时不需要，将其编译为动态加载库，以备后面需要。或者后续需要某些官方的模块，将其编译为独立的动态加载库。

  ```
  ./configure --prefix=/usr/local/tengine --with-http_trim_filter_module=shared
  make
  ```

  编译之后生成的动态库文件在 `objs/modules` 中。

  继续安装 nginx `make install` ，或者是安装官方库 `make dso_install`

- 编译安装某些第三方库

  ```
  cd /usr/local/tengine/sbin
  ./dso_tool --add-module=/home/dso/lua-nginx-module
  ```

  生成的编译文件已经为你放好在 `/usr/local/tengine/modules`，功能同 `make dso_install` , 也可以使用 `--dst` 参数指定生成库文件存放位置

### 配置使用 dos 动态链接库

无论是怎样获得的动态链接库，在放到指定位置之后，就可以配置使用了。

```
server {

  dso {
       load ngx_http_headers_more_filter_module.so;
  }


  more_set_headers "Access-Control-Allow-Credentials: true";
  more_set_headers "Access-Control-Allow-Origin: http://127.0.0.1:7890";
  more_set_headers 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
  more_set_headers 'Access-Control-Allow-Headers' 'Keep-Alive,User-Agent,X-Requested-With,X-Shard,Cache-Control,Content-Type';

}
```

## nginx 配置文件

nginx 的配置博大精深，学一分有一分的收获，进一寸有一寸的欢喜。

### location 路由匹配

nginx 配置中每个 server 作为一个虚拟主机，每一个 location 作为一个路由匹配。

匹配所有的路由请求

```
location / {
    index index.html;
    try_files $uri /index.html;
}
```

或者匹配静态文件

```
location ^~ /static/ {
    root /webroot/static/;
}
location ~* \.(gif|jpg|jpeg|png|css|js|ico)$ {
    root /webroot/res/;
}
```

匹配的规则是有 **优先级** 的，就是说，同时正则和字符串都匹配上了的话，会先匹配正则。

1. 全匹配 ( 也就是前缀  `=`) 表示精确匹配，不支持正则。
2. 路径匹配 （ 也就是前缀 `^~`）开头表示uri以某个常规字符串开头，不支持正则，理解为匹配url路径即可。
3. 正则匹配 （ 也就是前缀 `~` 或者 `~*`）表示区分大小写的和不区分大小写的正则匹配。`!~` 和 `!~* `开头表示区分大小写不匹配及不区分大小写不匹配的正则匹配。
4. 字符串匹配 （也就是前缀为 空）使用 `/` 的时候表示通用匹配，任何请求都会匹配，通常放着配置的最后。

> 需要注意 `^~ /333/` 表示匹配开头 ， `~ ^/333/$` 表示正则匹配开头结尾, `~ ^(/222/|/44/)` 表示匹配以 `/222/` 或者以 `/44/` 开头

示例

```
# 字符串匹配
location /static {
    alias  /home/www/static;
    access_log off;
}
# 路径匹配，此时proxy_pass的结束 / 决定是否带上匹配的路径
location ^~ /333/ {
    proxy_pass http://106.185.48.229/;
}
# 正则匹配，此时proxy_pass不能带结束 /
location ~ ^/(xxx|yyy)/ {
    proxy_pass http://106.185.48.229;
}
# 字符串匹配，此时proxy_pass的结束 / 决定是否带上匹配得路径
location /zzz/ {
    proxy_pass http://106.185.48.229/;
}
# 默认匹配
location / {
    proxy_pass http://127.0.0.1:8080;
}

location  = / {
  # 精确匹配 / ，主机名后面不能带任何字符串
  [ configuration A ]
}
location  / {
  # 因为所有的地址都以 / 开头，所以这条规则将匹配到所有请求
  # 但是正则和最长字符串会优先匹配
  [ configuration B ]
}
location /documents/ {
  # 匹配任何以 /documents/ 开头的地址，匹配符合以后，还要继续往下搜索
  # 只有后面的正则表达式没有匹配到时，这一条才会采用这一条
  [ configuration C ]
}
location ~ /documents/Abc {
  # 匹配任何以 /documents/Abc 开头的地址，匹配符合以后，还要继续往下搜索
  # 只有后面的正则表达式没有匹配到时，这一条才会采用这一条
  [ configuration CC ]
}
location ^~ /images/ {
  # 匹配任何以 /images/ 开头的地址，匹配符合以后，停止往下搜索正则，采用这一条。
  [ configuration D ]
}
location ~* \.(gif|jpg|jpeg)$ {
  # 匹配所有以 gif,jpg或jpeg 结尾的请求
  # 然而，所有请求 /images/ 下的图片会被 config D 处理，因为 ^~ 到达不了这一条正则
  [ configuration E ]
}
location /images/ {
  # 字符匹配到 /images/，继续往下，会发现 ^~ 存在
  [ configuration F ]
}
location /images/abc {
  # 最长字符匹配到 /images/abc，继续往下，会发现 ^~ 存在
  # F与G的放置顺序是没有关系的
  [ configuration G ]
}
location ~ /images/abc/ {
  # 只有去掉 config D 才有效：先最长匹配 config G 开头的地址，继续往下搜索，匹配到这一条正则，采用
    [ configuration H ]
}
```

### rewrite 路由重写

常见的路由重写有反向代理和 HTTP 转 HTTPS, 但是第一种是使用 `proxy_pass` ，对用户无感知，第二种是使用 `rewrite` ，可以对用户有感知，返回 302 ，也可以无感知。

反向代理，对用户透明

```
location / {
    proxy_pass http://127.0.0.01:8080/
}
```

HTTP 转 HTTPS，返回 302 跳转到 HTTPS 的站点

```
rewrite ^(.*) https://$server_name$1 permanent;
```

rewrite 语法规则 `rewrite [请求地址正则匹配] [替换地址规则模型] [标志位]`，一般 rewrite 也多是写在 server 里面，location 外面。

```
server {
    root /var/www/php;
    index index.php;

    rewrite ^/api/(.*)+ /index.php?app=api&method=$1 break;
    rewrite ^/index.php/(.*)+ /old_api_warning.html break;

    location / {
        return 200 "index";
    }

    location = /index.php {
        return 200 "index.php";
    }
}

```

或者是将请求路由的互换位置

```
rewrite ^/(.*)/(.*)$ /$2/$1;
# 注：用括号括起来的参数为后面的 $1 $2 变量
```

或者是去掉请求中的 `v2`

```
location ^~ /v2/ {
  rewrite ^/v2/(.*)$ /$1 last;
}
```

标志位共有以下四种, 如果替换之后的地址是一个 URL ， 则会返回 302 ，不会受标志位的影响。

1. `last`   last是不会再受其他 rewrite 影响,但会继续重试 server 中的其他 location 模块，用户无感知,地址栏不改变。
2. `break`  break是不会再受其他 rewrite 影响,而且不再进行 location 匹配，用户无感知，地址栏不变。
3. `redirect`  返回302临时重定向，浏览器地址会显示跳转后的URL地址。
4. `permanent`  返回301永久重定向，浏览器地址会显示跳转后的URL地址。

## 全局变量

nginx 配置中的全局变量

- `$query_string` : URL 中的请求参数
- `$args` : 这个变量等于请求地址中的参数，同$query_string
- `$arg_name` : 请求中的的参数名，即“?”后面的arg_name=arg_value形式的arg_name
- `$content_length` : 请求头中的 `Content-length` 字段
- `$content_type` : 请求头中的 `Content-Type` 字段
- `$document_root` : 当前请求在root指令中指定的值。
- `$host` : 请求主机头字段，否则为服务器名称。
- `$hostname` : 请求主机名
- `$http_user_agent` : 客户端agent信息
- `$http_cookie` : 客户端cookie信息
- `$http_origin` : 客户端请求来源，即请求头中的 `Origin` 字段
- `$http_host` : 客户端请求的源地址，即请求头中的 `Host` 字段
- `$limit_rate` : 这个变量可以限制连接速率。
- `$request_method` : 客户端请求的动作， 如 GET或POST。
- `$remote_addr` : 客户端的IP地址。
- `$remote_port` : 客户端的端口。
- `$remote_user` : 已经经过Auth Basic Module验证的用户名。
- `$request_filename` : 当前请求的文件路径，由root或alias指令与URI请求生成。
- `$scheme` : HTTP方法（如http，https）。
- `$server_protocol` : 请求使用的协议，通常是HTTP/1.0或HTTP/1.1。
- `$server_addr` : 服务器地址，在完成一次系统调用后可以确定这个值。
- `$server_name` : 服务器名称。
- `$server_port` : 请求到达服务器的端口号。
- `$request_uri` : 包含请求参数的原始URI，不包含主机名，”/foo/bar.php?arg=baz”。
- `$uri` : 不带请求参数的当前URI，$uri不包含主机名，如”/foo/bar.html”。
- `$document_uri` : 与$uri相同。
- `$msec` : 当前 Unix 时间戳
- `$nginx_version` : nginx 版本
- `$pid` : nginx 工作进程号
- `$proxy_protocol_addr` : 获取代理访问服务器的客户端地址
- `$http_xxxx` : xxxx 可以替换为任意 请求headers 中的值
- `$request` : 客户端的请求地址
- `$https` : 是否开启 HTTPS，如果开启就是 on
- `$request_body` : 客户端的请求主体
- `$proxy_add_x_forwarded_for` : 如果经过代理，则客户端的真实ip和代理ip
- `$status` : 服务器响应码


不太清晰，实践一下

```
    server {
        listen       8091;
          location / {
            proxy_pass http://127.0.0.1:5098;
            proxy_set_header Nginx-args $args;
            proxy_set_header Nginx-content_length $content_length;
            proxy_set_header Nginx-content_type $content_type;
            proxy_set_header Nginx-document_root $document_root;
            proxy_set_header Nginx-host $host;
            proxy_set_header Nginx-http_user_agent $http_user_agent;
            proxy_set_header Nginx-http_cookie $http_cookie;
            proxy_set_header Nginx-http_origin $http_origin;
            proxy_set_header Nginx-http_host $http_host;
            proxy_set_header Nginx-limit_rate $limit_rate;
            proxy_set_header Nginx-request_method $request_method;
            proxy_set_header Nginx-remote_addr $remote_addr;
            proxy_set_header Nginx-remote_port $remote_port;
            proxy_set_header Nginx-remote_user $remote_user;
            proxy_set_header Nginx-request_filename $request_filename;
            proxy_set_header Nginx-scheme $scheme;
            proxy_set_header Nginx-server_protocol $server_protocol;
            proxy_set_header Nginx-server_addr $server_addr;
            proxy_set_header Nginx-server_name $server_name;
            proxy_set_header Nginx-server_port $server_port;
            proxy_set_header Nginx-request_uri $request_uri;
            proxy_set_header Nginx-uri $uri;
            proxy_set_header Nginx-document_uri $document_uri;
            proxy_set_header Nginx-query_string $query_string;
            proxy_set_header Nginx-arg_name $arg_name;
            proxy_set_header Nginx-hostname $hostname;
            proxy_set_header Nginx-msec $msec;
            proxy_set_header Nginx-nginx_version $nginx_version;
            proxy_set_header Nginx-proxy_protocol_addr $proxy_protocol_addr;
            proxy_set_header Nginx-pid $pid;
            proxy_set_header Nginx-request $request;
            proxy_set_header Nginx-request_body $request_body;
            proxy_set_header Nginx-status $status;
            proxy_set_header Nginx-http_connection $http_connection;
            proxy_set_header Nginx-proxy_add_x_forwarded_for $proxy_add_x_forwarded_for;
            proxy_set_header Nginx-https $https;

          }
    }
```

查看效果,发现展示的字段比实际的少一些，因为空值的字段就没有返回

![Nginx-Builtin-Args](/images/Nginx-Builtin-Args.png)

其中 Host 字段，NGINX 拿到的 http_host 是真实请求的 host ，但是代码中拿到的是 nginx 的地址，所以一般这个字段需要修改为正确的地址。

还有 `X-Forwarded-For` 如果经过了多层代理也需要重新设置。

## Nginx 超时配置

Nginx 所处的位置，是一个中间代理层, 从浏览器发起请求到 Nginx ，然后经过转发到 应用层， `client ---> nginx ---> upstream` 。

所以在 request 的时候，nginx 先 read from client ，然后 send to upstream 。

所以在 response 的时候，nginx 先 read from upstream ，然后 send to client 。

### proxy_connect_timeout

默认 `proxy_connect_timeout 60s;`

连接后端服务的 连接超时时间，即发起握手，等待响应的超时时间。

### proxy_read_timeout

默认 `proxy_read_timeout 60s;`

在返回响应的时候，在读取后端应用的响应数据超时时间，就是在指定时间内需要返回所有数据。如果超过这段时间都没有任何数据返回，就会断开连接。

使用 nginx 代理 websocket 的时候，需要设置返回时间,否则就会断开连接，但是主要还是客户端需要保持心跳。

使用 nginx 代理 http 的时候，如果 upstream 在指定时间内无返回的话，就会报 504 (Gateway Time-out)

所以一般遇到 504 问题，就是调整这个时间。

```
Defines a timeout for reading a response from the proxied server. The timeout is set only between two successive read operations, not for the transmission of the whole response. If the proxied server does not transmit anything within this time, the connection is closed.
```

### proxy_send_timeout time;

默认 `proxy_send_timeout 60s;`

这个不知道是干什么用的，就是说即使长连接没有数据，也没有关系，不知道是啥超时。理论上说应该是 request 和 response 对应的，但是实践下来并非这样。

在请求的时候，nginx 从 client 读到数据之后，发送给后端应用的超时时间，理论上说，如果 nginx 只做转发，那这就是客户端请求的超时时间。

但是只要建立起请求，在连接之内再次发起请求的间隔时间不计？但是找不到这个到底表示什么的时间。

如果这个是 nginx 到 upstream 的那一小段，在拿到数据之后，nginx 理论上应该没有其他操作，那这个时间应该是可以小到忽略不计的。

```
Sets a timeout for transmitting a request to the proxied server. The timeout is set only between two successive write operations, not for the transmission of the whole request. If the proxied server does not receive anything within this time, the connection is closed.
```

### keepalive_timeout

默认 `keepalive_timeout 75s;`

Keep-Alive 超时时间，在 HTTP/1.1 之后，Connection 都是默认使用 Keep-Alive ，保持连接默认。但是如果在保持连接之后，一定时间内客户端都没有请求过来，那么 nginx 也会主动断开连接。

如果设置为 0，就禁止了 keepalive 连接。

### client_header_timeout

默认 `client_header_timeout 60s;`

客户端请求 headers 传输时间，即已经发送 HTTP 头的那一行之后，都是 headers ，如果在指定时间内 headers 没有发送完成，即返回 408 (Request Timeout)异常。

实际测试，并没有返回 408 ，只是 nginx 自己说返回 408，客户端啥都没收到，直接被断开连接了。

### client_body_timeout

默认 `client_body_timeout 60s;`

客户端请求 body 传输超时时间，在发送完 headers 之后，需要一个空行，然后开始发送 body 数据，如果在指定时间内 body 没有发送完成，即返回 408 (Request Timeout) 异常。

实际测试，并没有返回 408 ，只是 nginx 自己说返回 408，客户端啥都没收到，直接被断开连接了。

### send_timeout

默认 `send_timeout 60s;`

服务器端返回数据的超时时间，如果超过 60秒还未返回，nginx 断开连接。

但是它应该是只表示从 nginx 到 client 的那一小段，理论上 nginx 没有操作，这个时间小到可以忽略不计, 客户端怎么会收不到呢，客户端有问题？。

## 日志归档

nginx 在使用 yum 或者 apt 安装之后是自动安装了 logrotate，用来压缩切割日志文件，如果是手动编译安装就没有。

nginx 的 logrotate 配置文件位于 `/etc/logrotate.d/nginx` ,内容如下

```
/var/log/nginx/*log {
    create 0664 nginx root
    daily
    rotate 10
    missingok
    notifempty
    compress
    sharedscripts
    postrotate
        /bin/kill -USR1 `cat /run/nginx.pid 2>/dev/null` 2>/dev/null || true
    endscript
}
```

它会处理 `/var/log/nginx/` 下的所有 log 文件，压缩之后，用 nginx 的用户身份权限重新创建一个同名文件。
> 所以不要将你的业务日志文件放在这里，新建的日志文件你的服务用不了，😂，说多了都是泪,可能是用户权限的问题，也有可能是文件句柄的问题，没有重启服务。

然后 logrotate 只是处理日志的，你自己写一个日志处理的脚本， 也可以用 logrotate 配置。

写好 logrotate 后，使用 `logrotate -f /etc/logrotate.d/gunicorn` 运行。

logrotate 配置在 `/etc/cron.daily/logrotate` 中，会被每日执行。可以查看 `/var/lib/logrotate/logrotate.status` 中的日志归档状态。

> 正常情况下的 crontab 定时任务配置是在 `/etc/crontab` 中。

## 参考链接

[CentOS 7.0下编译安装Nginx 1.10.0](https://segmentfault.com/a/1190000005180585)   
[手动编译安装Nginx](https://xiaozhou.net/compile-nginx-manually-2015-07-23.html)   
[Module ngx_http_proxy_module](http://nginx.org/en/docs/http/ngx_http_proxy_module.html)    
[Module ngx_http_core_module](http://nginx.org/en/docs/http/ngx_http_core_module.html)   
[自动切割 Nginx 日志](https://ethendev.github.io/2019/01/10/roate-nginx-log/)   
[nginx认证走LDAP](https://blog.51cto.com/13520772/2434076)   
[Nginx做代理服务器代理支持HTTPS请求](https://www.jianshu.com/p/b1b5ef4636dd)

