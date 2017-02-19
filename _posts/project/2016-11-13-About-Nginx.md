---
layout: post
title: Nginx 的配置和使用
category: project
description: Nginx 的配置详解，虚拟主机，反向代理，基本认证和负载均衡。
---


## Nginx

Nginx 作为 web 服务器消耗是极少的，树莓派上都可以跑，性能是强悍的，比 Apache 不知道高到哪里去了，配置简单，快速上手，功能强大。现在越来越多的 web 服务器选择了 Nginx ，相信它还是可以的。

## 安装使用

在 Cent OS 7 上直接使用 yum 安装就可以使用

```
yum install nginx
```

开启，停止，查看状态，重新载入，重新启动，测试配置文件

```
service nginx start
service nginx stop
service nginx status
service nginx reload    // service nginx -s reload 平滑重启
service nginx restart
nginx -t                // 测试现在的配置文件是否有效
```

配置文件位置 `/etc/nginx/nginx.conf`

## 配置文件详解

```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers HIGH:!aNULL:!MD5;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}
```

看起来有很多，其实主要分为一下几大块

```
main
events   {
  ....
}
http        {
  ....
  upstream myproject {
    .....
  }
  server  {
    ....
    location {
        ....
    }
  }
  server  {
    ....
    location {
        ....
    }
  }
  ....
}
```

这留个部分分别是 `main(全局配置)` `events(Nginx 工作模式)` `http(HTTP 设置)` `server(主机设置)` `location(URL 匹配)` `upstream(负载均衡设置)`

### main 模块

```
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;
```

`user` 用来指定 Nginx worker 进程运行用户及用户组，一般使用 `user nobody nobody;`

`worker_processes` 指定 Nginx 开启的子进程数，一般使用 CPU 核数*2 就可以，Nginx 是多线程服务器，对每个连接开启一个线程，Apache 则是多进程服务器。

`error_log` 定义全局错误日志，日志输出额级别有 `debug` `info` `notice` `warn` `error` `crit` 可选，其中 `debug` 输出最为详细，`crit` 输出最少。

`pid` 指定进程 ID 的存储文件位置。

`worker_rlimit_nofile` 用来指定一个 Nginx 的进程可以打开的最多文件描述符数目，默认是 65535 ， 同时需要在 cent OS 中使用 `ulimit -n 65535` 设置，这里没有设置。

`include` 导入其他的配置文件，这里值导入 `/usr/share/nginx/modules` 目录下所有的配置文件。 

### events 模块

用来指定 Nginx 的工作模式和连接数上限。

```
events {
    worker_connections 1024;
}
```

`use` 指定 Nginx 的工作模式，Nginx 支持的工作模式有 `select` `poll` `kqueue` `epoll` `rtsig` 和 `/dev/poll` ，后两种使用的不多，`select` 和 `poll` 是传统的标准工作模式，`queueu` 是高效的工作模式，不同的是 `epoll` 只支持 Linux 平台上，`kqueue` 只支持 BSD 平台，对于 Cent OS 系统，在这里可以加上 `use epoll` 来提高工作效率。

`worker_connections` 最大连接数，最大连接客户数由 `worker_processes` 和 `worker_connections` 共同决定 `Max_clients = worker_processes * worker_connections`

### http 模块

这可以说是 Nginx 的核心模块，指定 HTTP 服务器的相关属性和配置，其 server 和 upstream 子模块至关重要。

```
http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        ...
    }

}
```

`log_format` 日志文件格式定义，在默认提供的几种文件格式之外指定设置一种正常记录访问连接的日志格式，也是最常用的日志格式。

`access_log` 设置正常访问连接的日志存储，使用上面定义的 `main` 格式

`sendfile` 开启高效文件传输，同时将 `tcp_nopush` 和 `tcp_nodelay` 开启来防止网络阻塞。

`keepalive_timeout` 设置客户端的保持连接活动的超时时间。

`include` 设置文件的 mime 格式，可以在 `/etc/nginx/mime.types` 中查看 Nginx 支持的网络传输文件格式。

`default_type` 设置默认的文传输格式为二进制流，这样可以有效防止文件上传漏洞，以及在未配置好 PHP 或 ASP 等配置环境时，一切不认识的文件都不会被执行，而是被默认下载。

`include` 又有一个 `include` 这里还是配置文件的，在 `/etc/nginx/conf.d` 文件夹下的配置文件也会被包含进来。

### server 模块

server 用来定义一个虚拟主机，最少只需要三条配置即可，`listen` 监听的端口，`server_name` 监听的服务器名，可以是 IP 也可以是域名，`location` 请求的资源定位。

```
    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
```

`listen` 监听的端口，默认是 80 端口，即 HTTP 协议的端口，它不但监听了 IPv 4 的 80 端口，还监听 IPv 6 的 80 端口，虽然我的服务器还没有 IPv 6 的 IP。

`server_name` 监听的所有的请求，无论是外网请求还是内网请求还是内网请求，在这里就可以设置不同的虚拟主机监听不同的请求。

`root` 默认的资源位置，即网站根目录位置 `/usr/share/nginx/html`，可以使用绝对路径也可以使用相对路径，如 `root html;` 即表示 `/usr/share/nginx/test` 。

`include` 又一次包含配置文件，这次的配置文件位置在 `/etc/nginx/default.d` 目录下。

`error_page` 定义默认错误页面， 404 为根目录下 `404.html` 页面，500 502 503 504 等服务器内部错误页面为 `50x.html` 页面。

### location 模块

这个模块用来定义请求的资源位置，就可以用来设置不同的虚拟主机的内容，还可以设置反向代理和负载均衡。

```
    location / {
    }
```

非常神奇的是默认的 location 是空的，只有一个 `/` 表示匹配根目录，根目录的位置在 http 模块里也定义了默认为 `/usr/share/nginx/html` ，所以它可以是空的。

那我们来看一份已经使用 PHP-fpm 配置好 PHP 的 locating 模块。

```
    location / {
            root html;
            index index.html index.htm index.php;
    }

    location ~ \.php$ {
            root            /usr/share/nginx/html;
            fastcgi_pass    127.0.0.1:9000;
            fastcgi_index   index.php;
            fastcgi_param   SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            include         fastcgi_params;
    }
```

`root` 同样为虚拟主机的根目录，一般来说，要是在 server 已经设定了 `root` 地址的话，在 location 中设置 `root` 就不再解析。

`index` 表示默认首页，在默认只有 `index.html` 和 `index.htm` ，在配置 PHP 的时候，需要手动加上 php 结尾的 index 文件。

`location` 使用正则匹配来选择所有以 `.php` 结尾的 URL ，来解析 PHP 文件 。

`fastcgi_pass` 链接到 PHP-fpm 的解析地址，可以像这样使用端口转发解析，也还可以使用 Unix sock 发送给 PHP 解析，下面的几个参数都是解析 PHP 用。

在下面还有一个被注释掉的 server ，可以查看注释知道其是为了 HTTPS 搭建的一个虚拟主机，暂先不表。

### upstram 模块

这个模块主要负载均衡，负载均衡即对外一个网站，对内多台服务器，多台服务器提供统一服务，对用户透明，实现一对多的映射。在网站逐步扩大，用户量递增的时候，仅靠一台服务器已不足够承受巨大的访问量时，我们就需要多台服务器构成集群，统一对外提供相同的服务，这些服务器之间的调度，网络资源的分配就是负载均衡。

## Nginx 的虚拟主机

Nginx 有三种不同的虚拟主机，分别是基于域名，基于端口和基于 IP 的虚拟主机，也就是在 server 模块中 `listen` 不同的端口，`server_name` 对应不同的 域名和 IP 。

### 基于域名的虚拟主机

假设我们现在有三个不同的项目搭建在本机，在 `/etc/hosts` 中映射到本地的 127.0.0.1 上:

```
127.0.0.1       www.test.com test.com
127.0.0.1       api.test.com
127.0.0.1       admin.test.com
```

这三个不同的项目地址是

```
/usr/share/nginx/www.test.com
/usr/share/nginx/api.test.com
/usr/share/nginx/admin.test.com
```

每一个项目中有一个 `index.php` 文件，分别输出自己的域名，然后我们就来创建这样的三个虚拟主机，为了不与默认的配置文件弄混，我们在 `/etc/nginx/conf.d` 目录下新建一个 `test.conf` 的配置文件。

```
server {
        listen 80;
        server_name www.test.com test.com;

        root /usr/share/nginx/www.test.com;
        index index.php index.html index.htm;

        access_log  /var/log/nginx/www.access.log  main;
        error_log   /var/log/nginx/www.error.log error;


        location ~ \.php$ {
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_index index.php;
                include fastcgi.conf;
        }
}
server {
        listen 80;
        server_name api.test.com;

        root /usr/share/nginx/api.test.com;
        index index.php index.html index.htm;

        access_log  /var/log/nginx/api.access.log  main;
        error_log   /var/log/nginx/api.error.log error;


        location ~ \.php$ {
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_index index.php;
                include fastcgi.conf;
        }
}
server {
        listen 80;
        server_name admin.test.com;

        root /usr/share/nginx/admin.test.com;
        index index.php index.html index.htm;

        access_log  /var/log/nginx/admin.access.log  main;
        error_log   /var/log/nginx/admin.error.log error;

        location ~ \.php$ {
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_index index.php;
                include fastcgi.conf;
        }
}
```

使用 

```
nginx -t
```

来测试配置文件是否书写错误，然后重启服务器

```
service nginx restart
```

因为是服务器上，所以通过 `curl` 来查看效果。

```
curl www.test.com
curl admin.test.com
curl api.test.com
```

应该是三个不同的结果，分别输出自己的域名。如果有自己的域名的话，也只需要在 DNS 的解析记录里加上三条 A 记录指向自己服务器的 IP 即可，这样的话访问不同的域名就是不同的内容，但是都是在同一个主机上。

### 基于 IP 的虚拟主机

既然可以使用不同的域名访问不同的 IP ，也就可以基于不同的 IP 来访问不同的内容，我们让从内网访问和外网访问不同的内容，配置文件如下。

```
server {
        listen 80;
        server_name 182.254.216.215;

        root /usr/share/nginx/outter;
        index index.php index.html index.htm;

        access_log  /var/log/nginx/outter.access.log  main;
        error_log   /var/log/nginx/outter.error.log error;

        location ~ \.php$ {
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_index index.php;
                include fastcgi.conf;
        }
}
```

然后在默认的配置文件 `/etc/nginx/nginx.conf` 中，将 `server_name` 改为 `localhost` ，然后重启 Nginx 。

同样的通过 `curl localhost` 和 `curl 182.254.216.215` 的结果也就不一样，也可以直接通过外网 IP 访问查看。

### 基于端口的 虚拟主机

同一服务器，也可以通过 Nginx 来让不同的端口访问不同的内容，当然你的防火墙 firewalld 或者 iptables 需要开放对应端口或关闭防火墙。

## 反向代理

代理，如果你用过其他的代理软件，比如说 shadowsocks ，就会知道什么是正向代理，即它的功能就像一个跳板。假设你需要访问 Google ，但是在中国大陆没法直接访问 Google ，不过你可以访问这个代理服务器，那你就先到这个代理服务器上，然后通过代理服务器访问 Google 。其实到了代理服务器上你访问哪里都可以，目标地址，如 Google，还以为是代理服务器访问的。这就是正向代理，它是位于 `客户端` 与 `代理服务器` ，到了代理服务器之后，你想去哪去哪，代理服务器管不着，也不知道。

那么反向代理就是位于 `代理服务器` 与 `目标地址` 之间的，你正常访问代理服务器，然后服务器就去把目标地址的资源取来给你，你只能得到代理服务器给你的资源而没得选。你本来正常访问代理服务器，结果却得到了目标服务器的资源，这就是反向代理，比如说 Google 镜像网站。

如果想使用反向代理，需要设定服务器开启转发功能，查看 `/proc/sys/net/ipv4/ip_forward` 的值是否为 1，如果不是请改为 1 。

比如说我们来搭建一个 Google 的镜像网站

```
server {
        listen 80;
        server_name search.windard.com;

        access_log /var/log/nginx/search.windard.access.log main;
        error_log /var/log/nginx/search.windard.error.log error;

        location / {
                proxy_pass https://www.google.com;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

当然前提是你的服务器能访问 Google ，我搭了一个 Google 的镜像网站在 `http://search.windard.com/` 可以一试。

或者我们在 8000 端口用 Python 搭建了一个 HTTP 服务器，但是我们不想让别人知道这是在 8000 端口，或者我们的对外端口只开了 80 ，那么我么就可以使用反向代理来让访问 80 端口也能得到 8000 端口的内容。

```
server {
        listen 80;
        server_name search.windard.com;

        access_log /var/log/nginx/python.access.log main;
        error_log /var/log/nginx/python.error.log error;

        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

其实如果是在本机上的话，使用 iptables 的 DNAT ，一句话就可以搞定

```
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000
```

## 负载均衡

一般常用的负载均衡的办法

1. DNS 轮询，即同一个域名有一个不同的IP，在不同的时间或者地点被分配到不同的服务器上。

2. CDN (Content Delivery Network) ，内容分发网络，对于一些不太重要的静态资源，如 css，js，图片等，可以使用 CDN 。

3. IP 负载均衡，如使用 NAT，在内网分发流量，或者使用硬件实现，如 F5。

Nginx 也提供了强大而又简单的负载均衡功能，Nginx 的主要四种调度算法

- weight 轮询（默认），每个请求按时间顺序逐一分配到不同的后端服务器，如果某一台后端服务器宕机，故障系统被自动剔除，使用户访问不受影响。weight ，指定轮询权重，weight 越大，分配到的访问几率越高，主要用于后端服务器性能不均的情况下。

- ip_hash ，每个请求按访问 IP 的hash 结果分配，这样来自同一个 IP 的访客固定访问一个后端服务器，可以有效解决动态网页的 session 存储问题。

- fair ，比上面两个更智能的负载均衡调度算法。这种算法可以根据页面大小和加载时间的长短来智能的进行负载均衡，也就是根据不同的后端服务器对不同的访问请求的响应时间来分配，以确保每一个访问都是使用最短的加载时间的服务器。Nginx 本身是不支持这种调度算法，需要加载 Nginx 的 upstream_fair 来使用这种调度算法。

- url_hash 按照 URL 的 hash 结果来分配请求，每一个 URL 对应一个后端服务器，可以有效利用后端缓存服务器。Nginx 本身是不支持这种调度算法，需要加载 Nginx 的  upstream_hash 来使用这种调度算法。

### 环境配置 

在 Cent OS 7 中装好 Docker ，使用 Docker-compose 构建 3 个 Nginx 容器，容器与主机采用网桥连接，自动分配 IP，在 Cent OS 中使用 Docker 的话需要注意 SELinux 。

docker-compose.yml

```
version: '2'
services:
    web1:
        image: nginx
        working_dir: /usr/share/nginx/html
        volumes: 
            - ./web1/html:/usr/share/nginx/html
    web2:
        image: nginx
        working_dir: /usr/share/nginx/html
        volumes: 
            - ./web2/html:/usr/share/nginx/html
    web3:
        image: nginx
        working_dir: /usr/share/nginx/html
        volumes: 
            - ./web3/html:/usr/share/nginx/html
```

启动容器

```
docker-compose up -d
```

分别查看容器的 IP 地址

```
docker-compose exec web1 ip addr
docker-compose exec web2 ip addr
docker-compose exec web3 ip addr
```

主机的 IP 为 `172.20.0.1` 三个容器的 IP 地址分别为 `172.20.0.2~4`

```
[root@localhost nginx]# curl http://172.20.0.2
This is web 2
[root@localhost nginx]# curl http://172.20.0.3
This is web 3
[root@localhost nginx]# curl http://172.20.0.4
This is web 1
```

### 基于权重的 负载均衡

upstream 配置

```
upstream webservers{
    server 172.20.0.2 weight=10;
    server 172.20.0.3 weight=10;
    server 172.20.0.4 weight=10;
}
server {
    listen 80;
    server_name 172.20.0.1;
    access_log /var/log/nginx/upstream.access.log main;
    error_log /var/log/nginx/upstream.error.log error;
    location / {
        proxy_pass http://webservers;
        proxy_set_header  X-Real-IP  $remote_addr;
    }
}
```

查看效果

```
[root@localhost nginx]# curl 172.20.0.1
This is web 2
[root@localhost nginx]# curl 172.20.0.1
This is web 3
[root@localhost nginx]# curl 172.20.0.1
This is web 1
```

因为权重相同，所以三个服务器出现的频率是相同的。然后查看日志

```
[root@localhost nginx]# cat /var/log/nginx/upstream.access.log
192.168.137.129 - - [18/Feb/2017:23:34:20 +0800] "GET / HTTP/1.1" 200 14 "-" "curl/7.29.0" "-"
192.168.137.129 - - [18/Feb/2017:23:34:21 +0800] "GET / HTTP/1.1" 200 14 "-" "curl/7.29.0" "-"
192.168.137.129 - - [18/Feb/2017:23:34:22 +0800] "GET / HTTP/1.1" 200 14 "-" "curl/7.29.0" "-"
```

其他参数

- `max_fails ` 允许请求失败的次数，默认为 1，即在一次请求失败之后暂停使用这个后台服务器
- `fail_timeout ` 在经历了 max_fails 次请求失败之后，暂停服务的时间，默认为永久

- `down` 停止使用这个后台服务器，相当于未加入负载均衡中
- `backup` 备用后台服务器，在其他服务器都不能使用时，才开始工作

在负载均衡的过程中，若是我们暂停一台后台服务器，Nginx 会自动切换，该机器不再继续提供服务。

我们停掉 web2 的后台服务器

```
[root@localhost nginx]# docker-compose stop web2
Stopping nginx_web2_1 ... done
[root@localhost nginx]# curl 172.20.0.1
This is web 3
[root@localhost nginx]# curl 172.20.0.1
This is web 1
[root@localhost nginx]# curl 172.20.0.1
This is web 3
[root@localhost nginx]# curl 172.20.0.1
This is web 1
[root@localhost nginx]# curl 172.20.0.1
This is web 3
```

在超过 Nginx 中设置的超时时间没有返回数据之后就会进行自动切换，设置的超时时间为 65 秒，在后面的请求中也将不再使用请求失败的服务器。

查看日志

```
[root@localhost nginx]# cat /var/log/nginx/upstream.error.log
2017/02/18 23:54:53 [error] 20547#0: *13 connect() failed (113: No route to host) while connecting to upstream, client: 192.168.137.129, server: 172.20.0.1, request: "GET / HTTP/1.1", upstream: "http://172.20.0.2:80/", host: "172.20.0.1"
```

现在测试一下 备用服务器，一台停用，一台启用，一台备用。

```
upstream webservers{
    server 172.20.0.2 down;
    server 172.20.0.3 ;
    server 172.20.0.4 backup;
}
```

重启 Nginx ，访问 172.20.0.1 ，只有 web3 提供服务。

```
[root@localhost nginx]# service nginx restart
Redirecting to /bin/systemctl restart  nginx.service
[root@localhost nginx]# curl 172.20.0.1
This is web 3
[root@localhost nginx]# curl 172.20.0.1
This is web 3
[root@localhost nginx]# curl 172.20.0.1
This is web 3
```

停用 web3 再次访问

在 65 秒的超时时间后，判断出当前服务器已经无法提供服务且无其他服务器工作，即启用备用服务器。

```
[root@localhost nginx]# docker-compose stop web3
Stopping nginx_web3_1 ... done
[root@localhost nginx]# curl 172.20.0.1
This is web 1
[root@localhost nginx]# curl 172.20.0.1
This is web 1
[root@localhost nginx]# curl 172.20.0.1
This is web 1
```

### 基于 ip_hash 的负载均衡

upstream 配置

```
upstream webservers{
    ip_hash;
    server 172.20.0.2 weight=10;
    server 172.20.0.3 weight=10;
    server 172.20.0.4 down;
}
```

重启服务器，查看访问效果

```
[root@localhost nginx]# service nginx restart
Redirecting to /bin/systemctl restart  nginx.service
[root@localhost nginx]# curl 172.20.0.1
This is web 2
[root@localhost nginx]# curl 172.20.0.1
This is web 2
[root@localhost nginx]# curl 172.20.0.1
This is web 2
```

同一个 ip 访问总是得到同一个服务器的返回，接下来我们调整一下不同服务器的权重。

```
upstream webservers{
    ip_hash;
    server 172.20.0.2 weight=10;
    server 172.20.0.3 weight=20;
    server 172.20.0.4 down;
}
```

重启服务器，查看访问效果

```
[root@localhost nginx]# service nginx restart
Redirecting to /bin/systemctl restart  nginx.service
[root@localhost nginx]# curl 172.20.0.1
This is web 2
[root@localhost nginx]# curl 172.20.0.1
This is web 2
[root@localhost nginx]# curl 172.20.0.1
This is web 2
```

好吧，仍然是 web2。

## HTTPS 

其实 HTTPS 也还是一个 server ，配置端口为 443，配置证书文件即可，可以查看我的另一篇博客 [在 Nginx 上配置 HTTPS](https://windard.com/project/2016/09/22/Use-HTTPS-In-Nginx)

```
    server {
        listen       443 ssl http2 default_server;
        listen       [::]:443 ssl http2 default_server;
        server_name  _;
        root         /usr/share/nginx/https;
        ssl on;
        ssl_certificate "/etc/nginx/server.crt";
        ssl_certificate_key "/etc/nginx/server.key";

    }
```

这样即可访问你的 HTTPS 的站，如果想在访问 HTTP 的站的时候自动跳转到 HTTPS ，则在 HTTP 的 server 里 加上一句跳转即可

```
server {
    listen 80;
    server_name www.yousite.com;
    rewrite ^(.*) https://$server_name$1 permanent;
}
```

## HTTP Basic Auth

HTTP Basic Auth 常见于网络认证，不像一般的登陆框在页面中，登陆选项也是在页面里的，HTTP Basic Auth 是 在 HTTP 层的认证协议，这种认证方式也用于 FTP 服务，效果类似于这样。

![http_basic_auth](/images/http_basic_auth.png)

```
        location / {
                auth_basic "Nginx auth";
                auth_basic_user_file /etc/nginx/httpass;
                autoindex on;
        }
```

密码文件 `/etc/nginx/httpass` 可以使用 OpenSSL 生成，也可以由 htpasswd 生成，且支持不同的密码加密方式。

```
[root@iZ2ze83hhomw2zcf15c3qcZ nginx]# htpasswd -c /etc/nginx/httpass admin
New password:
Re-type new password:
Adding password for user admin
[root@iZ2ze83hhomw2zcf15c3qcZ nginx]# printf "windard:$(openssl passwd -crypt 123456)\n">>/etc/nginx/httpass
[root@iZ2ze83hhomw2zcf15c3qcZ nginx]# cat httpass
admin:$apr1$Aik16iPT$TnwHj6RqjICV9QRi0FO9S1
windard:CT9Et3q0m2L/Q
```

除了可以在 Nginx 等 web 服务器上配置 HTTP Basic Auth 服务之外，还能够直接利用服务器端代码实现，如 Python flask。

```
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Python Auth"'})   

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/secret-page')
@requires_auth
def secret_page():
    return "Auth Successful ~"

if __name__ == '__main__':
    app.run()
```

或者是使用 flask_httpauth

```
from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "windard": "123456",
    "admin": "password"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run()
```

或者是 PHP

```
<?php
  if (!isset($_SERVER['PHP_AUTH_USER'])) {
    header('WWW-Authenticate: Basic realm="PHP Auth"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Login Failed';
    exit;
  } else {
    if($_SERVER['PHP_AUTH_USER'] == "admin" && $_SERVER['PHP_AUTH_PW'] == 'password'){
        echo "Login Successful !";
    }
  }
?>
```

## 参考链接

[nginx的配置、虚拟主机、负载均衡和反向代理 (一)](https://www.zybuluo.com/phper/note/89391)

[nginx的配置、虚拟主机、负载均衡和反向代理 (二)](https://www.zybuluo.com/phper/note/90310)
